class SemanticNetworkNode:
    """A single object node in a cell.

    Module Attributes:
        PROPERTY_KEYS (list(str)): The list of keys that represent object
            properties.
        RELATION_KEYS (list(str)): The list of keys that represent object
            relationships.

    Attributes:
        TRANSFORMATIONS (list(dict(name (str), weight (int), compare (function),
            transform (function)))): A list of dictionaries that include data
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

    PROPERTY_KEYS = ['shape', 'fill', 'size', 'angle']
    RELATION_KEYS = ['inside']

    def __init__(self, ravens_object=None):
        self.TRANSFORMATIONS = [
            dict(name='unchanged',
                 weight=5,
                 compare=self.__is_unchanged,
                 transform=self.__apply_unchanged),
            dict(name='reflected', weight=4,
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

    @staticmethod
    def __calculate_reflected_rotation(shape, angle, direction):
        """Calculates the reflected rotation of the shape.

        Reflections are dependant on the type of shape being reflected.
        For example:
            Circle:
                Would be the same (unchanged).
            Diamond:
                Would be the same (unchanged).
            Pac-man:
                Would be a 180 degree rotation.
            Plus:
                Would be the same (unchanged).
            Right Triangle:
                A right triangle reflection is the same as a (+/-)90degree
                rotation. Additionally, this rule is not enough; these rotations
                must correspond to specific starting rotations and which axis
                they are being rotated.
                0   -> x: +90deg, y: -90deg        Note: these rules are hard-
                90  -> x: -90deg, y: +90deg        coded. There is probably an
                180 -> x: +90deg, y: -90deg        algorithm to do this more
                270 -> x: -90deg, y: +90deg        precisely.
            Square:
                Would be the same (unchanged). It's possible that squares could
                be rotated, in which case the reflection would be a (+/-)180deg
                rotation, but that's not relevant fot the Basic problems.

        Args:
            shape (str): The shape being reflected.
            angle (int): The starting angle of the shape being reflected.
            direction (str): The direction of the reflection (row or column).

        Returns:
            (int): The new angle of the shape, when reflected.
        """

        pacman_reflection_map = {
            0: dict(column=0, row=180),
            45: dict(column=270, row=90),
            90: dict(column=180, row=0),
            135: dict(column=90, row=-90),
            180: dict(column=0, row=-180),
            225: dict(column=-90, row=90),
            270: dict(column=-180, row=0),
            315: dict(column=-270, row=-90)
        }

        right_triangle_reflection_map = {
            0: dict(column=90, row=-90),
            90: dict(column=-90, row=90),
            180: dict(column=90, row=-90),
            270: dict(column=-90, row=90)
        }

        # There may be a better algorithm for finding the reflection of all
        # shapes... but for now, I'm just hard-coding the ones I come across.
        if shape == 'circle':
            reflected_rotation = 0
        elif shape == 'diamond':
            reflected_rotation = 0
        elif shape == 'pac-man':
            reflected_rotation = \
                (angle + pacman_reflection_map[angle][direction]) % 360
        elif shape == 'plus':
            reflected_rotation = 0
        elif shape == 'right triangle':
            reflected_rotation = \
                (angle + right_triangle_reflection_map[angle][direction]) % 360
        elif shape == 'square':
            reflected_rotation = 0
        return reflected_rotation

    def __compare_property(self, property_name, node):
        """Compares the property from this node with the node passed in.

        Args:
            property_name (str): The name of the property to compare.
            node (SemanticNetworkNode): The node to compare with.

        Returns:
            (bool): Whether or not the property exists on both nodes and whether
                the properties match if they do exist.
        """

        return property_name in self.properties and \
               property_name in node.properties and \
               self.properties[property_name] == node.properties[property_name]

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

    def __is_reflected(self, node, direction):
        """Check if the object is reflected.

        Args:
            node (SemanticNetworkNode): The node to compare with.
            direction (str): The direction the node is relative to this node.

        Returns:
            (bool): Whether or not the node is reflected.
        """

        # Check to make sure all not rotation related properties are the same.
        # Basically this shape should be the same in every way, except it's
        # rotation and position.
        if self.__compare_property('shape', node) and \
                self.__compare_property('size', node) and \
                self.__compare_property('fill', node):

            # Some shapes don't have angle property. For those shapes just give
            # them an angle property.
            if 'angle' not in self.properties:
                self.properties['angle'] = '0'
            if 'angle' not in node.properties:
                node.properties['angle'] = '0'

            # Get the rotation of the shape when it's been rotated.
            reflected_rotation = \
                SemanticNetworkNode.__calculate_reflected_rotation(
                    self.properties['shape'], int(self.properties['angle']),
                    direction
                )

            # Check if the calculated reflected rotation matches up with the
            # angle of the node we're comparing against.
            if int(node.properties['angle']) == reflected_rotation:
                node.id = self.id
                self.transformations[direction] = 'reflected'
                return True
        return False

    def __is_rotated(self, node, direction):
        return False

    def __is_scaled(self, node, direction):
        return False

    def __is_deleted(self, node, direction):
        return False

    def __is_shape_changed(self, node, direction):
        return True

    def __apply_unchanged(self, node, _direction=''):
        """Applies the unchanged transformation onto this node.

        Generates a node that is unchanged from this node.

        Args:
            node (SemanticNetworkNode): The node to compare with.
            direction (str): The direction this node's transformations are
                being applied. (unused).

        Returns:
            (SemanticNetworkNode): A copy of this node, unchanged.
        """

        # If the node doesn't exist yet, then just create it.
        if node is None:
            node = SemanticNetworkNode(None)

        node.id = self.id
        node.properties = self.properties
        return node

    def __apply_reflected(self, node, direction):
        """Applies the reflected transformation onto this node.i

        Generates a node that is reflected from this node.

        Args:
            node (SemanticNetworkNode): The node to compare with.
            direction (str): The direction this node's transformations are
                being applied.

        Returns:
            (SemanticNetworkNode): A copy of this node, reflected.
        """

        # If the node doesn't exist yet, then just create it as a replica of
        # this node.
        if node is None:
            node = SemanticNetworkNode(None)
            node.properties = self.properties

        node.id = self.id

        # We want to give ourselves a default angle of 0 if the shape is a shape
        # that doesn't have an angle for some reason.
        if 'angle' not in self.properties:
            self.properties['angle'] = '0'

        reflected_rotation = \
            SemanticNetworkNode.__calculate_reflected_rotation(
                self.properties['shape'], int(self.properties['angle']),
                direction
            )

        node.properties['angle'] = str(reflected_rotation)
        return node

    def __apply_rotated(self, node, _direction=''):
        return None

    def __apply_scaled(self, node, _direction=''):
        return None

    def __apply_deleted(self, node, _direction=''):
        return None

    def __apply_shape_changed(self, node, _direction=''):
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

        # Some shapes do not have an angle. For those shapes, lets consider the
        # angle to be 0 for comparison.
        if 'angle' not in self.properties:
            self.properties['angle'] = '0'
        if 'angle' not in node.properties:
            node.properties['angle'] = '0'

        if self.properties == node.properties:
            return True
        return False
