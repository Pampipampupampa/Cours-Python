#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""


    Read a  xml file and add new item into it.
    field_dict used to add text according to tag name

    Some useful solutions to print a pretty xml file :
    ---> Hack used to print pretty xml (to_beautiful_xml)

    ---> Tail can be used too : Provide a way to add all type of object
         except application-specific object after elements ending tag and
         before the next tag. (indent)

    ---> The lxml module which is a externe library can be used
"""


########################################
#### Classes and Methods imported : ####
########################################


import xml.etree.ElementTree as ET

from random import randint
from sys import exit as sys_exit
from functools import wraps


#####################
#### Constants : ####
#####################


# Fields with specific value, else "str(randint(0, 255)" will be used
field_dict = {"Style": str(0),
              "Width": str(2)}


#######################################
#### Classes, Methods, Functions : ####
#######################################


def benchmark(func):
    """
        Time function
    """
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{} has spent {} sec to finish".format(func.__name__,
                                                     time.process_time()-t))
        return res
    return wrapper


def clean_xml(xml_file, head_length=157):
    """
        Open an xml file and return :
        First <head_length> caracters
        Rest as an xml tree.
    """
    with open(xml_file) as f:
        base = f.read()
        # The boost_serialization tag raise an error
        return base[:head_length], ET.fromstring(base[head_length:])


def add_item(tree, new_fields, template, title="Yes"):
    """
       Check if we have to add some new values from <new_fields> (must be a set)
       to the xml tree <tree> according to the template <template>.
       Use title to add an attribut inside each new template[0]

       <template[0]>
        <template[1]>str(field)</template[1]>
        <template[2]>
            <field_dict>dict value</field_dict>
            <no inside field_dict>0 to 255</no inside field_dict>
            <no inside field_dict>0 to 255</no inside field_dict>
            <no inside field_dict>0 to 255</no inside field_dict>
            <field_dict>dict value</field_dict>
        </template[2]>
       </template[0]>

       Return length of added elements
    """
    try:
        elements = new_fields - {item.text for item in tree.findall(template[1])}
    except Exception as e:
        print("\nThe new_fields argument must be a set" +
              " not a {}\n".format(type(new_fields)))
        raise e

    tree.find("count").text = str(int(tree.find("count").text) + len(elements))
    for elem in elements:
        # Base of current tree
        root = ET.SubElement(tree, template[0])
        # Keep trace of when this tag was added by using an attribute
        # Idiot SolisArt parsing
        # root.set('updated', title)
        # Add text inside template[1] tag
        ET.SubElement(root, tree.find(template[1]).tag).text = str(elem)
        child = ET.SubElement(root, tree.find(template[2]).tag)
        # Add text according to tag and template
        for field in tree.find(template[2]):
            try:
                ET.SubElement(child, field.tag).text = field_dict[field.tag]
            except KeyError:
                ET.SubElement(child, field.tag).text = str(randint(0, 255))
    return len(elements)


def to_beautiful_xml(bad_xml):
    """
        Return a pretty xml. Deprecated, use indent function instead
    """
    import xml.dom.minidom as md

    bad_xml = md.parseString(ET.tostring(bad_xml, encoding="unicode"))
    # Pretty xml with bad method... (other way ????)
    # No need for first line
    return (bad_xml.toprettyxml()[23:].replace("\t\t\t\n", "").
            replace("\t\t\n", "").replace("\t\n", "").replace("\n\n", "\n"))


def indent(elem, level=0):
    """
        Recursive prettyprint formatter
    """
    indentation = "\n" + level*"    "  # End line + indentation
    if len(elem):
        # Used to indent after element with subelement
        if not elem.text or not elem.text.strip():
            elem.text = indentation + "    "  # first SubElement of an Element
        if not elem.tail or not elem.tail.strip():
            elem.tail = indentation
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indentation
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indentation


@benchmark
def update_xml_linestyle(xml_in, xml_out, template, new_fields, title="Yes"):
    """
        Open xml file and update it with new fields
    """
    head, tree = clean_xml(xml_in)
    length = add_item(tree, new_fields, template, title)
    if length == 0:
        print("Nothing to change, script ended")
        sys_exit()  # Kill script
    else:
        print("{} new element[s] to add, now continue".format(length))
        indent(tree)
        pretty_xml = ET.tostring(tree, encoding="unicode")
        with open(xml_out, "w") as f:
            f.write(head)
            f.write(pretty_xml)


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    file_in = "SolisGraphDrawingStyles.xml"
    file_out = "output.xml"

    # Data Template
    TEMPLATE = ("item", "item/first", "item/second")

    test_new = {"V3VAB", "V3VAS", "S10", "S11", "V3VSS",
                "V3VSB", "chdr1", "chdr2", "Tcons1", "Tcons11",
                "Tcons12", "Tcons4", "POSV3VSOL", "POSV3VAPP"}

    update_xml_linestyle(file_in, file_out, TEMPLATE, test_new)
