# -*- coding: utf-8 -*-

from generate.util import DbConn
from Gen2PdfService.settings import PERSON_ATTRIBUTE, PERSON_ATTRIBUTE_INDEX, GENERATION_OPTIONS, MAX_ROW_STR, MAX_LINE
from generate.lineBiographyHtmlTemplate import *
from generate.util import createPdf, mergePdf


class LineBiography:
    row_count = 0
    pageNum = 0
    htmlStr = None
    docType = "行传"

    def __init__(self, zp_id):
        self.zpId = zp_id
        self.db = DbConn()
        zp_info = self.db.getZp(self.zpId)[0]
        self.zp_name = zp_info[0]
        self.zp_tag = zp_info[1]

        # 首先获得始祖个人信息
        ancestor = self.db.getAncestor(self.zpId)

        # 初始化html页面
        self.initPage()

        self.fillHTML([[ancestor, None, None]])

        mergePdf(self.zp_name, "行传")

    # 初始化页面，包括页眉和表格
    def initPage(self, exceeded_row=0):
        self.htmlStr = ""
        self.htmlStr += Header
        self.htmlStr += ZpName.format(self.zp_name)
        self.htmlStr += ZpTag.format(self.zp_tag)
        self.htmlStr += TableHeader
        self.row_count = 1
        self.row_count += exceeded_row

    # 填充表格数据
    def fillHTML(self, data):
        while len(data) != 0:
            self.htmlStr += TableGenNum.format(data[0][0][6])
            self.row_count += 1

            new_data = []
            for d in data:
                person_info, children, exceeded_para = self.getRowData(d[0], father_name=d[1], rank=d[2])
                if len(person_info[2]) > 0:
                    if person_info[2][-5:] == '<br/>':
                        person_info[2] = person_info[2][0:-6]
                    self.htmlStr += TableRow.format(person_info[0], person_info[1], person_info[2])

                if len(exceeded_para[0]) > 0:
                    # 生成html
                    self.htmlStr += End
                    createPdf(self.htmlStr, self.zp_name, self.docType, self.pageNum)
                    self.pageNum += 1
                    self.initPage(exceeded_para[1])
                    if len(person_info[2]) > 0:
                        self.htmlStr += TableRow.format(" ", " ", exceeded_para[0])
                    else:
                        self.htmlStr += TableRow.format(person_info[0], person_info[1], exceeded_para[0])
                new_data += children
            data = new_data
        createPdf(self.htmlStr, self.zp_name, self.docType, self.pageNum)

    # 得到表格每一行的数据
    def getRowData(self, data, father_name=None, rank=None):
        """
        :param data: 一个人物的全部信息（同表person_info）
        :param father_name: 父亲名字
        :param rank: 排行
        :return: [1: 该人物简介栏对应信息; 2: 该人物的妻儿信息; 3. 若该人物信息超过当前页面可容纳行数，需要放到下一页的数据]
        """
        person_str = ""
        # 格式例：礼周 长 子
        if father_name is not None:
            if rank == 1:
                rank = "长"
            elif rank == 2:
                rank = "次"
            else:
                rank = str(int(rank) + 1)
            sex = '女'
            if data[5] == '男':
                sex = '子'
            father_str = GENERATION_OPTIONS["father"].format(father_name, rank, sex)
            person_str += father_str
        else:
            father_name = "不详"
        # 字, 号
        if data[3] != '':
            person_str += GENERATION_OPTIONS["zi"].format(data[3])
        if data[4] != '':
            person_str += GENERATION_OPTIONS["hao"].format(data[4])

        children = []
        if data[5] == '男':
            # 妻子信息
            spouse_info = self.db.getFamilyInfo(data[0], int(data[6]), "妻子")
            son_info = self.db.getFamilyInfo(data[0], int(data[6]), "儿子")
            daughter_info = self.db.getFamilyInfo(data[0], int(data[6]), "女儿")

            # 妻子
            if len(spouse_info) != 0:
                spouse_name = ""
                for p in spouse_info:
                    spouse_name += p[2] + "；"
                person_str += GENERATION_OPTIONS["spouse"].format(spouse_name)

            # 儿子
            son_data = []
            if len(son_info) != 0:
                son_name = ""
                for i in range(len(son_info)):
                    son_name += son_info[i][2] + "；"
                    son_data.append([son_info[i], data[2], son_info[i][7]])
                son_str = GENERATION_OPTIONS["son"].format(str(len(son_info)), son_name)
                person_str += son_str

            # 女儿
            daughter_data = []
            if len(daughter_info) != 0:
                daughter_name = ""
                for i in range(len(daughter_info)):
                    daughter_name += daughter_info[i][2] + "；"
                    daughter_data.append([daughter_info[i], data[2], daughter_info[i][7]])
                daughter_str = GENERATION_OPTIONS["daughter"].format(str(len(daughter_info)), daughter_name)
                person_str += daughter_str

            children = son_data + daughter_data

        # 拼接其他信息字段，包括：date_birth，date_dead，education，title_post，desc_living，desc_dead
        other_str = ""
        for index in PERSON_ATTRIBUTE_INDEX:
            if data[index] != '':
                other_str += GENERATION_OPTIONS[PERSON_ATTRIBUTE[index]].format(str(data[index]))
        person_str += other_str

        if person_str[-1:] == '\n':
            person_str = person_str[0:-2]

        # 格式化“简介”栏的字符串
        para, exceeded_para = self.formatString(person_str)
        result = [[father_name, data[2], para], children, exceeded_para]
        return result

    # 格式化“简介”栏字符串
    def formatString(self, original_s):
        formatted_s = ""
        exceeded_s = ""

        exceeded_row = 1

        count = 0
        self.row_count += 1
        for i in original_s:
            if self.row_count <= MAX_LINE:
                if count < MAX_ROW_STR:
                    if i == '\n':
                        if count != 0:
                            formatted_s += '<br/>'
                            self.row_count += 1
                            count = 0
                    else:
                        formatted_s += i
                        count += 1
                else:
                    if i != '\n':
                        formatted_s += '<br/>' + i
                        self.row_count += 1
                        count = 0
            else:
                if count < MAX_ROW_STR:
                    if i == '\n':
                        if count != 0:
                            exceeded_s += '<br/>'
                            exceeded_row += 1
                            count = 0
                    else:
                        exceeded_s += i
                        count += 1
                else:
                    if i != '\n':
                        exceeded_s += '<br/>' + i
                        exceeded_row += 1
                        count = 0

        return [formatted_s, [exceeded_s, exceeded_row]]


if __name__ == '__main__':
    zp = LineBiography(26)
