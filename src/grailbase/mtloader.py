"""Extension loader for filetype handlers.

The extension objects provided by MIMEExtensionLoader objects have four
attributes: parse, embed, add_options, and update_options.  The first two
are used as handlers for supporting the MIME type as primary and embeded
resources.  The last two are (currently) only used for printing.
"""
__version__ = '$Revision: 2.1 $'


import extloader
import string


class MIMEExtensionLoader(extloader.ExtensionLoader):
    def find(self, name):
        new_name = string.replace(name, "-", "_")
        major, minor = tuple(string.split(new_name, "/"))
        if minor:
            modname = "%s_%s" % (major, minor)
        else:
            modname = major
        mod = self.find_module(modname)
        ext = None
        if not mod and modname != major:
            ext = self.get(major + "/")
        elif mod:
            ext = MIMETypeExtension(name, mod, modname)
        return ext


class MIMETypeExtension:
    def __init__(self, type, mod, modname):
        self.type = name
        self.__load_attr(mod, "parse_" + modname, "parse")
        self.__load_attr(mod, "embed_" + modname, "embed")
        self.__load_attr(mod, "add_options")
        self.__load_attr(mod, "update_settings")

    def __load_attr(mod, name, as=None):
        as = as or name
        if hasattr(mod, name):
            v = getattr(mod, name)
        else:
            v = None
        setattr(ext, as, v)