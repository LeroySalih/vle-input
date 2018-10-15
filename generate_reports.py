html = """
<img src="bisak_logo.png" height="120" width="550"></img>

<h1>Heros Of Computing - Leroy Salih</h1>
<h2>Level: 4A</h2>

<p>Detailed Feedback.</p>
 
<table border="0" align="left" width="75%">
<thead>
  <tr>
    <th width="60%" align="left">Name</th>
    <th width="20%">Evidenced</th>
    <th width="20%">Not Evidenced</th>
  </tr>
</thead>
<tbody>
{0}
</tbody>
</table>
"""
 
from fpdf import FPDF, HTMLMixin
 
class MyFPDF(FPDF, HTMLMixin):
    pass
 
pdf=MyFPDF()
#First page
pdf.add_page()
rows =  """ 
  <tr>
    <td>Evidence Item 11</td>
    <td align="center">X</td>
    <td align="center"></td>
  </tr>
"""



pdf.write_html(html.format(rows))
pdf.add_page()
pdf.write_html(html.format(rows))


pdf.output('html.pdf','F')