from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, TableStyle
from reportlab.lib import colors

width, height = A4
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER


########################################################################
class Test(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height - y * unit
        return x, y

    # ----------------------------------------------------------------------
    def run(self):
        """
        Run the report
        """
        self.doc = SimpleDocTemplate("test.pdf")
        self.story = [Spacer(1, 2.5 * inch)]
        self.createLineItems()

        self.doc.build(self.story, onFirstPage=self.createDocument)
        print "finished!"

    # ----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        """
        Create the document
        """
        self.c = canvas
        normal = self.styles["Normal"]

        header_text = "<b>CERTIFICATION REPORT</b>"
        p = Paragraph(header_text, normal)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(100, 12, mm))

        ptext = """County: Salem County
                   Owner: Betty Ann Davis
                   fARM: Betty Davis Farm"""

        p = Paragraph(ptext, style=normal)
        p.wrapOn(self.c, self.width - 50, self.height)
        p.drawOn(self.c, 30, 700)

        ptext = """
        Residential Opportunities/Exceptions:
        #
        #
        #
        #
        """
        p = Paragraph(ptext, style=normal)
        p.wrapOn(self.c, self.width - 50, self.height)
        p.drawOn(self.c, 30, 600)

    # ----------------------------------------------------------------------


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

data = [[hAppraiser, hDate, hBefore, hAfter, hEasement],
        [Appraiser, Date, Before, After, Easement]]

table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                               3 * cm, 3 * cm])

table.setStyle(TableStyle([
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
]))

table.wrapOn(c, width, height)
table.drawOn(c, *coord(1.8, 9.6, cm))
# ----------------------------------------------------------------------
if __name__ == "__main__":
    t = Test()
    t.run()