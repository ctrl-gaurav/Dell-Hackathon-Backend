from pdf2image import convert_from_path
import os

class ImageConverter():
    def __init__(self) -> None:
        pass

    def converter(self, pdfPath):

        files = []
        for filename in os.listdir(pdfPath):
            files.append(os.path.join(pdfPath, filename))

        for i, f in enumerate(files):
            images = convert_from_path(f)
            for image in images:
                image.save('ConvertedImages/000{}.jpg'.format(i+1), 'JPEG')