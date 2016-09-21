from PIL import Image
from ImageUtils import ImageUtils


class Transform:
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
            reflected=Transform('reflected', image1_data, image2_data),
            rotated=Transform('rotated', image1_data, image2_data)
            #fill_changed=Transform('fill_changed', image1_data, image2_data)
        )

    def __init__(self, name, image1_data, image2_data):
        self.transformations_map = {
            'unchanged': self.match_unchanged,
            'reflected': self.match_reflected,
            'rotated': self.match_rotated,
            'filled_changed': self.match_fill_changed
        }

        self.name = name
        self.image1_data = image1_data
        self.image2_data = image2_data
        self.match = self.transformations_map[name](image1_data, image2_data)

    def match_unchanged(self, image1_data, image2_data):
        return ImageUtils \
            .match_percentage(image1_data['pixels'], image2_data['pixels'])

    def match_reflected(self, image1_data, image2_data):
        if hasattr(self, 'orientation'):
            image1_reflected = image1_data['image'].transpose(self.orientation)
            return ImageUtils.match_percentage(
                image1_reflected.getdata(), image2_data['pixels'])
        else:
            image1_reflected_vert = \
                image1_data['image'].transpose(Image.FLIP_TOP_BOTTOM)
            reflected_vert_match = ImageUtils.match_percentage(
                image1_reflected_vert.getdata(), image2_data['pixels'])
            image1_reflected_horiz = \
                image1_data['image'].transpose(Image.FLIP_LEFT_RIGHT)
            reflected_horiz_match = ImageUtils.match_percentage(
                image1_reflected_horiz.getdata(), image2_data['pixels'])
            max_match = max([reflected_vert_match, reflected_horiz_match])
            if max_match == reflected_vert_match:
                self.orientation = Image.FLIP_TOP_BOTTOM
            else:  # max_match == reflected_horiz_match
                self.orientation = Image.FLIP_LEFT_RIGHT
            return max_match

    def match_rotated(self, image1_data, image2_data):
        if hasattr(self, 'rotation'):
            image1_rotated = image1_data['image'].transpose(self.rotation)
            return ImageUtils.match_percentage(
                image1_rotated.getdata(), image2_data['pixels'])
        else:
            image1_rotated_90 = image1_data['image'].transpose(Image.ROTATE_90)
            rotated_90_match = ImageUtils.match_percentage(
                image1_rotated_90.getdata(), image2_data['pixels'])
            image1_rotated_180 = \
                image1_data['image'].transpose(Image.ROTATE_180)
            rotated_180_match = ImageUtils.match_percentage(
                image1_rotated_180.getdata(), image2_data['pixels'])
            image1_rotated_270 = \
                image1_data['image'].transpose(Image.ROTATE_270)
            rotated_270_match = ImageUtils.match_percentage(
                image1_rotated_270.getdata(), image2_data['pixels'])
            max_match = \
                max([rotated_90_match, rotated_180_match, rotated_270_match])
            if max_match == rotated_90_match:
                self.rotation = Image.ROTATE_90
            elif max_match == rotated_180_match:
                self.rotation = Image.ROTATE_180
            else:  # max_match == rotated_270_match
                self.rotation = Image.ROTATE_270
            return max_match

    def match_fill_changed(self, image1_data, image2_data):
        pass

    def apply_and_compare(self, image1_data, image2_data):
        """Applies this transformation to image1 and compares with image2."""

        return self.transformations_map[self.name](image1_data, image2_data)
