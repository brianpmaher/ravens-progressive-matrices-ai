# A single object node in a cell.
class SemanticNetworkNode:
    PROPERTY_KEYS = ['shape', 'fill', 'size']
    RELATION_KEYS = []

    def __init__(self, ravens_object):
        self.TRANSFORMATIONS = [
            dict(name='unchanged',
                 weight=5,
                 compare=self.__is_unchanged,
                 transform=self.__apply_unchanged),
            dict(name='reflected',
                 weight=4,
                 compare=self.__is_reflected,
                 transform=self.__apply_reflected),
            dict(name='rotated',
                 weight=3,
                 compare=self.__is_rotated,
                 transform=self.__apply_rotated),
            dict(name='scaled',
                 weight=2,
                 compare=self.__is_scaled,
                 transform=self.__apply_scaled),
            dict(name='deleted',
                 weight=1,
                 compare=self.__is_deleted,
                 transform=self.__apply_deleted),
            dict(name='changed',
                 weight=0,
                 compare=self.__is_shape_changed,
                 transform=self.__apply_shape_changed)
        ]

        self.ravens_object = ravens_object
        self.properties = {}
        self.relations = {}
        self.transformations = {}
        self.id = 0

        if ravens_object is None:
            return

        # set attributes for each object
        for attr_key, attr_value in ravens_object.attributes.iteritems():
            if attr_key in self.PROPERTY_KEYS:
                # Example format
                # properties: {
                #     'shape': 'square',
                #     'fill': True
                # }
                self.properties[attr_key] = attr_value
            elif attr_key in self.RELATION_KEYS:
                # Example format
                # relations: {
                #     'above': ['a', 'b', 'c'],
                #     'inside': ['d']
                # }
                if attr_key in self.relations:
                    self.relations[attr_key].append(attr_value)
                else:
                    self.relations[attr_key] = []

    def __is_unchanged(self, node, direction):
        if self.same_as(node):
            node.id = self.id
            self.transformations[direction] = 'unchanged'
            return True
        return False

    def __is_reflected(self, node):
        return False

    def __is_rotated(self, node):
        return False

    def __is_scaled(self, node):
        return False

    def __is_deleted(self, node):
        return False

    def __is_shape_changed(self, node):
        return False

    def __apply_unchanged(self, node=None):
        if node is None:
            node = SemanticNetworkNode(None)
        node.id = self.id
        node.properties = self.properties
        return node

    def __apply_reflected(self):
        return None

    def __apply_rotated(self):
        return None

    def __apply_scaled(self):
        return None

    def __apply_deleted(self):
        return None

    def __apply_shape_changed(self):
        return None

    def transform_index_from_name(self, transform_name):
        for i in range(0, len(self.TRANSFORMATIONS)):
            if self.TRANSFORMATIONS[i]['name'] == transform_name:
                return i

    def same_as(self, node):
        if self.properties == node.properties:
            return True
        return False
