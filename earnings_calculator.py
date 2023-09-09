import sys as sys
import re as re
from PyPDF2 import PdfReader

def getCreditQuantity(line, match_target, boo):
    match_credit = re.compile(r'Credit:.+$')
    match_quantity = re.compile(r'[0-9]+\.[0-9]+')

    search_regexp = lambda string, compiled_regexp : compiled_regexp.search(string)


    found_content =  search_regexp(line, match_credit)
    if(found_content is not None):
        found_target = search_regexp(line, match_target)
        if(found_target is not None):
            value = search_regexp(line, match_quantity).group()
            #if (boo is False):
            #    print("Fuel:\t", value)
            #else:
            #    print("Tip Val=\t\t\t", value)
            return float(value)
    return float(0)

if len(sys.argv) == 2:
    
    f = open(str(sys.argv[1]), 'rb')
    reader = PdfReader(f)
    earnings = float(0)
    reimbursements = float(0)
    match_tips = re.compile(r'Tips.+$')
    match_credit = re.compile(r'Reimbursement.+$')
    quantities = 0
    for page in reader.pages:
        lines = page.extract_text().split('\n')
        for text in lines:
            earnings += getCreditQuantity(text, match_tips, True)
            reimbursements += getCreditQuantity(text, match_credit, False)
    print("Total earnings:\n", (reimbursements + earnings))
    print("Breakdown:\n")
    print('Reimbursements:\t', reimbursements)
    print('Tips:\t', earnings)

    f.close()
else:
    print('usage: python earnings_calculator.py <pdf_to_read>\n')