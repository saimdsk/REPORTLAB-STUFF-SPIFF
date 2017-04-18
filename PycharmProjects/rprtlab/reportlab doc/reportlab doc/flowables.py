from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
styleF = styles['Heading2']
story = []
#add some flowables
story.append(Paragraph("Certification Report"
                       "Meeting Date: January 28,2016"
                       "County PIG Program",styleH))
story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
styleN))
c = Canvas('mydoc.pdf')
f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
f.addFromList(story,c)
c.save()