# -*- coding: utf-8 -*-
import datetime
import os
import shutil
import pdfkit
import psycopg2
from PyPDF2 import PdfFileReader, PdfFileWriter
from Gen2PdfService.settings import PDF_OUTPUT_PATH, LOCAL_DATABASE, LOCAL_HOST, LOCAL_PASSWORD, LOCAL_PORT, LOCAL_USER

resources_path = os.path.abspath('.') + r"/resources"


# 生成pdf
def createPdf(htmlStr, zp_name, docType, pageNum):
    pdf_path = os.path.join(PDF_OUTPUT_PATH, zp_name, docType)

    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)

    filename = "{}-{}.pdf".format(docType, str(pageNum))
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': 'UTF-8',
    }
    path_wk = os.path.join(resources_path, "wkhtmltopdf.exe")  # 安装位置
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    pdfkit.from_string(htmlStr, pdf_path + "/" + filename, options=options, configuration=config)


# 合并
def mergePdf(zp_name, docType):
    pdf_path = os.path.join(PDF_OUTPUT_PATH, zp_name, docType)
    outfile = "{}-{}.pdf".format(zp_name, docType)  # 输出的PDF文件的名称

    file_names = os.listdir(pdf_path)
    files = [os.path.join(pdf_path, "{}-{}.pdf".format(docType, str(i))) for i in range(len(file_names))]

    output = PdfFileWriter()
    o_files = []
    for file in files:
        f = open(file, "rb")
        pdf_page = PdfFileReader(f).getPage(0)
        output.addPage(pdf_page)
        o_files.append(f)

    outputStream = open(os.path.join(PDF_OUTPUT_PATH, zp_name, outfile), "wb")
    output.write(outputStream)
    outputStream.close()

    for o_f in o_files:
        o_f.close()

# 合并行传和吊线图
def mergeHzAndDxt(zp_name):
    timeStr = datetime.datetime.now()
    timeStr = timeStr.strftime("%Y%m%d%H%M%S")
    pdf_path = os.path.join(PDF_OUTPUT_PATH, zp_name)
    dxt_path = os.path.join(pdf_path, zp_name + "-吊线图.pdf")
    hz_path = os.path.join(pdf_path, zp_name+"-行传.pdf")

    o_files = []
    output = PdfFileWriter()
    f = open(dxt_path, "rb")
    dxt = PdfFileReader(f)
    for i in range(dxt.numPages):
        output.addPage(dxt.getPage(i))
    o_files.append(f)

    f = open(hz_path, "rb")
    hz = PdfFileReader(f)
    for i in range(hz.numPages):
        output.addPage(hz.getPage(i))
    o_files.append(f)

    outfile = zp_name + timeStr + ".pdf"
    outputStream = open(os.path.join(PDF_OUTPUT_PATH, zp_name, outfile), "wb")
    output.write(outputStream)
    outputStream.close()

    for o_f in o_files:
        o_f.close()

    filelist = os.listdir(pdf_path)  # 列出该目录下的所有文件名
    for f in filelist:
        if f != outfile:
            filepath = os.path.join(pdf_path, f)  # 将文件名映射成绝对路劲
            if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
                os.remove(filepath)  # 若为文件，则直接删除
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件

    return outfile


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class DbConn:
    def __init__(self):
        self.conn = psycopg2.connect(database=LOCAL_DATABASE, user=LOCAL_USER, password=LOCAL_PASSWORD,
                                     host=LOCAL_HOST, port=LOCAL_PORT)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def getZp(self, zp_id=None):
        if zp_id is not None:
            sql = "select zp_name, tag from zp_info where id = {};".format(zp_id)
        else:
            sql = "select * from zp_info;"
        self.cur.execute(sql)
        zps = self.cur.fetchall()
        return zps

    # 根据族谱id得到族谱始祖，认定只有一位始祖
    def getAncestor(self, zp_id):
        sql = "select * from person_info where zp_id = {0} and father_id='-1';".format(str(zp_id))
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    # 根据父亲ID找到其妻子
    def getFamilyInfo(self, father_id, gen, queryType="妻子"):
        if queryType == "妻子":
            sql = "select * from person_info where father_id = {0} and generation = {1};".format(father_id,
                                                                                                 str(gen))
        elif queryType == "儿子":
            sql = "select * from person_info where father_id = {0} and generation = {1} " \
                  "and sex = '男' order by ranknum;".format(father_id, str(gen + 1))
        else:
            sql = "select * from person_info where father_id = {0} and generation = {1} " \
                  "and sex = '女' order by ranknum;".format(father_id, str(gen + 1))
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result








