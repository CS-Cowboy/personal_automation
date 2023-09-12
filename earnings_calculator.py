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

def printStatement(data):
    print("\tItemized breakdown:\n")
    month = list([])
    for key in data:
        print("\t\t", key, ":=  ", data[key])
        weekly_total = sum(data[key])
        month.append(weekly_total)
        print("\t\tWeek total:=  ", weekly_total, "\n\n\t\t---------------------------\n")
    months_total = sum(month)
    print("\tMonths Total:=\t\t", months_total)
    return months_total     #return for complete total.

if len(sys.argv) == 2:
    
    f = open(str(sys.argv[1]), 'rb')
    reader = PdfReader(f)
    days = 1
    week = 'week_' + str(1)
    reimbursements = dict({week : []})
    earnings = dict({week : []})
    for page in reader.pages:
        lines = page.extract_text().split('\n')
        for text in lines:
            if(containsCredit(text)):
                if((days % 15) == 0):
                    week = 'week_' + str(len(earnings)+1)
                    reimbursements.update({week : []})
                    earnings.update({week : []})
                    days = 1
                val = getQuantity(text)
                if(containsReimbursement(text)):
                    reimbursements[week].append(val)
                if(containsTip(text)):
                    earnings[week].append(val)
                
                days+=1
    print("\nEARNINGS  follow:\n")
    monthsTotalTips = printStatement(earnings)
    print("\nREIMBURSED\tfollows:\n")
    monthsTotalEarns = printStatement(reimbursements)
    print("COMPLETE MONTHS TOTAL=\t", (monthsTotalEarns + monthsTotalTips))
    f.close()
    
else:
    print('usage: python earnings_calculator.py <pdf_to_read>\n')