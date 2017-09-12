import pdfquery
from extractors.pdf_text_key_extractor import extract_key_value
import specCreator.spec_creator_general

if __name__ == '__main__':

    pdf = pdfquery.PDFQuery("/Users/mehrap/Desktop/B000058TJ3.pdf")

    pdf.load(0)
    pdf.tree.write('test1.xml', pretty_print=True)