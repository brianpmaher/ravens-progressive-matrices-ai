# A single object node in a cell.
class SemanticNetworkNode:
    PROPERTY_KEYS = ['shape', 'fill', 'size']
    RELATION_KEYS = []

    def __init__(self, ravens_object):
        self.TRANSFORMATIONS = [
            dict(name='unchanged', weight=5, function=self.__is_unchanged),
            dict(name='reflected', weight=4, function=self.__is_reflected),
            dict(name='rotated', weight=3, function=self.__is_rotated),
            dict(name='scaled', weight=2, function=self.__is_scaled),
            dict(name='deleted', weight=1, function=self.__is_deleted),
            dict(name='changed', weight=0, function=self.__is_shape_changed)
        ]

        self.ravens_object = ravens_object
        self.properties = {}
        self.relations = {}
        self.transformation = ''
        self.id = 0

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

    def __is_unchanged(self, node):
        if self.properties == node.properties:
            node.id = self.id
            self.transformation = 'unchanged'
            return True
        return False

    def __is_reflected(self, node):
        pass

    def __is_rotated(self, node):
        pass

    def __is_scaled(self, node):
        pass

    def __is_deleted(self, node):
        pass

    def __is_shape_changed(self, node):
        pass
