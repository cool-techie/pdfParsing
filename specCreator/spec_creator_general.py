class SpecNode:
    def __init__(self, name, regulation, primary_keys, additional_primary_keys, secondary_keys):
        self.name = name
        self.regulation = regulation
        self.primary_keys = primary_keys
        self.additional_primary_keys = additional_primary_keys
        self.secondary_keys = secondary_keys

    def print_spec(self):
        print(self)

# Create all specs to act as a knowledge base
# These specs will then be used to validate the Test Reports
def create_general_specs_knowledge_base():
    specs = []

    spec1_pk = ['16 CFR 1303', 'U.S. CFR', 'CPSIA Section 101', 'CPSIA S.101', 'ASTM F963-11', 'CPSC-CH-E1003-09.1', '16 CFR Part 1303']
    apk1 = ['16', 'CFR', '1303']
    apk2 = ['CPSIA', '101']
    apk3 = ['Consumer', 'Product', 'Safety', 'Improvement', 'Act', '2008', '101']
    apk4 = ['ASTM', 'F96311']  # sometimes - is omitted by OCR
    spec1_apks = [apk1, apk2, apk3, apk4]
    spec1_sk = ['total lead', 'surface coating']
    spec1 = SpecNode("S000306", "16 CFR 1303", spec1_pk, spec1_apks, spec1_sk)
    specs.append(spec1)

    spec2_pk = ['CPSIA Section 101', 'CPSIA S.101', 'ASTM F963-11', 'EPA 3050/3051']
    apk2_1 = ['CPSIA', '101']
    apk2_2 = ['Consumer', 'Product', 'Safety', 'Improvement', 'Act', '2008', '101']
    apk2_3 = ['ASTM', 'F96311'] # sometimes - is omitted by OCR
    spec2_apks = [apk2_1, apk2_2, apk2_3]
    spec2_sk = ['total lead', 'substrate']
    spec2 = SpecNode('S000309', 'CPSIA Section 101', spec2_pk, spec2_apks, spec2_sk)
    specs.append(spec2)

    spec3_pk = ['ASTM F963-16', 'CPSIA']
    apk3_1 = ['CPSIA', '106']
    apk3_2 = ['Consumer', 'Product', 'Safety', 'Improvement', 'Act', '2008', '106']
    apk3_3 = ['ASTM', 'F96316']  # sometimes - is omitted by OCR
    spec3_apks = [apk3_1, apk3_2, apk3_3]
    spec3_sk = ['physical', 'mechanical'] # can also include <optional> matches like `Toys` here, which could increase rating.
    spec3 = SpecNode('S001977', 'CPSIA Section 106', spec3_pk, spec3_apks, spec3_sk)
    specs.append(spec3)

    return specs


