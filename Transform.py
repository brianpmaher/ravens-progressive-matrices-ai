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

        transformations = dict(
            unchanged=Transform('unchanged', image1_data, image2_data),
            reflected_vert=Transform(
                'reflected_vert', image1_data, image2_data),
            reflected_horiz=Transform(
                'reflected_horiz', image1_data, image2_data),
            rotated_90=Transform('rotated_90', image1_data, image2_data),
            rotated_180=Transform('rotated_180', image1_data, image2_data),
            rotated_270=Transform('rotated_270', image1_data, image2_data)
        )

        transformations_names = [
            'unchanged',
            'reflected_vert',
            'reflected_horiz',
            'rotated_90',
            'rotated_180',
            'rotated_270'
        ]

        best_match = transformations['unchanged']
        for transformation in transformations_names:
            if transformations[transformation].match > best_match.match:
                best_match = transformations[transformation]
                if best_match.match > .98:
                    break
        return {best_match.name: best_match}

    def __init__(self, name, image1_data, image2_data):
        self.transformations_map = {
            'unchanged': self.match_unchanged,
            'reflected_vert': self.match_reflected_vert,
            'reflected_horiz': self.match_reflected_horiz,
            'rotated_90': self.match_rotated_90,
            'rotated_180': self.match_rotated_180,
            'rotated_270': self.match_rotated_270
        }

        self.name = name
        self.image1_data = image1_data
        self.image2_data = image2_data
        self.match = self.transformations_map[name](image1_data, image2_data)

    def match_unchanged(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['pixels'], image2_data['pixels']
        )

    def match_reflected_vert(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['image'].transpose(Image.FLIP_TOP_BOTTOM).getdata(),
            image2_data['pixels']
        )

    def match_reflected_horiz(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['image'].transpose(Image.FLIP_LEFT_RIGHT).getdata(),
            image2_data['pixels']
        )

    def match_rotated_90(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['image'].transpose(Image.ROTATE_90).getdata(),
            image2_data['pixels']
        )

    def match_rotated_180(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['image'].transpose(Image.ROTATE_180).getdata(),
            image2_data['pixels']
        )

    def match_rotated_270(self, image1_data, image2_data):
        return ImageUtils.match_percentage(
            image1_data['image'].transpose(Image.ROTATE_270).getdata(),
            image2_data['pixels']
        )

    def apply_and_compare(self, image1_data, image2_data):
        """Applies this transformation to image1 and compares with image2."""

        return self.transformations_map[self.name](image1_data, image2_data)
