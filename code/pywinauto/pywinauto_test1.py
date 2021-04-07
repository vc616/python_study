#!/usr/bin/python2.7
# -*- coding: gbk -*-
# function �Զ������Լ�����
import os.path
import re
import win32con
import codecs
import sys
from pywinauto import Desktop
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import win32clipboard as wc

# �������ı����ʽ
print(sys.getdefaultencoding())
# if sys.getdefaultencoding() != 'gbk':
#     importlib.reload(sys)
#     sys.setdefaultencoding('gbk')

# ����txt�ļ�����·��
txt_path = './TXT/'
if not os.path.exists(txt_path):
    os.mkdir(txt_path)

# ���ÿؼ���Ϣ��txt�ļ���
control_txt_name = txt_path + 'control.txt'

# ���ñ�����Ϣ��txt�ļ�·��
title_txt_file = txt_path + "title.txt"

# ���ü���¼��Ϣ��txt�ļ�·��
record_txt_file = txt_path + "record.txt"

# �������ı����ʽ
# if sys.getdefaultencoding() != 'gbk':
#     importlib.reload(sys)
    # sys.setdefaultencoding('gbk')

# �򿪼�����Ӧ��
app = Application(backend="uia").start("calc.exe")
dlg_spec = Desktop(backend="uia").window(title=u"������", visible_only=False)
dlg_spec.restore()

# ��ӡ�ؼ���Ϣ��ָ��·��
dlg_spec.print_control_identifiers(filename=control_txt_name)

"""

# ��ȡ�ؼ���Ϣtxt�ļ�
fr = open(control_txt_name, "r")
# ����������ʽ��������ȡbutton�ؼ���title
par = r'.+title=\"([^,]+)\".+\"Button\"'
content = []
for line in fr.readlines():
    res = re.compile(par).findall(line)
    if res:
        result = str(res[0]).split(',')
        par_str = str(result[0])
        content.append(par_str)
    else:
        pass
fr.close()
print("content:",content)
# ����ȡ������Ϣ���Ϊ����txt�ļ�
fw = codecs.open(title_txt_file, "w", 'gbk')
for i in range(0, len(content)):
    # ʹ���б��Ƶ�ʽ���б��еĵ���Ԫ��ȫ��ת��Ϊstr����
    new_content_line = [str(i) for i in content[i]]
    # ���б��е�Ԫ�ط��ڿմ��У�Ԫ�ؼ��ÿո����
    new_content_lines = ''.join(new_content_line)
    # �������ַ��滻Ϊ���ַ�
    new_content_lines = re.sub(r'\'', "", new_content_lines)
    # ȥ������
    if new_content_lines == '':
        pass
    else:
        # fw.write(new_content_lines + '\n')
        fw.write((new_content_lines + '\n').encode('gbk'))

fw.close()
"""
# ��� record_txt_file�ļ�����
fw_record = codecs.open(record_txt_file, "a", 'gbk')
fw_record.seek(0)
fw_record.truncate()
# �Զ������ԡ�һλ�����˷���(10������������ˣ���10*10=100�����)

for i in range(1, 10):
    for j in range(1, 10):
        real_value = i * j
        # dlg_spec.window(title=str(i), control_type="Button").draw_outline(colour="red", thickness=3)
        dlg_spec.window(title=str(i), control_type="Button").click()
        # dlg_spec.window(title="��", control_type="Button").draw_outline(colour="red", thickness=3)
        dlg_spec.window(title="��", control_type="Button").click()
        # dlg_spec.window(title=str(j), control_type="Button").draw_outline(colour="red", thickness=3)
        dlg_spec.window(title=str(j), control_type="Button").click()
        # dlg_spec.window(title="����", control_type="Button").draw_outline(colour="red", thickness=3)
        dlg_spec.window(title="����", control_type="Button").click()

        # ѡ�н����
        # dlg_spec.window(title="���").draw_outline(colour="red", thickness=3)
        # ��������
        send_keys("^c")
        # �򿪼�����
        wc.OpenClipboard()
        # ��ȡ����������
        copy_text = wc.GetClipboardData(win32con.CF_TEXT)
        # �رռ�����
        wc.CloseClipboard()
        # ��ȡ������
        calc_value = copy_text.decode().strip('\0')
        # �жϼ�����������
        if calc_value == str(real_value):
            record = "%d��%d=%s ����ȷ��" % (i, j, calc_value)
            print(record)
        else:
            record = "%d��%d=%s ������" % (i, j, calc_value)
            print(record)
        # �������Ϣ���Ϊ��־txt�ļ�
        fw_record = codecs.open(record_txt_file, "a", 'gbk')
        fw_record.write((record + '\n').encode('gbk'))
fw_record.close()