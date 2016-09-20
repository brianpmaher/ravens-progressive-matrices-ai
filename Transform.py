from ImageUtils import ImageUtils

class Transform:
    @staticmethod
    def match_unchanged(image1_data, image2_data):
        return ImageUtils \
            .match_percentage(image1_data['pixels'], image2_data['pixels'])

    @staticmethod
    def match_reflected(image1_data, image2_data):
        pass

    @staticmethod
    def match_rotated(image1_data, image2_data):
        pass

    @staticmethod
    def match_fill_changed(image1_data, image2_data):
        pass

    @staticmethod
    def generate_transforms_data(image1_data, image2_data):
        """Generates transformations along with percentage matches.

        Args:
            image1_data (dict): Dictionary of image data in the form:
                dict(image, pixels).
            image2_data (dict): Dictionary of image data in the form:
                dict(image, pixels).

        Return:
            (dict): Dictionary of transform data in the form:
                dict(transform, match).
        """

        return dict(
            unchanged=Transform('unchanged', image1_data, image2_data),
            #reflected=Transform('reflected', image1_data, image2_data),
            #rotated=Transform('rotated', image1_data, image2_data),
            #fill_changed=Transform('fill_changed', image1_data, image2_data)
        )

    def __init__(self, name, image1_data, image2_data):
        self.transformations_map = {
            'unchanged': Transform.match_unchanged,
            'reflected': Transform.match_reflected,
            'rotated': Transform.match_rotated,
            'filled_changed': Transform.match_fill_changed
        }

        self.name = name
        self.image1_data = image1_data
        self.image2_data = image2_data
        self.match = self.transformations_map[name](image1_data, image2_data)

    def apply_and_compare(self, image1_data, image2_data):
        """Applies this transformation to image1 and compares with image2."""

        return self.transformations_map[self.name](image1_data, image2_data)

