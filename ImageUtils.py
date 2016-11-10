import numpy as np

BLACK_PIXEL = (0, 0, 0, 255)


class ImageUtils:
    @staticmethod
    def get_image_data(image):
        image_data = []

        for pixel in image.getdata():
            if pixel == BLACK_PIXEL:
                image_data.append(1)
            else:
                image_data.append(0)

        return np.int_(image_data)

    def __init__(self):
        pass
