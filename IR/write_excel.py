import xlwt, xlrd
from xlutils.copy import copy

class xml_writer(object):
    def __init__(self):
        # 创建一个Workbook对象，这就相当于创建了一个Excel文件
        self.book = None
        '''
        Workbook类初始化时有encoding和style_compression参数
        encoding:设置字符编码，一般要这样设置：w = Workbook(encoding='utf-8')，就可以在excel中输出中文了。
        默认是ascii。当然要记得在文件头部添加：
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        style_compression:表示是否压缩，不常用。
        '''
        self.sheet = None

    def open_xml_file(self, url=None):
        if url:
            xlsfile = url# 打开指定路径中的xls文件
            self.book = xlrd.open_workbook(xlsfile)#得到Excel文件的book对象，实例化对象
            self.sheet = self.book.sheet_by_index(0) # 通过sheet索引获得sheet对象
            rb = self.book.sheet_by_index(0)
 
            self.book = copy(rb)
            
            #通过get_sheet()获取的sheet有write()方法
            self.sheet = self.book.get_sheet(0)
            
            self.book.save('m:\\1.xls')
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet('test', cell_overwrite_ok=True)

    def write_xml_file(self, write_fun):
        write_fun(self.sheet)