from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_LEFT, TA_CENTER
from reportlab.lib.enums import TA_RIGHT


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
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(1.0)
        self.line(77, 88, A4[0] - 77, 88)
        self.setFont('Times-Roman', 10)
        self.drawString(A4[0]-x, 75, page)
        self.restoreState()


if __name__ == '__main__':

    # Content
    styles = getSampleStyleSheet()
    elements = []
    elements.append(PageBreak())
    #elements.append(Paragraph("You are in page 2", styles["Normal"]))

# Heading
styles = getSampleStyleSheet()
styleN = styles['Normal']
#styleN.alignment = TA_CENTER
styleH = styles['Heading1']
styleH.alignment = TA_CENTER
styleF = styles['Heading2']
styleF.alignment = TA_RIGHT
styleU = styles['Heading3']
styleU.alignment = TA_RIGHT

doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20,
                        bottomMargin=8)
#doc.pagesize = landscape(A4)
#doc.watermark = 'SADC'


#image.drawInlineImage(image, 256, 720, width=100, height=60)

elements = []
logo = "sadc_title.gif"
im = Image(logo, 0*inch, 0*inch)
elements.append(im)
elements.append(Paragraph("Certification Report", styleH))
elements.append(Paragraph("Meeting Date: January 28, 2016", styleH))
elements.append(Paragraph("County PIG Program", styleH))

style = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=9,
    alignment=TA_LEFT,
)

elements.append(Paragraph("County: Salem County  ", style))
elements.append(Paragraph("Owner: Betty Ann Davis ", style))
elements.append(Paragraph("Farm: Betty Davis Farm ", style))
elements.append(Paragraph("Muncipality: Upper Pittsgrove Township", styleF))
elements.append(Paragraph("SADC ID#______________", styleF))
elements.append(Paragraph("County:_______m____b ___l_____", styleN))
elements.append(Spacer(1, 0.2 * inch))
elements.append(Paragraph("Acreage in Application: 42Net Acres", style))
elements.append(Paragraph("Residential Oppurtunities/Exceptions:", styleN))
elements.append(Spacer(1, 0.2 * inch))
elements.append(Paragraph(
    "Value Conclusions - Current Zoning and Environmental Regulations  " * 10, style))

# info = [
#     ['Appraiser', 'Date', 'Before', 'After', 'Easement'],
#     ['Name', 11/4/87, 26, 88, 54],
#     ['Name', 77777, 26, 66, 88],
#     ['Name', 77777, 26, 67, 89],
# ]
#
#
# table1 = Table(info, [3 * inch, 1.5 * inch, inch])
# table1_with_style = Table(info, [3 * inch, 1.5 * inch, inch])
#
# table1_with_style.setStyle(TableStyle([
#     ('FONT', (0, 0), (-1, -1), 'Helvetica'),
#     ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('FONTSIZE', (0, 0), (-1, -1), 8),
#     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#     ('BOX', (0, 0), (-1, 0), 0.25, colors.green),
#     ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
# ]))

# Table1
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER

hAppraiser = Paragraph('''<b>Appraiser<b>''', styleBH)
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

dat= [[hAppraiser, hDate, hBefore, hAfter, hEasement],
       [Appraiser, Date, Before, After, Easement]]

table = Table(dat, colWidths=[4.05 * cm, 3.7 * cm, 5 * cm,
                               3* cm, 3 * cm])

table.setStyle(TableStyle([
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.blue),
                        ]))
# Table 2
table1 = Table(dat, colWidths=[4.05 * cm, 3.7 * cm, 5 * cm,
                               3* cm, 3 * cm])

table1.setStyle(TableStyle([
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.blue),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.blue),
                        ]))

# Send the data and build the file
elements.append(Spacer(1, 0.2 * inch))
#elements.append()
elements.append(table)
elements.append(Spacer(1, 0.2 * inch))
elements.append(table1)
elements.append(Spacer(1, 0.2 * inch))
elements.append(Paragraph('Note:..............................................................', styleN))
elements.append(Image('trenton.png', 6*inch, 6*inch))
#elements.append(table1)
#elements.append(table1_with_style)
#doc.build(elements)
doc.multiBuild(elements, canvasmaker=FooterCanvas)
