from django.shortcuts import HttpResponse

from generate.family_tree import FamilyTree
from generate.line_biography import LineBiography
from generate.util import mergeHzAndDxt
from generate.web2local import web2local


def getPdf(request):
    server_gid = request.GET["gid"]
    server_grpid = request.GET["grpid"]

    # 数据库转换
    zp_id, zp_name = web2local(server_gid, server_grpid)
    print("---数据库转换结束---")
    # 生成
    LineBiography(zp_id)
    print("---行传生成完成---")
    FamilyTree(zp_id)
    print("---吊线图生成完成---")
    pdf_path = mergeHzAndDxt(zp_name)
    print("---合并完成---")
    return HttpResponse(pdf_path)
