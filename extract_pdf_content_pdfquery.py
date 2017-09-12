from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import pdfquery
from extractors.pdf_text_key_extractor import extract_key_value
import specCreator.spec_creator_general


global_data_map = {};

# Split the element on ':' and strip the resulting tokens of leading and trailing whitespaces
def split_and_strip(ele, key):
    tokens = ele.split(key)

    for i in xrange(len(tokens)):
        tokens[i] = tokens[i].strip() # strip spaces
        tokens[i] = tokens[i].strip(".") # strip trailing full stops
        tokens[i] = tokens[i].strip("\"") # strip any extra double quote brought by pdf extractor
        if tokens[i]:
            return tokens[i]
    return None

def find_and_insert_in_global_map(key, found_pdf_record):
    value = split_and_strip(found_pdf_record, key)
    if value is not None:
        global_data_map[key.lower()] = value
    else:
        global_data_map[key.lower()] = None

# Add logic to identify the Spec Test Keywords like ASTM/SOR etc. and the type of spec like flammability etc.
# Add logic to look for the result on the very right.

global_spec_map = {}
def find_label(label):
    labels = pdf.pq('LTTextLineHorizontal:contains("%s")' % (label))
    labels = labels('LTTextLineHorizontal')
    total_specs = len(labels)
    for i in range(0, total_specs):
        label = labels.eq(i)
        # get the coordinates of the spec text box
        left_corner = float(label.attr('x0'))
        bottom_corner = float(label.attr('y0'))
        right_corner = float(label.attr('x1'))
        top_corner = float(label.attr('y1'))
        #print(left_corner, bottom_corner, right_corner, top_corner)
        # the values are adjusted slightly to ensure any co-ordinates mismatch
        spec_res = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (right_corner+10, bottom_corner-5, right_corner+400, top_corner+5)).text()
        spec = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner-20, right_corner+200, top_corner)).text()

        #print("{0} -- {1}".format(spec, spec_res))
        global_spec_map[spec] = spec_res

def get_all_spec_names_matching_primary_key(spec_names, primary_key):
    matching_spec_1 = set() # set
    #print ("{0} -- {1}".format(primary_key, spec_names))
    for spec_name in spec_names:
        if primary_key in spec_name:
            matching_spec_1.add(spec_name)

    return matching_spec_1

def get_all_spec_names_matching_additional_primary_key(spec_names, add_primary_key):
    matching_specs = set()

    #print ("{0} -- {1}".format(add_primary_key, spec_names))
    for spec_name in spec_names:
        if all(tokens in spec_name for tokens in add_primary_key):
            matching_specs.add(spec_name)

    return matching_specs


if __name__ == '__main__':

    pdf = pdfquery.PDFQuery("/Users/mehrap/Desktop/ML_Stuff/122310480X-GUNBQ/report.pdf")
    #pdf = pdfquery.PDFQuery("/Users/mehrap/Desktop/ML_Stuff/US:CA Report/CA Sample Reports/HKGH0209242709.pdf")
    #pdf = pdfquery.PDFQuery("/Users/mehrap/Desktop/ML_Stuff/US:CA Report/US Sample Reports/scanned.pdf")

    pdf.load(0)
    #pdf.tree.write('test.xml', pretty_print=True)

    if len(pdf.tree.xpath('//*/LTTextLineHorizontal')) == 0:
        print ("PDF is scanned pdf. Use Ocr")
        exit(0)

    coo_key = "Country of Origin"
    coo_pdf_record = extract_key_value(coo_key, pdf)
    find_and_insert_in_global_map(coo_key, coo_pdf_record)


    date_key = "Date"
    date_pdf_record = extract_key_value(date_key, pdf)
    find_and_insert_in_global_map(date_key, date_pdf_record)

    # need to try with permutations as well since diff reports have different formats
    # Example "Labelled Age Group" vs "Labelled age group" (notice the caps)
    age_group_keys = ["Labelled age group", "Labelled Age Group"]
    for age_group_key in age_group_keys:
        age_group = extract_key_value(age_group_key, pdf)
        if age_group is not None:
            find_and_insert_in_global_map(age_group_key, age_group)

    pdf.load(1)
    #pdf.tree.write('test.xml', pretty_print=True)

    #initialize global spec map by comparing all Spec Node Primary Keys on PDF Element Tree
    spec_nodes = specCreator.spec_creator_general.create_general_specs_knowledge_base()
    for spec_node in spec_nodes:
        for pk in spec_node.primary_keys:
            find_label(pk)

    spec_names_in_report = list(global_spec_map.keys())

    for spec_node in spec_nodes:
        spec_primary_keys = spec_node.primary_keys
        spec_additional_primary_keys = spec_node.additional_primary_keys
        spec_secondary_keys = spec_node.secondary_keys

        matching_spec_names = set()
        for primary_key in spec_primary_keys:
            matching_spec_names.update(get_all_spec_names_matching_primary_key(spec_names_in_report, primary_key))

        for add_primary_key in spec_additional_primary_keys:
            matching_spec_names.update(
                get_all_spec_names_matching_additional_primary_key(spec_names_in_report, add_primary_key))

        if not matching_spec_names:
            print #("No matching spec names found in report for Spec {0}".format(spec_node.name))

        else:
            for matching_spec in matching_spec_names:
                # print("{0} - {1} - {2}".format(spec_node.name, spec_secondary_keys, matching_spec))
                if all(tokens in matching_spec.lower() for tokens in spec_secondary_keys):
                    print ("Spec {0}:{1} --[{2}]".format(spec_node.name, global_spec_map[matching_spec], matching_spec))

    print(global_data_map)


''' Way to handle Nulls in case the string key is not found

label = pdf.pq('LTTextLineHorizontal:contains("Pulkit")')
if label.attr('x0') is not None and label.attr('y0') is not None:
    left_corner = float(label.attr('x0'))
    bottom_corner = float(label.attr('y0'))
    name = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (left_corner, bottom_corner, left_corner+300, bottom_corner+15)).text()
    print(name)
    
'''
