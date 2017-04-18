import os
from printing import MyPrint
from io import BytesIO



buffer = BytesIO()

report = MyPrint('test.pdf', 'Letter')
pdf = report.print_users()



