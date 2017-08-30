#!/usr/bin/env python3

import collections
import ifcopenshell
import sys
from sys import stdout

def attr2str(attr):
    if attr is None:
        return "$"

    if isinstance(attr, str):
        return "'%s'" % attr

    if isinstance(attr, int) or isinstance(attr, float):
        return "%s" % attr

    if isinstance(attr, ifcopenshell.entity_instance):
        a_id = attr.id()
        if a_id != 0:
            return "<a href=\"#%s\">#%s</a>" % (a_id, a_id)
        else:
            a_info = attr.get_info()
            return "%s(%s)" % (a_info["type"], a_info["wrappedValue"])
            

    if isinstance(attr, collections.Iterable): # tuple, list or somesuch
        return "(%s)" % ",".join([attr2str(a) for a in attr])

    return type(attr)

if len(sys.argv) < 2:
    print("No IFC file specified")
    sys.exit(-1)

IfcFileName = sys.argv[1]

stdout.write("<html><body>\n")

IfcFile = ifcopenshell.open(IfcFileName)

for entity in IfcFile:
    e_id = entity.id()
    e_type = entity.get_info()["type"]
    attrs = ", ".join([attr2str(a) for a in entity])
#    for attrib in entity:
#        stdout.write("%s " % (attr2str(attrib)))

    stdout.write("<a name=\"%s\">#%s=%s(%s)</a><br>\n" % (e_id, e_id, e_type, attrs))

stdout.write("</body></html>\n")
