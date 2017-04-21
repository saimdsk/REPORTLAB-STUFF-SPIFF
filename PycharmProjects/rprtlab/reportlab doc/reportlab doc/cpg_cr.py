from PIL import Image, JpegImagePlugin
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, cm, portrait
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, Indenter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_LEFT, TA_CENTER
from reportlab.lib.enums import TA_RIGHT
import details
from functools import partial


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        # self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
        #                      "Page %d of %d" % (self._pageNumber, page_count))
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(1.0)
        self.line(47, 88, A4[0] - 47, 88)
        self.setFont('Times-Roman', 10)
        self.drawString(A4[0]-97, 75, page)
        self.restoreState()

# Heading ................................................................................................
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
styleH.alignment = TA_CENTER
styleF = styles['Heading2']
styleF.alignment = TA_RIGHT
styleU = styles['Heading3']
styleU.alignment = TA_RIGHT

doc = SimpleDocTemplate("cpp.pdf", pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20,
                        bottomMargin=8)

# doc.pagesize = landscape(A4)
doc.pagesize = portrait(A4)

elements = []
logo = "sadc_title.gif"
im = Image(logo, 0*inch, 0*inch)
elements.append(im)
elements.append(Paragraph("Certification Report", styleH))
elements.append(Paragraph("Meeting Date: January 28, 2016", styleH))
elements.append(Paragraph("County PIG Program", styleH))
elements.append(Spacer(1, 0.4*inch))

# ..................................................................................................
style_l = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=12,
    alignment=TA_LEFT,
)

style_r = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=12,
    alignment=TA_RIGHT,
)

style_c = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=12,
    alignment=TA_CENTER,
)
# ..................................................................................................
for i in details.COUNTY_LIST:
    elements.append(Paragraph("County:" + i["c"], style_l))
    elements.append(Paragraph("Owner:" + i["o"], style_l))
    elements.append(Paragraph("Farm:" + i["f"], style_l))
    elements.append(Paragraph("Muncipality:" + i["m"], style_r))
    elements.append(Paragraph("<u>SADC ID#</u>" + i["ID"], style_r))
    #elements.append(Paragraph("<b>County:</b>", styleN))
    #elements.append(Paragraph(i["c"], styleN))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("Acreage in Application: 42Net Acres(Appraisal Order Checklist)", style_l))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("<b>Residential Oppurtunities/Exceptions:</b>", style_l))
    elements.append(Paragraph("#<u>0</u>RDSOs -", style_l))
    elements.append(Paragraph("#Existing Dwellings in Easement Area", style_l))
    elements.append(Paragraph("#Non-Severable Exception(2 Acres with existing house)", style_l))
    elements.append(Spacer(1, 0.9 * inch))
    elements.append(Paragraph(
        "Value Conclusions - Current Zoning and Environmental Regulations  ", style_c))
    elements.append(Paragraph("Based on 42 Net Acres", style_c))
    elements.append(Spacer(1, 0.3 * inch))

# Table Stylesheet.................................................................................
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER

hAppraiser = Paragraph('''<b>Appraiser</b>''', styleBH)
hDate = Paragraph('''<b>Date</b>''', styleBH)
hBefore = Paragraph('''<b>Before</b>''', styleBH)
hAfter = Paragraph('''<b>After</b>''', styleBH)
hEasement = Paragraph('''<b>Easement</b>''', styleBH)

# Texts
for i in details.VALUE_CONCLUSIONS_PERACRE:
    Appraiser = Paragraph(i["A"], styleN)
    Date = Paragraph(str(i["D"]), styleN)
    Before = Paragraph(i["B"], styleN)
    After = Paragraph(i["Af"], styleN)
    Easement = Paragraph(i["E"], styleN)
# Data to be given
dat = [[hAppraiser, hDate, hBefore, hAfter, hEasement],
       [Appraiser, Date, Before, After, Easement],
       [i["A1"], i["D1"], i["B1"], i["Af1"], i["E1"]],
       [Appraiser, Date, Before, After, Easement],
       [Appraiser, Date, Before, After, Easement]]
# Table 1
table = Table(dat, colWidths=[4.05 * cm, 4.05 * cm, 5 * cm, 3 * cm, 3 * cm])

table.setStyle(TableStyle([
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                       ]))
# Table 2
table1 = Table(dat, colWidths=[4.05 * cm, 4.05 * cm, 5 * cm,
                               3 * cm, 3 * cm])

table1.setStyle(TableStyle([
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                      ]))

# Table 3
# Texts
HighlandsStatus = Paragraph('''<b>H</b>''', styleBH)
Location = Paragraph('''<b>L</b>''', styleBH)
Size = Paragraph('''S''', styleBH)
Acres = Paragraph('A', styleBH)
Shape = Paragraph('SH', styleBH)

H = Paragraph("HS", styleBH)
L = Paragraph("Loc", styleN)
S = Paragraph("Si", styleN)
A = Paragraph("AC", styleN)
SH = Paragraph("SHA", styleN)

data = [[HighlandsStatus],
        [Location],
        [Size],
        ]
table3 = Table(data, colWidths=[9.05 * cm, 4.05 * cm, 4.05 * cm, 4.05 * cm])
table3.setStyle(TableStyle([
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                        ]))
# ............................................................................................

style1 = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=11,
    alignment=TA_CENTER,
)

# Send the data and build the file
#elements.append(Spacer(1, 0.2 * inch))
#elements.append()
elements.append(Paragraph("Per Acre", style1))
elements.append(table)
elements.append(Spacer(1, 0.29 * inch))
elements.append(Paragraph("Total Value", style1))
elements.append(table1)
elements.append(Spacer(1, 0.29 * inch))
elements.append(Paragraph('<u>Note</u>:Both appraisers used 42 net acres as per the AOC.'
                          ' Tim Sheehan rounded the total values.', styleN))
elements.append(Image('pic2.jpg', 8*inch, 9*inch))
elements.append(Paragraph("FARMLAND PRESERVATION PROGRAM NJ SADC", styleH))
elements.append(PageBreak())
elements.append(Image('pic2.jpg', 8*inch, 9*inch))
elements.append(Paragraph("FARMLAND PRESERVATION PROGRAM NJ SADC", styleH))
elements.append(Spacer(1, 0.5 * inch))
elements.append(PageBreak())
elements.append(Paragraph("Reviewers Comments", styleH))
elements.append(PageBreak())
elements.append(Paragraph("Certification Report", styleH))
elements.append(Spacer(1, 0.9 * inch))
elements.append(table3)
#elements.append(table1)
#elements.append(table1_with_style)
#doc.build(elements)
doc.multiBuild(elements, canvasmaker=FooterCanvas)
