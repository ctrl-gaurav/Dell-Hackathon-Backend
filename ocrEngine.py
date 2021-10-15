import easyocr
import cv2
import numpy as np

class OCR():
    def __init__(self) -> None:
        pass

    def engine(self, path):
        reader = easyocr.Reader(['en'], gpu=False)
        image_file_name = path
        image = cv2.imread(image_file_name)

        # sharp the edges or image.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        r_easy_ocr = reader.readtext(thresh)

        return r_easy_ocr