# -*- coding: utf-8 -*-

from Gen2PdfService.settings import IMAGE_PATH

image_path = "file:///{}".format(IMAGE_PATH)

BodyFront = """
<html>
<head>
<meta charset="utf-8" />
<style type="text/css">
.main{
    width:800px;
    margin: 0 auto;
    text-align:center;
}
.tableOuter{
    font-size:15px;
    border-collapse: collapse;
    margin: auto;
    cellpadding:0px;
    cellspacing:0px;
}

.tableInner{
    font-size:15px;
    width:350px;
    border-collapse: collapse;
    margin: auto;
    cellpadding:0px;
    cellspacing:0px;
}

.tdGen{
    font-weight:bold;
    height:40px;
    background-color: #000;
    color:#FFF;
    height:20px;
    vertical-align:middle;
}

table td{
    border:solid 0px #FFF;
    padding:0px;
    width:70px;
    height:40px;
    text-align:center;
    vertical-align:top;
}
</style>
</head>
<body>
"""

BodyEnd = """
</body>
</html>
"""

ZpName = """
<h2 align="center">{}</h2>
"""

ZpTag = """
<h3 align="right">· {} ·</h3>
<hr style="width:750px;height:1px;border:solid 1px #000;background-color:#000"/>
"""

DivMain = """
<div class="main">
<table class="tableOuter">
<tr>
<td>
<table class="tableInner">
{0}
</table>
</td>
<td style="width:20px;"><hr style="width:1px;height:100%;border:solid 0px #000;background-color:#000"/></td>
<td>
<table class="tableInner">
{1}
</table>
</td>
</tr>
</div>
"""

TableGenNum = """
<tr><td class="tdGen">{0}</td><td class="tdGen">{1}</td><td class="tdGen">{2}</td><td class="tdGen">{3}</td>
<td class="tdGen">{4}</td></tr>
"""

BKbg = """
style="background-image:url({}/BKbg.gif);"
""".format(image_path)

BKbg1 = """
style="background-image:url({}/BKbg1.gif);"
""".format(image_path)

BKbg2 = """
style="background-image:url({}/BKbg2.gif);"
""".format(image_path)

BKbg3 = """
style="background-image:url({}/BKbg3.gif);"
""".format(image_path)

BKbg4 = """
style="background-image:url({}/BKbg4.gif);"
""".format(image_path)

BKbg5 = """
style="background-image:url({}/BKbg5.gif);"
""".format(image_path)

BKbg6 = """
style="background-image:url({}/BKbg6.gif);"
""".format(image_path)

BKbg7 = """
style="background-image:url({}/BKbg7.gif);"
""".format(image_path)

BKbg8 = """
style="background-image:url({}/BKbg8.gif);"
""".format(image_path)

BKbg9 = """
style="background-image:url({}/BKbg9.gif);"
""".format(image_path)

TR = """
<tr>{}</tr>
"""

TdWithBg = """
<td {0}>{1}</td>
"""

TdWithoutBg = """
<td>{}</td>
"""
