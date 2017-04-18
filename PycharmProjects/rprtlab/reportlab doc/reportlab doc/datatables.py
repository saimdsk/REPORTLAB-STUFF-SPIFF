from io import BytesIO
from reportlab.platypus import Table, SimpleDocTemplate
from reportlab.platypus import Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors, pagesizes
from reportlab.lib.textsplit import wordSplit


class DataCell(object):
    """Store Data & other attrs for each Table cell."""

    def __init__(self, table, row, col, data):
        """Initiate the cell.
        table: The DataTable instance this cell belongs to. *
        row, col: Position of this cell in the table. *
        data: A string or something convertible to string. *
        * Required.
        """
        self.table = table
        self.row = row
        self.col = col
        self.data = str(data)

    def get_max_width(self):
        """Return the sum of widths of all columns in parent table."""
        return sum(self.table.widths[:])

    def get_col_width(self):
        """Return the width of the corresponding column"""
        # The total available width is the sum of widths of all columns
        # which are spanned together.
        hspan = self.get_hspan()
        return sum(self.table.widths[self.col: self.col + hspan])

    def get_font(self):
        """Return (font_name, font_size)"""
        return self.table.get_font(self.row, self.col)

    def get_hspan(self):
        """Return the horizontal span"""
        return self.table.get_hspan(self.row, self.col)

    def get_vspan(self):
        """Return the vertical span"""
        return self.table.get_vspan(self.row, self.col)

    def get_align(self):
        """Return the align property"""
        return self.table.get_align(self.row, self.col)

    def get_data(self):
        """Return the word_wrapped data string. 
        Use this for Pdf only. This exists because Reportlab does not enforce 
        wordwrap for table cells.
        """
        font_vals = self.get_font()
        if not font_vals:
            # No font defined for this cell! return the row data
            return self.data
        # Leave a 5% space. We need to accommodate a hyphen(-) also.
        width = int(self.get_col_width() * 95 / 100)
        data = ''.join(self.data.split('\n'))
        lines = wordSplit(data, width, *font_vals)
        return "-\n".join([split[1] for split in lines])


class DataTable(object):
    """Store the data for each Table instance in ReportView"""

    def __init__(self, widths, page_break=False):
        """Initiate the table.
        widths: A list of width of each column in a row. *
        page_break: Insert page_break after table? True/False. Default: False.
        * Required.
        """
        self.widths = widths
        self.page_break = page_break
        self.rows = []
        self.styles = {}

    def get_col_width(self, col):
        """Return the width of given column"""
        return self.widths[col]

    def add_rows(self, rows):
        """A convenience method to add more rows at one go.

        rows: List of iterables each of which represents one row.
        """
        for row in rows:
            self.add_row(row)

    def add_row(self, row):
        """row: An iterable of data-strings representing one row."""
        nrow = len(self.rows)
        self.rows.append([
            DataCell(self, nrow, col, data) for col, data in enumerate(row)
        ])

    def get_rows(self):
        """Return the list of all rows with cells as plain strings.
        Useful to test the content for views with their own tables.
        """
        rows = []
        for row in self.rows:
            rows.append([cell.get_data() for cell in row])
        return rows

    def get_styles(self):
        """Return list of all styles, for the PdfReport."""
        styles = []
        for (s_name, s_vals) in self.styles.items():
            for s_tuple in s_vals:
                style = (s_name,) + s_tuple[:2]
                # The 3rd item, if any, contains all other attrs.
                if len(s_tuple) == 3:
                    style += s_tuple[2]
                styles.append(style)
        return styles

    def add_styles(self, styles):
        """ Just a shortcut to add more styles at one go"""
        for style in styles:
            self.add_style(style)

    def add_style(self, style):
        """
        Accepts & store style in reportlab's table_style format.
        :param style: ('PROPERTY',(c0,r0),(c1,r1),..)
        """
        # Just make sure that property names are all uppercased.
        proprty = style[0].upper()
        start = style[1]
        end = style[2]
        # Rest of the items, if any, are packed into one tuple.
        vals = tuple(style[3:])
        style_tuple = (start, end, vals) if vals else (start, end)
        if proprty in self.styles.keys():
            self.styles[proprty].append(style_tuple)
        else:
            self.styles[proprty] = [style_tuple]

    def convert_col(self, col_index):
        """ Convert -ve column indices"""
        if col_index < 0:
            return len(self.widths) + col_index
        return col_index

    def convert_row(self, row_index):
        """ Convert -ve row indices"""
        if row_index < 0:
            return len(self.rows) + row_index
        return row_index

    ######################################################################
    ## Methods that return style attributes of each cell.
    ## Mostly useful when cell is rendered in HTML or other formats.
    ## Note that we store styles in the order they are added. For each
    ## cell, a property is determined by the last added style.
    ## eg, if 2 font styles are added for the same set of cells, the last
    ## added one will get applied.
    ######################################################################

    def get_align(self, row, col):
        """ Return Value for the align attribute of the given cell"""
        styles = self.styles.get('ALIGN', [])[::-1]
        if not styles:
            return ''
        for (start, end, vals) in styles:
            start = (self.convert_col(start[0]), self.convert_row(start[1]))
            end = (self.convert_col(end[0]), self.convert_row(end[1]))
            if (start[0] <= col <= end[0]) and (start[1] <= row <= end[1]):
                return vals[0]
        return ''

    def get_font(self, row, col):
        """ Return (font_name, font_size) for the given cell"""
        styles = self.styles.get('FONT', [])[::-1]
        if not styles:
            return ()
        for (start, end, vals) in styles:
            start = (self.convert_col(start[0]), self.convert_row(start[1]))
            end = (self.convert_col(end[0]), self.convert_row(end[1]))
            if (start[0] <= col <= end[0]) and (start[1] <= row <= end[1]):
                return vals
        return ()

    def get_hspan(self, row, col):
        """
        :param row, col: Indices of the cell whose hspan is to be found.
        Return 0, 1, or more.
        The starting cell of a span will return the span coverage in the row.
        All following cells in the same row will return 0 and go hiding.
        If a cell does not belong to any horizontal spans, 1 is returned.
        """
        styles = self.styles.get('SPAN', [])[::-1]
        if not styles:
            return 1
        for (start, end) in styles:
            start = (self.convert_col(start[0]), self.convert_row(start[1]))
            end = (self.convert_col(end[0]), self.convert_row(end[1]))
            if start == (col, row) and (end[0] - start[0] > 0):
                # This cell starts a horizontal span. Return the breadth.
                return 1 + end[0] - start[0]
            elif start == (col, row):
                # This cell starts a vertical span with breadth = 1.
                return 1
            elif (start[0] < col <= end[0]) and (start[1] <= row <= end[1]):
                # This cell is inside a span. Go hiding.
                return 0
        return 1

    def get_vspan(self, row, col):
        """
        :param row, col: Indices of the cell whose vspan is to be found.
        Return 0, 1, or more.
        The starting cell of a span will return the span coverage in the col.
        All following cells in the same span will return 0 and go hiding.
        If a cell does not belong to any vertical spans, 1 is returned.
        """
        # The style declaration that comes last gets applied.
        # So reverse the list.
        styles = self.styles.get('SPAN', [])[::-1]
        if not styles:
            return 1
        for (start, end) in styles:
            start = (self.convert_col(start[0]), self.convert_row(start[1]))
            end = (self.convert_col(end[0]), self.convert_row(end[1]))
            if start == (col, row) and (end[1] - start[1] > 0):
                # This cell starts a vertical span. Return the height.
                return 1 + end[1] - start[1]
            elif start == (col, row):
                # This cell starts a horizontal span with height = 1.
                return 1
            elif (start[1] < row <= end[1]) and (start[0] <= col <= end[0]):
                # This cell is inside a span. Hidden.
                return 0
        return 1


class PdfReport(object):
    """A class that generates pdf reports. Rename as ReportView."""

    def __init__(self, title, org_name='', address='', banner=None):
        """Initiate the instance.
        title: A string to be used as the report_title. *
        org_name: Name of the organisation which generates this. Default: ''
        address: Postal-address of the organization. Default: ''
        banner: Banner image of the organization. 
                An image of dimension, 580x60, is preferred. Default: None.
        * Required.
        """
        self.title = title
        self.org_name = org_name
        self.address = address
        self.banner = banner
        self.footer = "%s -- %s -- by ProjectP" % (self.org_name, self.title)
        # TODO: Page dimensions are hardcoded for now.
        (self.page_width, self.page_height) = pagesizes.A4

    def get_first_page(self):
        """Return the function that generates first page of report."""

        def first_page(canvas, doc):
            """self.build_doc will pass this to SimplDocTemplate.build()"""
            canvas.saveState()
            # Page Header Border. Horizontal at y = 100.
            canvas.line(
                0, self.page_height - 100,
                self.page_width, self.page_height - 100
            )
            # Put banner, if given, on top of the header. 580x60 preferred.
            if self.banner:
                canvas.drawImage(
                    self.banner, 1.0, self.page_height - 60, 580, 60
                )
            canvas.setFont("Times-Bold", 16)
            canvas.drawCentredString(
                self.page_width / 2.0, self.page_height - 75, self.org_name
            )
            canvas.setFont("Times-Bold", 12)
            canvas.drawCentredString(
                self.page_width / 2.0, self.page_height - 90, self.address
            )
            # Report title
            canvas.setFont("Times-Bold", 14)
            canvas.drawCentredString(
                self.page_width / 2.0, self.page_height - 115, self.title
            )
            # Page Footer
            canvas.setFont("Helvetica-Bold", 8)
            canvas.drawString(
                .7 * inch, .5 * inch, "Page %d %s" % (doc.page, self.footer)
            )
            canvas.restoreState()

        return first_page

    def get_later_pages(self):
        """Return the function that generates pages other than the first."""

        def later_pages(canvas, doc):
            """self.build_doc will pass this to SimplDocTemplate.build()"""
            canvas.saveState()
            # Page Header Border
            canvas.line(
                0, self.page_height - 55,
                self.page_width, self.page_height - 55
            )
            # Report title
            canvas.setFont("Times-Bold", 14)
            canvas.drawCentredString(
                self.page_width / 2.0, self.page_height - 70, self.title
            )
            # Page Footer
            canvas.setFont("Times-Roman", 9)
            canvas.drawString(
                inch, .75 * inch, "Page %d %s" % (doc.page, self.footer)
            )
            canvas.restoreState()

        return later_pages

    def build_doc(self, tables):
        """Build & return a simple PDF document from tables.
        tables: A list of DataTable instances. *
        * Required.
        """
        # Build a story out of the tables provided.
        common_style = [
            ('INNERGRID', (0, 0), (-1, -1), .25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('FONT', (0, 0), (-1, -1), "Helvetica", 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]
        story = []
        for table in tables:
            data_list = []
            for row in table.rows:
                data_list.append([cell.get_data() for cell in row])
            pdf_table = Table(
                data=data_list, splitByRow=1, repeatRows=1,
                repeatCols=3, colWidths=table.widths
            )
            pdf_table.setStyle(common_style + table.get_styles())
            story += [Spacer(1, 1 * inch), pdf_table]
            if table.page_break:
                story += [PageBreak()]
        if not story:
            story.append(Spacer(1, 1 * inch))
        # Generate & return a PDF from the story
        buff = BytesIO()
        doc = SimpleDocTemplate(buff, pagesize=pagesizes.A4)
        doc.title = self.title
        doc.author = "Report-maker"
        doc.subject = self.title
        doc.build(
            story, onFirstPage=self.get_first_page(),
            onLaterPages=self.get_later_pages()
        )
        doc_pdf = buff.getvalue()
        buff.close()
        return doc_pdf