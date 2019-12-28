# -*- coding: utf-8 -*-

Header = """
<html>
<head>
<meta charset="utf-8" />
<style type="text/css">
body{
    text-align:center
} 
div{
    text-align:center;
    border:solid 2px #000;
    margin:0 auto;
    padding:1px;
    width:600px;
}
.tblHeader{
    /* 表格表头*/
    text-align:center;
    font-weight:bold;
}

.col1{
    /* 第一列*/
    width:15%;
    vertical-align:text-top;
    text-align:center;
}

.col2{
    /* 第二列*/
    width:15%;
    text-align:center;
    vertical-align:text-top;
    font-weight:bold;
}

.col3{
    /* 第三列*/
    width:70%;
}

.geneNum{
    /* 世代头 */
}

table{
    border:solid 1px #000;
    font-size:15px;
    width:100%;
    border-collapse: collapse;
    margin: auto;
    cellpadding:0px;
    cellspacing:0px;
}

table td{
    padding-left:0;
    border:solid 1px #000;
    padding:0px;
    line-height:20px;
    overflow:hidden;
}
</style>
</head>
<body>
"""

ZpName = """
<h2 align="center">{}</h2>
"""

ZpTag = """
<h3 align="right">· {} ·</h3>
<hr />
"""

TableHeader = """
<div>
<table>
<tr><td class="tblHeader">父亲谱名</td><td class="tblHeader">本世派名</td><td class="tblHeader">简介</td></tr>
"""

TableGenNum = """
<tr><td colspan="3" style="text-align:center;">第{}世</td></tr>
"""

TableRow = """
<tr><td class="col1">{}</td><td class="col2">{}</td><td class="col3">{}</td></tr>
"""

End = """
</table>
</div>
</body>
</html>
"""
