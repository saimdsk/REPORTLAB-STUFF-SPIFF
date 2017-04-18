from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode

redirect = "https://yapra.github.io"

def create_qr_code(data, output_path):
    qrcode.make(data, border=0).save(output_path)

def create_pdf_stamp(output_path, add_frame=False):
    from reportlab.platypus import Image,Frame,Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.colors import Color
    from reportlab.lib.pagesizes import A4

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontSize = 8
    normal_style.fontName = 'Helvetica'
    normal_style.textColor = Color(0,0,0)

    qr_img_path = "pic.jpg"
    create_qr_code(redirect, qr_img_path)
    story1 = [Image(qr_img_path, width=22, height=22)]
    s = "stamped" \
        "with frame"
    story2 = [Paragraph(s, normal_style)]
    c = Canvas(output_path, pagesize=A4)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(1,1,1)
    if add_frame:
        c.setLineWidth(0)
        c.roundRect(2, 2, 126, 26, 2, fill=1, stroke=1)
        c.linkURL(redirect, (2, 2, 126, 26), relative=1)

    f1 = Frame(2, 2, 26, 26, 2, 2, 2, 2, showBoundary=0)
    f2 = Frame(26, 2, 100, 28, 2, 2, 2, 2, showBoundary=0)
    f1.addFromList(story1, c)
    f2.addFromList(story2, c)
    c.save()



def stamp_pdf(input_path, stamp_path, output_path, add_frame=False):
    output = PdfFileWriter()
    create_pdf_stamp(stamp_path, add_frame=add_frame)
    pdf_in = PdfFileReader(open(input_path, 'rb'))
    pdf_stamp = PdfFileReader(open(stamp_path, 'rb'))
    stamp = pdf_stamp.getPage(0)

    for i in xrange(pdf_in.getNumPages()):
        page = pdf_in.getPage(i)
        page.mergePage(stamp)
        output.addPage(page)

    with open(output_path, 'wb') as f:
        output.write(f)


def main():
    stamp_pdf('form2.pdf', 'form_letter.pdf', 'stamp.pdf')
    stamp_pdf('form2.pdf', 'form_letter.pdf', 'stamp1.pdf', add_frame=True)
    stamp_pdf('form2.pdf', 'form_letter.pdf', 'stamp3.pdf')
    stamp_pdf('form2.pdf', 'form_letter.pdf', 'stamp4.pdf', add_frame=True)


if __name__ == "__main__":
    main()