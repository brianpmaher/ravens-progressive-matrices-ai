class SemanticNetworkNode:
    """A single object node in a cell.

    Module Attributes:
        PROPERTY_KEYS (list(str)): The list of keys that represent object
            properties.
        RELATION_KEYS (list(str)): The list of keys that represent object
            relationships.

    Attributes:
        TRANSFORMATIONS (list(dict(name(str), weight(int), compare(function),
            transform(function)))): A list of dictionaries that include data
            about various shape transformations.

            Dictionary entries of transform objects:
                name (str): The transformation name.
                weight (int): Ranked weight for the transform type. This is used
                    to compare the transform totals for a transformation or
                    between cells. The heigher the weight score, the more likely
                    the transformation.
                compare (function): A function to compare the transformation
                    type with another node to determine if the transformation
                    matches.
                transform (function): A function to apply the transformation
                    type on this node.
        ravens_object (RavensObject): The RPM figure object used to generate
            this node.
        properties (dict([, property_key (str): property_value (str)])): The
            list of properties the node has. These include some relevant
            information about the Ravens Object. Things like shape, fill, size,
            etc.

            Example format

                properties: {
                    'shape': 'square',
                    'fill': True
                }
        relations (dict([, relation_key (str): relation_value (str)])): The
            list of positional relations the node has with other nodes within
            its cell.

            Example format

                relations: {
                    'above': ['a', 'b', 'c'],
                    'inside': ['d']
                }
        transformations (dict([, direction (str): transform (str)])): The list
            of transformations the node has with nodes in other cells. These
            transformations are defined by the TRANSFORMATIONS instance
            constant.

            Example format

                transformations: {
                    'row': 'unchanged',
                    'column': 'rotated',
                    'diagonal': 'shape changed'
                }
        id (int): An identifier that helps identify this node with nodes in
            other cells. When the nodes are first generated, they are given
            irrelevant labels such as 'a', 'b', 'c'. These labels do not map to
            nodes in any cell on their own and their labels are irrelevant for
            anything other than naming within cells. So in order to make sure
            that we understand that an 'a' node and an 'e' node in separate
            cells represent the same object, we make them have the same
            identifier.
    """

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

        # Passed in when we create a new object that is not originating from a
        # RavensObject.
        if ravens_object is None:
            return

        # Set attributes for each object.
        for attr_key, attr_value in ravens_object.attributes.iteritems():
            if attr_key in self.PROPERTY_KEYS:
                self.properties[attr_key] = attr_value
            elif attr_key in self.RELATION_KEYS:
                if attr_key in self.relations:
                    self.relations[attr_key].append(attr_value)
                else:
                    self.relations[attr_key] = []

    def __is_unchanged(self, node, direction):
        """Check if the object is unchanged.

        The object should contain all of the same properties.

        Args:
            node (SemanticNetworkNode): The node to compare with.
            direction (str): The direction the node is relative to this node.
                Example: 'row', 'column', 'diagonal'

        Returns:
            (bool): Whether or not this node is unchanged when compared to the
                other node.
        """

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
        """Applies the unchanged transformation onto this node.

        Generates a node that is unchanged from this node.

        Args:
            node (SemanticNetworkNode): The node to compare with.

        Returns:
            (SemanticNetworkNode): A copy of this node, unchanged.
        """

        # If the node doesn't exist yet, then just create it.
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
        """Gets the transform index from the transform name.

        Args:
            transform_name (str): The name of the transform.

        Returns:
            (int): The transform index for the name.
        """
        for i in range(0, len(self.TRANSFORMATIONS)):
            if self.TRANSFORMATIONS[i]['name'] == transform_name:
                return i

    def same_as(self, node):
        """Checks if the node's properties are the same.

        Args:
            node (SemanticNetworkNode): Node to compare with.

        Returns:
            (bool): Whether or not this node is the same as the node passed in.
        """
        if self.properties == node.properties:
            return True
        return False
