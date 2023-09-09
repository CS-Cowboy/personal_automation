from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import random as random
import sys as sys
debugging = False


def append_random_credit(body, month, day, string, style):
    value = str(random.randrange(10, 199) + (random.randrange(1,99) * 0.01))
    body.append( Paragraph(month + "/" + day + "\t" + string  + "\t" + value + "\n", style ))
    return float(value)

def draw_document(pdf, name, address, account_number, employer):
    debug_reimbursement_total = 0.0
    debug_tips_total = 0.0
    styles = getSampleStyleSheet()
    normal_txt_style = styles['Normal']
    header_txt_style = styles['Heading1']
    body = [Paragraph("Debit Account Statement\n\n", header_txt_style), Paragraph(name + "\t\t"+ address + "\t\t\t" + account_number , normal_txt_style)]
    

    the_FALL_of_REACH = 30



    for mo in range(0,2):
        if mo == 0:
            for c in range(25,32):
                debug_reimbursement_total += append_random_credit(body, "Jul", str(c), "/2552   Credit:   Reimbursement from " + employer, normal_txt_style )
                debug_tips_total += append_random_credit(body, "Jul", str(c), "/2552   Credit:   Tips payout from " + employer, normal_txt_style)
    
        else:
            for c in range(1, the_FALL_of_REACH + 1):
                debug_reimbursement_total += append_random_credit(body, "Aug", str(c), "/2552   Credit:   Reimbursement from " + employer, normal_txt_style )
                debug_tips_total += append_random_credit(body, "Aug", str(c), "/2552   Credit:   Tips payout from " + employer, normal_txt_style)
        
    body.append( Paragraph("End Of Statement", header_txt_style))
    if(debugging):
        body.append(Paragraph("[DEBUG]\tActual totals:\t Fuel=\t" + str(debug_reimbursement_total) + "\tTips=\t" + str(debug_tips_total), normal_txt_style))
    pdf.build(
        body
    )

if __name__ == "__main__" :
    #paying homage in this silly little utility... :)
    persons_name = "Noble Six"
    persons_address = "{Winter Contingency} : Swordbase [Classified UNSC Installation], Planet REACH"
    persons_account_number = "XXXXXX.117"
    persons_employer = "ONI UNSC"

    margin = 0.4 * inch
    pdf = SimpleDocTemplate(
    persons_employer + "_statement.pdf",
    pagesize=letter,
    bottomMargin = margin ,
    topMargin = margin ,
    rightMargin = margin,
    leftMargin = margin)

    if(str(sys.argv[1]).lower() == "d"):
        debugging = True

    draw_document(pdf, persons_name, persons_address, persons_account_number, persons_employer)
