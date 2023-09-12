import sys as sys
import re as re
from PyPDF2 import PdfReader

def containsCredit(line):
    match_credit = re.compile(r'Credit:.+$')
    return (match_credit.search(line) is not None)

def containsTip(line):
    match_tips = re.compile(r'Tips.+$')
    found = match_tips.search(line)
    return found is not None

def containsReimbursement(line):
    match_credit = re.compile(r'Reimbursement.+$')
    found = match_credit.search(line)
    return found is not None

def getQuantity(line):
    match_quantity = re.compile(r'[0-9]+\.[0-9]+')
    return float(match_quantity.search(line).group())

def printStatement(data, otput):
    print("Itemized breakdown:\n")
    for group in data:
        print(group, "\t:=", data[group], "\n")
    print("Total:=\t", otput)

if len(sys.argv) == 2:
    
    f = open(str(sys.argv[1]), 'rb')
    reader = PdfReader(f)
    totalEarns = float(0)
    totalReimb = float(0)
    quantities = 0
    days = 1
    week_no = 1
    reimbursements = dict({})
    earnings = dict({})
    for page in reader.pages:
        lines = page.extract_text().split('\n')
        for text in lines:
            if(containsCredit(text)):
                if((days % 15) == 0 or days == 1):
                    week = 'week_' +str(week_no)
                    reimbursements.update({week : []})
                    earnings.update({week : []})
                    week_no += 1
                    days = 1
                val = getQuantity(text)
                if(containsReimbursement(text)):
                    reimbursements[week].append(val)
                    totalReimb += val
                if(containsTip(text)):
                    earnings[week].append(val)
                    totalEarns += val
                days+=1
                
    print("EARNINGS:\n")
    printStatement(earnings, totalEarns)
    print("REIMBURSED:\n")
    printStatement(reimbursements, totalReimb)
    f.close()
else:
    print('usage: python earnings_calculator.py <pdf_to_read>\n')