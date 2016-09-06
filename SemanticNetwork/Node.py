# A single object node in a cell.
class SemanticNetworkNode:
    PROPERTY_KEYS = ['shape', 'fill', 'size']
    RELATION_KEYS = []

    def __init__(self, ravens_object):
        self.ravens_object = ravens_object
        self.properties = {}
        self.relations = []

        for attr_key, attr_value in ravens_object.attributes.iteritems():
            if attr_key in self.PROPERTY_KEYS:
                self.properties[attr_key] = attr_value
            elif attr_key in self.RELATION_KEYS:
                self.relations[attr_key] = attr_value
