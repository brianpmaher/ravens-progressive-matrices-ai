class ImageUtils:
    @staticmethod
    def match_percentage(image1_pixels, image2_pixels):
        """Compares two image's pixels and returns the percentage that those
        two pixel lists match.

        Args:
            image1_pixels (list): A list of pixels in an image.
            image2_pixels (list): A list of pixels in an image.

        Return:
            (float): Percentage the two pixel lists match.
        """

        match, total = 0, 0
        for i in range(len(image1_pixels)):
            if image1_pixels[i] == image2_pixels[i]:
                match += 1
                total += 1
            else:
                total += 1
        return float(match) / float(total)

    @staticmethod
    def black_pixel_count(image_pixels):
        black = 0
        for i in range(len(image_pixels)):
            if image_pixels[i] == (0, 0, 0, 255):
                black += 1
        return black
