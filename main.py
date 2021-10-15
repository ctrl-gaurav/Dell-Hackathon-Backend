from imageConverter import ImageConverter
from ocrEngine import OCR
from gridItems import Grid
from regex import Regex
from addressInvoiceExtractor import Address
from excelWriter import Excel
import os

def final():

    # converting PDFs to image
    img = ImageConverter()
    img.converter('PDFs')
    
    # applying OCR
    ocr = OCR()
    files = []
    imgPath = 'ConvertedImages'
    for filename in os.listdir(imgPath):
        files.append(os.path.join(imgPath, filename))
    
    for i, f in enumerate(files):
        print('Running on PDF {} .....'.format(i + 1))
        r_easy_ocr = ocr.engine(f)
        # Phone Number, E-mail Regex Parsing
        reg = Regex()
        Extracted_data = reg.emailPhone(r_easy_ocr)
    
        grid = Grid()
        grid.detect(f, i+1)
    
        # Address, Invoice Recognition
        add = Address()
        inv = add.addressInvoice(r_easy_ocr, 'Invoice Number', f)
        fr = add.addressInvoice(r_easy_ocr, 'From:', f)
        to = add.addressInvoice(r_easy_ocr, 'To:', f)
    
        # writing in csv
        exc = Excel()
        name = 'GeneratedCSVs/Data_Extraction0{}.xlsx'.format(i + 1)
        exc.write(Extracted_data, inv, fr, to, name)