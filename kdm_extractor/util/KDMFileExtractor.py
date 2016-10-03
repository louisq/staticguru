import re

TOIF_PATTERN = re.compile("<http://toif/(\d+)> <http://toif/(\w+)(?::(\w+))?>")
TOIF_ID_PATTERN = re.compile("<http://toif/\d+> <http://toif/.+> <http://toif/(\d+)>")
TOIF_STRING_PATTERN = re.compile(r'<http://toif/\d+> <http://toif/\w+> "(.*)"')

TOIF_CHILDREN_KEY = "children"

# Toif adds certain values that we are not interested of for the bug prediction
ELEMENT_EXCLUSION_LIST = ['project', 'role', 'organization']

"""
This tool allows the KDM file to be read and it's components extracted for additional analysis
"""


def extractfile(file_path):

    toif_types_not_supported = []

    contents = open(file_path).read()

    lines = contents.split('\n')

    components = ToifComponents()

    for line in lines:
        is_toif_line = TOIF_PATTERN.match(line)

        if is_toif_line:
            toif_line_index = is_toif_line.group(1)

            # print line
            element_type = is_toif_line.group(2)
            # element_type = TOIF_ELEMENT_TYPE_PATTERN.match(line).group(1)

            if len(is_toif_line.groups()) == 3 and is_toif_line.group(3) is not None:
                relation = is_toif_line.group(3)

                components.add_component_element(toif_line_index, relation, TOIF_ID_PATTERN.match(line).group(1))
            else:

                if element_type == "contains":
                    components.add_component_child(toif_line_index, TOIF_ID_PATTERN.match(line).group(1))
                elif element_type in ELEMENT_EXCLUSION_LIST:
                    pass
                else:
                    element_value = TOIF_STRING_PATTERN.match(line)

                    if element_value is None:
                        pass
                    else:
                        components.add_component_element(toif_line_index, element_type, TOIF_STRING_PATTERN.match(line).group(1))

        else:
            print "Excluded: %s" % line

    return components.toif_components


class ToifComponents:

    def __init__(self):
        self.toif_components = {}

    def _create_component(self, toif_component_id):
        if toif_component_id not in self.toif_components:
            self.toif_components[toif_component_id] = {TOIF_CHILDREN_KEY: []}

    def add_component_element(self, toif_component_id, element_key, element_value):

        self._create_component(toif_component_id)

        self.toif_components[toif_component_id][element_key] = element_value

    def append_component_element(self, toif_component_id, element_key, element_value):

        self._create_component(toif_component_id)

        if element_key not in self.toif_components[toif_component_id]:
            self.toif_components[toif_component_id][element_key] = [element_value]
        else:
            self.toif_components[toif_component_id][element_key].append(element_value)

    def add_component_child(self, toif_parent, toif_children):

        self._create_component(toif_parent)
        self._create_component(toif_children)

        self.toif_components[toif_parent][TOIF_CHILDREN_KEY].append(toif_children)

    def _create_component(self, toif_component_id):
        if toif_component_id not in self.toif_components:
            self.toif_components[toif_component_id] = {TOIF_CHILDREN_KEY: []}

    def add_component_element(self, toif_component_id, element_key, element_value):

        self._create_component(toif_component_id)

        self.toif_components[toif_component_id][element_key] = element_value

    def append_component_element(self, toif_component_id, element_key, element_value):

        self._create_component(toif_component_id)

        if element_key not in self.toif_components[toif_component_id]:
            self.toif_components[toif_component_id][element_key] = [element_value]
        else:
            self.toif_components[toif_component_id][element_key].append(element_value)

    def add_component_child(self, toif_parent, toif_children):

        self._create_component(toif_parent)
        self._create_component(toif_children)

        self.toif_components[toif_parent][TOIF_CHILDREN_KEY].append(toif_children)
