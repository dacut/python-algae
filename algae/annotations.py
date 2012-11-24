#! /usr/bin/env python
from __future__ import (absolute_import, division, with_statement)

class typechecked_property(object):
    """An object descriptor supporting a typechecked property."""

    unset = object()

    def __init__(self, types, name=None, deletion=False):
        """Creates a property on the specified class which implements type
checking when the property is set."""
        super(typechecked_property, self).__init__()
        self.types = types
        if name is not None:
            self.name = name
        else:
            self.name = "typechecked_%x" % id(self)
        self.deletion = deletion
        return

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("Unknown attribute")
        result = instance.__dict__.get(self.name, self.unset)
        if result is self.unset:
            raise AttributeError("Unknown attribute")
        return result

    def __set__(self, instance, value):
        if not isinstance(value, self.types):
            raise TypeError(
                "Cannot set attribute to %s: allowed types are %s" %
                (type(value).__name__,
                 ", ".join([t.__name__ for t in self.types])))
        instance.__dict__[self.name] = value
        return

    def __delete__(self, instance):
        if not self.deletion:
            raise TypeError("Cannot delete attribute")
        del instance.__dict__[self.name]
# end typechecked_property
    
# Local variables:
# mode: Python
# tab-width: 8
# indent-tabs-mode: nil
# End:
# vi: set expandtab tabstop=8
