import easyocr
import cv2


class Address():
    def __init__(self) -> None:
        pass

    def addressInvoice(self, r_easy_ocr, st, path):

        img = cv2.imread(path)
        for i in r_easy_ocr:
            for c, j in enumerate(i):
                if c == 1:
                    if j == st:
                        bb = i[0]
        x = bb[0][0]
        y = bb[0][1]
        w = (bb[1][0] - bb[0][0]) + 400

        if st == "Invoice Number":
            h = (bb[2][1] - bb[1][1])
        else:
            h = (bb[2][1] - bb[1][1]) * 6

        crop_img = img[y:y + h, x:x + w]
        print("Running OCR on Cropped Image ....")
        reader = easyocr.Reader(['en'], gpu=False)
        res = reader.readtext(crop_img)
        abc = ""
        for r in res:
            abc = abc + r[1] + " "

        return abc