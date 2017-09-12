# -*- coding: utf-8 -*-
import re
import unicodedata

test_result_values = ['pass', 'fail']

def extract_spec_from_text(text):
    spec_line_regex = '\({}\)(.*)' #(.*) is to match till end of line
    end_regex = '\*\*\*\*\*\*' # for now this works, need to handle cases where ***** might not represent end of specs.

    text_split_by_newlines = text.splitlines()

    cleaned_text = []
    for line in text_split_by_newlines:
        line = line.strip()
        cleaned_text.append(line)

    cleaned_text = filter(None, cleaned_text)

    spec_result_dict = {}
    i = 1
    spec_name = ""
    spec_result = ""
    for line in cleaned_text:
        #print("{}: {}".format(i, unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')))
        non_unicode_line = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')
        spec_regex_match = re.search(spec_line_regex.format(i), non_unicode_line) # match (1), (2) etc...
        spec_end_regex_match = re.search(end_regex, non_unicode_line) # match *****
        if spec_regex_match:
            spec_result_dict[spec_name] = spec_result
            spec_name = ""
            expected_spec_name=spec_regex_match.group()
            expected_result = expected_spec_name.split()[-1]
            if expected_result.lower() in test_result_values: # valid spec with result
                spec_result = expected_result.lower()
                spec_name = expected_spec_name.rsplit(' ', 1)[0] # reverse split on the last word and take the 1st part of split string
            i+=1

        elif non_unicode_line.split()[-1].lower() in test_result_values:
            spec_result_dict[spec_name] = spec_result
            spec_name = non_unicode_line.rsplit(' ', 1)[0] # take all but last word
            spec_result = non_unicode_line.split()[-1].lower() #last word

        elif spec_end_regex_match:
            spec_result_dict[spec_name] = spec_result
            break

        elif spec_name:
            spec_name+=non_unicode_line


    return spec_result_dict

