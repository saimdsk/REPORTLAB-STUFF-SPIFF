from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
styles = getSampleStyleSheet()

doc = SimpleDocTemplate('rrrr.pdf')
elements0 = []
elements1 = []
elements2 = []

# 1-st platypus
elements0.append(Paragraph("The Platypus0", styles['Heading1']))
elements0.append(Paragraph("Very <i>Special</i>!", styles['Normal']))

# 2-nd platypus
elements1.append(Paragraph("The Platypus1", styles['Heading1']))
elements1.append(Paragraph("Very <i>Special</i>!", styles['Normal']))

# append them
elements2 = elements0 + elements1

# Write the document
doc.build(elements2)