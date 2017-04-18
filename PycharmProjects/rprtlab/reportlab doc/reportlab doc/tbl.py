from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

width, height = A4
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER

def createdoc(h,sh,p,id):
    story=[]
    story.append()


def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

# Headers
hAppraiser = Paragraph('''<b>Appraiser</b>''', styleBH)
hDate = Paragraph('''<b>Date</b>''', styleBH)
hBefore = Paragraph('''<b>Before</b>''', styleBH)
hAfter = Paragraph('''<b>After</b>''', styleBH)
hEasement = Paragraph('''<b>Easement</b>''', styleBH)

# Texts
Appraiser = Paragraph('Name', styleN)
Date = Paragraph('m/d/y', styleN)
Before = Paragraph('$', styleN)
After = Paragraph('$', styleN)
Easement = Paragraph('$', styleN)

data= [[hAppraiser, hDate,hBefore, hAfter, hEasement],
       [Appraiser, Date, Before, After, Easement]]

table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                               3* cm, 3 * cm])

table.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))

c = canvas.Canvas("a.pdf", pagesize=A4)
table.wrapOn(c, width, height)
table.drawOn(c, *coord(1.8, 9.6, cm))
c.save()