# -*- coding: utf-8 -*-

from Gen2PdfService.settings import MAX_LINE_TREE
from generate.familyTreeHtmlTemplate import *
from generate.util import DbConn
from generate.util import createPdf, mergePdf


class PersonWithFlag:
    def __init__(self, info, flag):
        """
        :param info: 个人信息 list:[id, name, generation]
        :param flag: 选择背景图的标识 list:[是否有孩子,是否是第一个孩子, 是否是最后一个孩子]
        """
        self.personInfo = info
        self.flag = flag


class FamilyTree(object):
    def __init__(self, zp_id):
        self.docType = "吊线图"
        self.zpId = zp_id
        self.db = DbConn()
        zp_info = self.db.getZp(self.zpId)[0]
        self.zp_name = zp_info[0]
        self.zp_tag = zp_info[1]

        self.tableData = []

        # 首先获得始祖个人信息
        ancestor = self.db.getAncestor(self.zpId)
        self.cur_gen = int(ancestor[6])
        ancestorWithFlag = PersonWithFlag([ancestor[0], ancestor[2], ancestor[6]], [0, 0, 0])
        self.currGen = [ancestorWithFlag]
        self.nextGen = []
        while len(self.currGen) > 0:
            self.tableData.append(["{}世".format(str(i)) for i in range(self.cur_gen, self.cur_gen + 5)])
            self.fillTableData(self.currGen, [["", [0]*3]]*5)
            self.currGen = self.nextGen
            self.nextGen = []
            self.cur_gen += 4
        self.formatTableData()
        self.genFamilyTree()

    # 填充表格数据
    def fillTableData(self, personL, path, depth=0):
        if depth < 5:
            for person in personL:
                son_info = self.db.getFamilyInfo(person.personInfo[0], int(person.personInfo[2]), "儿子")
                if len(son_info) > 0:
                    person.flag[0] = 1
                # path[depth] = NameWithFlag(person.personInfo[1], person.flag)
                path[depth] = [person.personInfo[1], person.flag.copy()]

                for i in range(depth + 1, 5):
                    path[i] = ["", path[i][1].copy()]

                son = []
                if len(son_info) > 0:
                    for i in range(len(son_info)):
                        personInfo = [son_info[i][0], son_info[i][2], son_info[i][6]]
                        if len(son_info) == 1:
                            flag = [0, 1, 1]
                        else:
                            if i == 0:
                                flag = [0, 1, 0]
                            elif i == len(son_info)-1:
                                flag = [0, 0, 1]
                            else:
                                flag = [0, 0, 0]
                        son.append(PersonWithFlag(personInfo, flag))
                    self.fillTableData(son, path, depth+1)
                    if depth == 4:
                        print(path)
                        self.tableData.append(path.copy())
                        if len(son_info) > 0:
                            self.nextGen.append(person)
                else:
                    print(path)
                    self.tableData.append(path.copy())

    # 格式化表格数据
    def formatTableData(self):
        last = [""]*5
        for i in range(len(self.tableData)):
            data = self.tableData[i]
            if isinstance(data[0], str):  # 第几世
                last = data.copy()
                tr = TableGenNum.format(data[0], data[1], data[2], data[3], data[4])
            else:
                td = ""
                for j in range(len(data)):
                    name = data[j][0]
                    flag = data[j][1]
                    if j == 0:  # 第一列, 肯定是有孩子的
                        if name == last[j]:  # 与上一行相同
                            td_temp = TdWithoutBg.format(" ")
                        else:
                            bg_temp = BKbg
                            td_temp = TdWithBg.format(bg_temp, name)
                            last[j] = name
                        td += td_temp
                    elif j == 4:  # 第五列，肯定与上一行不同，也不用判断是否有孩子,
                        if name == "":  # 没有值
                            td_temp = TdWithoutBg.format(" ")
                        else:
                            if flag[1] == 1 and flag[2] == 1:  # 既是第一个孩子又是最后一个孩子
                                bg_temp = BKbg6
                            elif flag[1] == 1:  # 第一个孩子
                                bg_temp = BKbg2
                            elif flag[2] == 1:  # 最后一个孩子
                                bg_temp = BKbg4
                            else:
                                bg_temp = BKbg9
                            td_temp = TdWithBg.format(bg_temp, name)
                        last[j] = name
                        td += td_temp
                    else:  # 中间列
                        if name == "":  # 没有值
                            td_temp = TdWithoutBg.format(name)
                            last[j] = name
                        else:
                            if name == last[j]:  # 与上一行相同
                                if flag[2] == 1:  # 最后一个孩子
                                    td_temp = TdWithoutBg.format(" ")
                                else:
                                    bg_temp = BKbg3
                                    td_temp = TdWithBg.format(bg_temp, " ")
                            else:
                                if flag[1] == 1 and flag[2] == 1:  # 既是第一个孩子又是最后一个孩子
                                    if flag[0] == 1:  # 有孩子
                                        bg_temp = BKbg8
                                    else:
                                        bg_temp = BKbg6
                                elif flag[1] == 1:  # 第一个孩子
                                    if flag[0] == 1:  # 有孩子
                                        bg_temp = BKbg1
                                    else:
                                        bg_temp = BKbg2
                                elif flag[2] == 1:  # 最后一个孩子
                                    if flag[0] == 1:  # 有孩子
                                        bg_temp = BKbg7
                                    else:
                                        bg_temp = BKbg4
                                else:
                                    if flag[0] == 1:  # 有孩子
                                        bg_temp = BKbg5
                                    else:
                                        bg_temp = BKbg9
                                td_temp = TdWithBg.format(bg_temp, name)
                                last[j] = name
                        td += td_temp
                tr = TR.format(td)
            self.tableData[i] = tr

    # 生成吊线图pdf
    def genFamilyTree(self):
        zpNameStr = ZpName.format(self.zp_name)
        zpTagStr = ZpTag.format(self.zp_tag)

        tableList = []
        tableStr = ""

        lastGenNumRow = ""

        cur_row_count = 0
        for i in range(len(self.tableData)):
            data = self.tableData[i]
            if "tdGen" in data:
                lastGenNumRow = data

            if cur_row_count == 0:
                if "tdGen" not in data:
                    tableStr += lastGenNumRow
                    tableStr += data
                    cur_row_count += 2
            elif cur_row_count < MAX_LINE_TREE:
                tableStr += data
                cur_row_count += 1
            elif cur_row_count == MAX_LINE_TREE-1:
                if "tdGen" in data:  # 最后一行不允许是世代数
                    tableList.append(tableStr)
                    tableStr = data
                    cur_row_count = 1
                else:
                    tableStr += data
                    cur_row_count += 1
            else:
                tableList.append(tableStr)
                if "tdGen" not in data:
                    tableStr = lastGenNumRow + data
                    cur_row_count = 2
                else:
                    tableStr = data
                    cur_row_count = 1
            if i == len(self.tableData)-1:
                tableList.append(tableStr)

        if len(tableList) % 2 != 0:
            tableList.append(" ")

        count = 0
        while count < len(tableList):
            divMainStr = DivMain.format(tableList[count], tableList[count+1])
            htmlStr = r"{}".format(BodyFront + zpNameStr + zpTagStr + divMainStr + BodyEnd)
            # print(htmlStr)
            # with open("html{}.html".format(str(int(count/2))), 'w', encoding='utf-8') as f:
            #     f.write(htmlStr)
            # f.close()
            createPdf(htmlStr, self.zp_name, self.docType, int(count/2))
            count += 2

        mergePdf(self.zp_name, self.docType)


if __name__ == '__main__':
    FamilyTree(1)
