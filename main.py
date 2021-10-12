import cv2
import numpy as np
import easyocr
import re
from pdf2image import convert_from_path
import xlsxwriter

def prototype():
    
    images = convert_from_path('temp/temp_file.pdf')
    for image in images:
        image.save('0001.jpg', 'JPEG')
    #filename = r"Single_Page_Image.jpg"

    reader = easyocr.Reader(['en'], gpu=False)  # load once only in memory.

    image_file_name = '0001.jpg'
    image = cv2.imread(image_file_name)

    # sharp the edges or image.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    r_easy_ocr = reader.readtext(thresh)


    #     Phone Number, E-mail Regex Parsing

    print(r_easy_ocr)
    st=""

    for i in r_easy_ocr:
        print(i[1])
        st = st + i[1] + " "

    #print(r_easy_ocr)

    regex_pairs = [
        [
            #Phone Number
            "Phone Number",
            #r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
            r'\b[0-9]{10}\b'
        ],
        [
            #Email
            "Email",
            #r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\b'
        ]

    ]

    Extracted_data_name = []
    Extracted_data = []

    for[name, regex] in regex_pairs:
        Extracted_data_name.append(name)
        Extracted_data.append(re.compile(regex).findall(st))


    #    Address, Invoice Recognition

    def func(st):
        img = cv2.imread("0001.jpg")
        for i in r_easy_ocr:
            for c, j in enumerate(i):
                if c == 1:
                    # print(i)
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


    inv = func('Invoice Number')
    fr = func('From:')
    to = func('To:')

    #print(inv)
    #print(fr)
    #print(to)

    Extracted_data_name.append('Invoice Number')
    Extracted_data_name.append('From')
    Extracted_data_name.append('To')
    Extracted_data.append(inv)
    Extracted_data.append(fr)
    Extracted_data.append(to)


    #Workbook creation and adding worksheets
    workbook= xlsxwriter.Workbook('Data_Extraction01.xlsx')
    worksheet = workbook.add_worksheet()

    # To start from the first cell
    row = 0
    col = 0
    a = 0
    for i in Extracted_data_name:
        col = 0
        worksheet.write(row, col, i)
        col = 1
        for j in Extracted_data[a]:
            worksheet.write(row, col, j)
            col += 1
        row += 1
        a += 1

    workbook.close()
    return