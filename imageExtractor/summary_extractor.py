import numpy as np
import argparse
import cv2
from PIL import Image
import pytesseract
import os.path
import io
import pathlib
import re

# below line is to avoid the OSError: [Errno 2] No such file or directory
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

global_data_map = {};

regexToMatch = '{}([ \t]*):(.+?)$'

def search_and_update_data_map(key, text, explicity_key=None):
    value = re.search(regexToMatch.format(key), text, re.MULTILINE | re.IGNORECASE)
    if value:
        tokens = str(value.group()).split(':')
        if not explicity_key:
            global_data_map[tokens[0].lower()] = tokens[1]
        elif explicity_key:
            global_data_map[explicity_key.lower()] = tokens[1]



''' def text_extractor(image_path):

    text = pytesseract.image_to_string(Image.open(image_path))
    return text


image = cv2.imread("/Users/mehrap/Desktop/ML_Stuff/B002B555QQ-HASAI/scanned_00.tiff")
tempImage = "{}.tiff".format(os.getpid())
cv2.imwrite(tempImage, image)
imgToProcess = Image.open(pathlib.Path(tempImage))
text = pytesseract.image_to_string(imgToProcess)
#print(text)
os.remove(tempImage) '''

def extract_text_from_page_0(text):

    search_and_update_data_map("Item name", text)
    search_and_update_data_map("Labelled Age Group", text)
    search_and_update_data_map("Test Report Number", text)
    if not "Test Report Number" in global_data_map:
        search_and_update_data_map("Test Regort Number", text, "Test Report Number")  # OCRs sometimes read p as g and q as p
    search_and_update_data_map("Date", text)

    return global_data_map

def extract_text_from_spec_summary_page(text):
    test_result_values = ['Pass', 'Fail']
    image = cv2.imread("/Users/mehrap/Desktop/ML_Stuff/B002B555QQ-HASAI/scanned_00.tiff")
    tempImage = "{}.tiff".format(os.getpid())
    cv2.imwrite(tempImage, image)
    imgToProcess = Image.open(pathlib.Path(tempImage))
    text = pytesseract.image_to_string(imgToProcess)
    os.remove(tempImage)


    result_table_header_keywords = ['Requirement', 'Reguirement', 'Requirement Result', 'Reguirement Result']
    keyword_regex = '{}(.*)'
    for keyword in result_table_header_keywords:
        spec_results = re.search(keyword_regex.format(keyword), text, re.DOTALL)
        if spec_results:
            results = spec_results.group()


