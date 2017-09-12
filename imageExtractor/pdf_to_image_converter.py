import os.path

import PIL
import cv2
import pathlib
import pytesseract
import specCreator.spec_creator_ocr
from wand.image import Image

import spec_result_extractor
import summary_extractor

pdf_filename="/Users/mehrap/Desktop/ML_Stuff/B002B555QQ-HASAI/scanned.pdf"


with(Image(filename=pdf_filename,resolution=500)) as source:
    images=source.sequence
    pages=len(images)
    for i in range(3):# change to (pages) for all pages
        Image(images[i]).save(filename=str(i)+'.png')


for i in range(2):
    image = cv2.imread(str(i)+'.png')
    tempImage = "{}.png".format(os.getpid())
    cv2.imwrite(tempImage, image)
    imgToProcess = PIL.Image.open(pathlib.Path(tempImage))
    text = pytesseract.image_to_string(imgToProcess)

    #print (text)


    if i == 0:
        summary_map = summary_extractor.extract_text_from_page_0(text)
        print(summary_map)
    elif i == 1:
        spec_map = spec_result_extractor.extract_spec_from_text(text)

    os.remove(tempImage)

for i in range(3):
    os.remove(str(i)+'.png')

# Now we have specs, need to validate them.
spec_nodes = specCreator.spec_creator_ocr.create_ocr_specs_knowledge_base()

def get_all_spec_names_matching_primary_key(spec_names, primary_key):
    matching_spec_1 = set() # set

    for spec_name in spec_names:
        if primary_key in spec_name:
            matching_spec_1.add(spec_name)

    return matching_spec_1

def get_all_spec_names_matching_additional_primary_key(spec_names, add_primary_key):
    matching_specs = set()

    for spec_name in spec_names:
        if all(tokens in spec_name for tokens in add_primary_key):
            matching_specs.add(spec_name)

    return matching_specs

# iterate over the specs found in report
spec_names_in_report = list(spec_map.keys())
#print("Spec Names in Report: {0}", spec_names_in_report)

for spec_node in spec_nodes:

    spec_primary_keys = spec_node.primary_keys
    spec_additional_primary_keys = spec_node.additional_primary_keys
    spec_secondary_keys = spec_node.secondary_keys

    matching_spec_names = set()
    for primary_key in spec_primary_keys:
        matching_spec_names.update(get_all_spec_names_matching_primary_key(spec_names_in_report, primary_key))

    for add_primary_key in spec_additional_primary_keys:
        matching_spec_names.update(get_all_spec_names_matching_additional_primary_key(spec_names_in_report, add_primary_key))


    if not matching_spec_names:
        print ("No matching spec names found in report for Spec {0}".format(spec_node.name))

    else:
        for matching_spec in matching_spec_names:
            #print("{0} - {1} - {2}".format(spec_node.name, spec_secondary_keys, matching_spec))
            if all(tokens in matching_spec.lower() for tokens in spec_secondary_keys):
                print ("Spec {0}:{1} - [{2}]".format(spec_node.name, spec_map[matching_spec], matching_spec))









