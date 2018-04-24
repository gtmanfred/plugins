# -*- coding: utf-8 -*-

# Import Python Libs
import collections
import inspect
import os
import types

# Import Hub Libs
import hub.dirs
import hub.loader
import hub.scanner


class Hub(object):
    def __init__(self):
        self._subs = collections.OrderedDict()
        self._add_system('tools', pypath='hub.mods.tools')

    def _add_system(self, modname, subname=None, pypath=None, virtual=True, recurse=False, mod_basename='hub.pack'):
        subname = subname if subname else modname
        self._subs[modname] = Pack(self, modname, subname, pypath, virtual, recurse)

    def _remove_system(self, subname):
        if subname in self._systems:
            self._subs.pop(subname)
            return True
        return False

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__getattribute__(item)
        if item in self._subs:
            return self._subs[item]
        return self.__getattribute__(item)


class Pack(object):
    def __init__(self, parent, modname, subname=None, pypath=None, virtual=True,
                 recurse=False, mod_basename='hub.pack'):
        self._parent = parent
        self._modname = modname
        self._subname = subname if subname else modname
        self._pypath = pypath
        self._virtual = virtual
        self._recurse = recurse
        self._loaded_all = False
        self._loaded = {}
        self._load_errors = {}
        self._mod_basename = mod_basename
        self.__prepare__()

    def __prepare__(self):
        self._dirs = hub.dirs.dir_list(self._pypath)
        self._scan = hub.scanner.scan(self._dirs, self._recurse)

    @property
    def __name__(self):
        return '{}.{}'.format(self._mod_basename, self._modname)

    def __iter__(self):
        if self._loaded_all is False:
            self._load_all()
        return iter(self._loaded.values())

    def _load_all(self):
        if self._loaded_all is True:
            return
        for bname in self._scan:
            if self._scan[bname].get('loaded'):
                continue
            self._load_item(bname)
        self._loaded_all = True

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__getattribute__(item)
        if item in self._loaded:
            return self._loaded[item]
        return self._find_mod(item)

    def _apply_wrapper(self, mod):
        ret = types.SimpleNamespace()
        for func_name, func in inspect.getmembers(mod, inspect.isfunction):
            if func_name.startswith('_'):
                continue
            setattr(ret, func_name, Wrapper(self._parent, func))
        return ret

    def _find_mod(self, item):
        '''
        find the module named item
        '''
        for bname in self._scan:
            if self._scan[bname].get('loaded'):
                continue
            self._load_item(bname)
            if item in self._loaded:
                return self._loaded[item]
        # Let's see if the module being lookup is in the load errors dictionary
        if item in self._load_errors:
            # Return the LoadError
            return self._load_errors[item]

    def _load_item(self, bname):
        mname = f'{self.__name__}.{os.path.basename(bname).split(".")[0]}'
        if bname not in self._scan:
            raise Exception('Bad call to load item: {mname}')
        mod = hub.loader.load_mod(mname, self._scan[bname]['path'])
        vret = hub.loader.load_virtual(self._parent, self._virtual, mod, bname)
        if 'error' in vret:
            self._load_errors[vret['name']] = vret['error']
            return
        self._loaded[vret['name']] = self._apply_wrapper(mod)
        self._scan[bname]['loaded'] = True


class Wrapper(object):
    def __init__(self, parent, func):
        self.parent = parent
        self.func = func
        self.func_name = func.__name__
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        if args and (args[0] is self.parent or isinstance(args[0], self.parent.__class__)):
            # The hub(parent) is being passed directly, remove it from args
            # since we'll inject it further down
            args = list(args)[1:]
        args = [self.parent] + list(args)
        return self.func(*args, **kwargs)

    def __repr__(self):
        return '<{} func={}.{}>'.format(self.__class__.__name__, self.func.__module__, self.func_name)
