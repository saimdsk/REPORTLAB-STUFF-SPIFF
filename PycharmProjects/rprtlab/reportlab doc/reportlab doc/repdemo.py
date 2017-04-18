from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from functools import partial
from reportlab.lib.units import inch
import time


class Demosections(Flowable):
    def __init__(self,sections,x,y):
        Flowable.__init__(self)
        self.sections = sections
        self.x = x
        self.y = y
        print sections

    def coord(self,x,y,unit = 1):
         x ,y = x*unit,y*unit
         return x,y

    def draw(self):
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading3']
        self.canv.line(0, 0, 7.5 * inch, 0)  # 0*inch, 0*inch, self.width, 0*inch)
        title = Paragraph(self.sectioninfo['sectiontitle'], style=styleH)
        title.wrapOn(self.canv, self.width, 0.5 * inch)
        title.drawOn(self.canv, self.x, self.y - 0.5 * inch)
        desc = Paragraph(self.sectioninfo['sectiondescription'], style=styleN)
        desc.wrapOn(self.canv, self.width, 0.25 * inch)
        desc.drawOn(self.canv, self.x, self.y - 1 * inch)


class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A5':
            self.pagesize = A5
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize





