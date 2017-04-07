from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from functools import partial
from reportlab.lib.units import inch
import time

'''
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    canvas.restoreState()

doc = BaseDocTemplate('test.pdf', pagesize=letter)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-2*cm, id='normal')
header_content = Paragraph("This is a multi-line header.  It goes on every page.  " * 8, styleN)
template = PageTemplate(id='test', frames=frame, onPage=partial(header, content=header_content))
doc.addPageTemplates([template])

text = []
for i in range(111):
    text.append(Paragraph("This is line %d." % i, styleN))
doc.build(text)
'''



class TextSection(Flowable):
    def __init__(self, sectioninfo, x=0*inch, y=0*inch, width=7.5*inch):
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        #self.height = height
        self.sectioninfo = sectioninfo
        print sectioninfo

    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y

    def draw(self):
        """
        Draw the Section
        """
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading3']
        self.canv.line(0,0,7.5*inch,0)#0*inch, 0*inch, self.width, 0*inch)
        title = Paragraph(self.sectioninfo['sectiontitle'], style=styleH)
        title.wrapOn(self.canv, self.width, 0.5*inch)
        title.drawOn(self.canv, self.x, self.y - 0.5*inch)
        desc = Paragraph(self.sectioninfo['sectiondescription'], style=styleN)
        desc.wrapOn(self.canv, self.width, 0.25*inch)
        desc.drawOn(self.canv, self.x, self.y - 1*inch)

        #self.canv.drawString(self.x+5, self.y+3, self.text)






class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize


    @staticmethod
    def header_footer(canvas, doc, content):
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        canvas.saveState()
        reporttitle = Paragraph(content[1], styleH)
        w, h = content[0].wrap(0.5*inch, 0.5*inch) #doc.width
        w1, h1 = reporttitle.wrap(5*inch, doc.topMargin) #doc.width
        content[0].drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        reporttitle.drawOn(canvas, doc.leftMargin + 1.5*inch, doc.height + doc.topMargin - h1)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.height - 0.25*inch, doc.width + doc.leftMargin, doc.height - 0.25*inch)

        canvas.line(doc.leftMargin, 0.75*inch, doc.width + doc.leftMargin, 0.75*inch)
        reporttitleBottom = Paragraph(content[1], styleN)
        w2,h2 = reporttitleBottom.wrap(3*inch, 0.5*inch)
        reporttitleBottom.drawOn(canvas, doc.leftMargin, 0.5*inch)

        datestamp = Paragraph("Printed on " + time.strftime("%x"), styleN)
        w3, h3 = datestamp.wrap(2*inch, 0.5*inch)
        datestamp.drawOn(canvas, doc.width - 1*inch, 0.5*inch)

        canvas.restoreState()



    def print_users(self):

        buffer = self.buffer
        """
        doc = SimpleDocTemplate(buffer,
                                rightMargin=36,
                                leftMargin=36,
                                topMargin=40,
                                bottomMargin=40,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = ['Bryce','Nolan','Beo','Benji']
        elements.append(Paragraph('My User Names', styles['Heading1']))
        for i, user in enumerate(users):
            elements.append(Paragraph(user, styles['Normal']))

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # Get the value of the BytesIO buffer and write it to the response.
        #pdf = buffer.getvalue()
        #buffer.close()
        return doc
        """
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        doc = BaseDocTemplate(buffer,
                                rightMargin=.5*inch,
                                leftMargin=.5*inch,
                                topMargin=.5*inch,
                                bottomMargin=.5*inch,
                                pagesize=letter)
        frame = Frame(doc.leftMargin, 1*inch, doc.width, doc.height-2*inch, id='normal')
        header_title = "Report Title Goes Here"
        header_content = [Image('C:\Users\oacmed1\Desktop\python_logo.png', 0.5*inch, 0.5*inch),header_title]
        template = PageTemplate(id='test', frames=frame, onPage=partial(self.header_footer, content=header_content))
        doc.addPageTemplates([template])


        reportsections = [{'sectionid':1,
                           'sectiontitle':'Section 1',
                           'sectiondescription':'Section 1 Description',
                           'sectiondata':'This is some free text that will be displayed in my text section \n Important facts and figures'
                           },{'sectionid':2,
                           'sectiontitle':'Section 2',
                           'sectiondescription':'Section 2 Description',
                           'sectiondata':'This is some free text that will be displayed in my text section \n Important facts and figures'
                           }]

        elements = []
        elements.append(TextSection(reportsections[0]))
        elements.append(Spacer(width=0, height=1*inch))
        elements.append(TextSection(reportsections[1]))

        '''
        for i in reportsections:
            newflowable = TextSection(i)

            elements.append(newflowable)
            elements.append(Spacer(width=0, height=1*inch))
        '''

        doc.build(elements)
        return doc


