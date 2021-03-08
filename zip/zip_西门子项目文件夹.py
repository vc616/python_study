# 用everything软件搜索 ".s7p" ,将所有文件的路径复制到字符串s中，本脚本可自动将step7程序的文件夹压缩，并将源文件夹删除
# 可以搜索“.mcp” ,可压缩wincc项目文件文件夹

import zipfile
import os
import re

s = r"""D:\Work_VC\项目备份\其他人员项目移交备份\高满兴\2018\梧州\梧州项目程序2014年10月11日\S0627_Wu\S0627_Wu.s7p
D:\Work_VC\Project_old\W梧州项目\程序\S0627_Wu\S0627_Wu.s7p
D:\Work_VC\Project_old\C长山口\changshankouPLC_DTRO\S7_changshankou\S7_fushu.s7p
D:\Work_VC\Project_old\B碧水源\碧水源黄\碧水源\S7_bishu\S7_bishu\S7_bishu.s7p
D:\Work_VC\项目备份\其他人员项目移交备份\李华东项目备份\完成\石河子\0310石河子上传\S7_weinan 170310\S7_weinan\S7_ningg.s7p
D:\Work_VC\项目备份\其他人员项目移交备份\李华东项目备份\完成\渭南\陈经理0306\渭南程序-13.06.08\渭南程序-13.06.08\S7_weinan\S7_ningg.s7p
D:\Work_VC\Project_old\Q青龙满族自治县垃圾渗滤液处理设备采购及安装项目\调试中……\S7_河北青龙\S7_ningg.s7p"""

# s = r"""D:\Work_VC\项目备份\其他人员项目移交备份\高满兴\201903\抚州\天台项目设备\1\Fz1\Fz1.s7p"""
# zipname = 'G:\VC\Desktop\dawu0603.zip'

s2 = s.split("\n")
import shutil

base_name = r'C:\Users\vm\Desktop'


# shutil.make_archive("A", "zip", root_dir='C:\\Users\\vm\\Desktop\\新建文件夹')
# dir=r'C:\Users\vm\Desktop\WinCC_20190327'


def zipDir(dirpath, p):
    # """
    # 压缩指定文件夹
    # :param dirpath: 目标文件夹路径
    # :param outFullName: 压缩文件保存路径+xxxx.zip
    # :return: 无
    # """
    # print(out.)

    s = dirpath.rfind("\\")
    d1 = dirpath[0:s]
    d2 = "s7_" + dirpath[s + 1:] + "." + p
    zip = zipfile.ZipFile(d1 + "\\" + d2, "w", zipfile.ZIP_DEFLATED)
    print(d1 + "\\" + d2)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            # print((d1+"\\"+filename))
    zip.close()


# zipDir(dir,"zip")
for i in range(len(s2)):
    # print(s2[i])
    dirpath = str(s2[i])

    s = dirpath.rfind("\\")

    d = dirpath[0:s]
    s = d.rfind("\\")
    d1 = d[0:s]
    d2 = d[s + 1:]
    # print(d)
    # print(d1)
    # print(d2)
    zipDir(d, "zip")   #压缩文件夹
    try:               #删除压缩有的文件夹
        shutil.rmtree(d)
    except:
        print(d)
        # pass
    # zip = zipfile.ZipFile(d1 + "\\" + d2, "w", zipfile.ZIP_DEFLATED)
    # zipDir(s2[i], "zip")
