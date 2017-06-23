# -*- coding: utf-8 -*-

# Created by: xiaohuihui
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import urllib
import urllib2
import BeautifulSoup
import cookielib
from bs4 import BeautifulSoup
import os

reload(sys)
sys.setdefaultencoding("gbk")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class GetGrade(QtGui.QWidget):
    def __init__(self):
        super(GetGrade, self).__init__()

        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        self.login_url = 'http://jwc1.wtc.edu.cn/default3.aspx'
        self.xs_main_url = "http://jwc1.wtc.edu.cn/xs_main.aspx?xh="
        self.result_url = "http://jwc1.wtc.edu.cn/xscj_gc.aspx?xh="
        self.PassWord_error = "密码错误！！"
        self.StudentNo_error = "用户名不存在或未按照要求参加教学活动！！"
        self.setupUi()

    def setupUi(self):

        '''创建组件'''
        self.studNo = QtGui.QLabel(u'学号')
        self.Passwd = QtGui.QLabel(u'密码')
        self.Xn = QtGui.QLabel(u'学年')
        self.Xq = QtGui.QLabel(u'学期')
        self.Clear = QtGui.QPushButton(u'清空重添')
        self.Button5 = QtGui.QPushButton(u'按学年查询')
        self.Button1 = QtGui.QPushButton(u'按学期查询')
        self.Initialize = QtGui.QPushButton(u'初始化')
        self.xq1 = QtGui.QRadioButton(u'第一学期')
        self.xq2 = QtGui.QRadioButton(u'第二学期')
        self.Views = QtGui.QTableView()
        self.Stno = QtGui.QLineEdit()
        self.Stno.setText(u"150330****")
        self.Pwd = QtGui.QLineEdit()
        self.Pwd.setText(u"123456")
        self.Pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.year_end_box = QtGui.QComboBox()
        self.year_end_box.addItem(_fromUtf8("2008-2009"))
        self.year_end_box.addItem(_fromUtf8("2009-2010"))
        self.year_end_box.addItem(_fromUtf8("2010-2011"))
        self.year_end_box.addItem(_fromUtf8("2011-2012"))
        self.year_end_box.addItem(_fromUtf8("2012-2013"))
        self.year_end_box.addItem(_fromUtf8("2013-2014"))
        self.year_end_box.addItem(_fromUtf8("2014-2015"))
        self.year_end_box.addItem(_fromUtf8("2015-2016"))
        self.year_end_box.addItem(_fromUtf8("2016-2017"))
        self.year_end_box.addItem(_fromUtf8("2017-2018"))
        self.year_end_box.addItem(_fromUtf8("2018-2019"))
        self.model = QtGui.QStandardItemModel()
        # self.model.setHorizontalHeaderLabels([u'学年', u'学期', '', u'课程名称', u'课程性质', '', u'学分', u'绩点', u'成绩'])

        '''创建布局'''
        self.Xq_box = QtGui.QHBoxLayout()
        self.Xq_box.addWidget(self.xq1)
        self.Xq_box.addWidget(self.xq2)
        self.Layout = QtGui.QGridLayout()
        self.Layout.addWidget(self.studNo, 0, 0, 1, 1)
        self.Layout.addWidget(self.Stno, 0, 1, 1, 1)
        self.Layout.addWidget(self.Clear, 0, 2, 1, 1)
        self.Layout.addWidget(self.Passwd, 1, 0, 1, 1)
        self.Layout.addWidget(self.Pwd, 1, 1, 1, 1)
        self.Layout.addWidget(self.Button5, 1, 2, 1, 1)
        self.Layout.addWidget(self.Xn, 2, 0, 1, 1)
        self.Layout.addWidget(self.year_end_box, 2, 1, 1, 1)
        self.Layout.addWidget(self.Button1, 2, 2, 1, 1)
        self.Layout.addWidget(self.Xq, 3, 0, 1, 1)
        self.Layout.addLayout(self.Xq_box, 3, 1, 1, 1)
        self.Layout.addWidget(self.Initialize, 3, 2, 1, 1)
        self.Layout.addWidget(self.Views, 4, 0, 1, 3)

        '''信号/槽'''
        self.Clear.clicked.connect(self.Stno.clear)
        self.Clear.clicked.connect(self.Pwd.clear)
        self.Initialize.clicked.connect(self.remove)
        self.Button1.clicked.connect(self.ln)
        self.Button5.clicked.connect(self.ln)
        self.xq1.clicked.connect(self.xq_0)
        self.xq2.clicked.connect(self.xq_0)

        self.setWindowTitle(u"查成绩3.0-by:小辉辉")
        self.setLayout(self.Layout)
        self.setGeometry(10, 30, 711, 391)
        self.show()

    def remove(self):
        self.model.clear()  # 清楚所有表项及表头

    def ln(self):
        self.model.clear()  # http://blog.sina.com.cn/s/blog_4b5039210100h6rn.html
        grade = self.getResult()
        if grade == self.StudentNo_error:
            self.model.setItem(0, 0, QtGui.QStandardItem(self.StudentNo_error.decode("utf-8")))
            self.Views.setModel(self.model)
        elif grade == self.PassWord_error:
            self.model.setItem(0, 0, QtGui.QStandardItem(self.PassWord_error.decode("utf-8")))
            self.Views.setModel(self.model)
        else:
            pass

    def xq_0(self):
        if self.xq2.isChecked():
            semester = '2'
            return semester
        else:
            semester = '1'
            return semester

    def button(self):
        source = self.sender()
        if source == self.Button1:
            return {'Button': 'Button1', 'value': '按学期查询', 'semester': self.xq_0()}
        elif source == self.Button5:
            return {'Button': 'Button5', 'value': '按学年查询', 'semester': ''}
        else:
            pass

    def login(self):
        box = self.button()
        studentNo = self.Stno.text()
        passWord = self.Pwd.text()
        year_end = self.year_end_box.currentText()

        '''get login viewstate'''
        viewstate_view = urllib2.urlopen(urllib2.Request(self.login_url, headers=self.login_headers)).read()
        viewstate_soup = BeautifulSoup(viewstate_view, "html.parser")
        viewstate_tmp = viewstate_soup.find('input', attrs={'name': '__VIEWSTATE'})
        login_viewstate = viewstate_tmp['value']

        login_data = urllib.urlencode({
            "__VIEWSTATE": login_viewstate,
            "TextBox1": studentNo,
            "TextBox2": passWord,
            "ddl_js": u'学生',
            "Button1": '+%B5%C7+%C2%BC+'
        })

        '''make a handler = opener'''
        mycookie = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie))

        '''login and get cookie'''
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0')]
        login_result = opener.open(self.login_url, login_data)

        '''find error'''
        login_soup = BeautifulSoup(login_result.read(), "html.parser")
        error = login_soup.find_all('script')
        error_source = error[0].get_text().encode("utf-8")
        PassWord_tmp = error_source.find(self.PassWord_error)
        StudentNo_tmp = error_source.find(self.StudentNo_error)
        try:
            if PassWord_tmp != -1:
                sys.exit(0)
        except:
            return self.PassWord_error
        if StudentNo_tmp != -1:
            return self.StudentNo_error

        '''get StudentName'''
        xs_main_url = self.xs_main_url + str(studentNo)
        xs_main_result = urllib2.Request(xs_main_url)
        xs_main = opener.open(xs_main_result)
        soup = BeautifulSoup(xs_main.read(), "html.parser")
        tmp = soup.find(id="xhxm")
        StudentName = str(tmp.string.decode('gbk')[:-2])

        result_url = self.result_url + str(studentNo) + "&xm=" + StudentName + "&gnmkdm=N121605"
        '''str(StudentNo)https://stackoverflow.com/questions/7748172/qstring-object-has-no-attribute-strip'''
        viewstate_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
            'Referer': self.xs_main_url,
        }
        result_headers = {
            'Referer': self.result_url,
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }

        '''get result viewstate'''
        viewstate_request = urllib2.Request(result_url, headers=viewstate_headers)
        viewstate_result = opener.open(viewstate_request)
        soup = BeautifulSoup(viewstate_result.read(), "html.parser")
        viewstate_tmp = soup.find('input', attrs={'name': '__VIEWSTATE'})
        result_viewstate = viewstate_tmp['value']
        result_data = urllib.urlencode({
            '__VIEWSTATE': result_viewstate,
            'ddlXN': year_end,
            'ddlXQ': box['semester'],
            box['Button']: box['value']
        })

        '''login and get result then return'''
        result = urllib2.Request(result_url, result_data, result_headers)
        result = opener.open(result)
        return result.read()

    def getResult(self):
        pageCode = self.login()
        if pageCode == self.PassWord_error:
            return self.PassWord_error
        elif pageCode == self.StudentNo_error:
            return self.StudentNo_error
        else:
            soup = BeautifulSoup(pageCode, 'html.parser')
            table = soup.find("table", class_="datelist")
            trs = table.find_all("tr")
            for i in range(len(trs)):
                if i >= 0:
                    tds = trs[i].find_all("td")
                    for j in range(len(tds)):
                        if j == 0 or j == 1 or j == 2 or j == 3 or j == 4 or j == 6 or j == 7 or j == 8:
                            item = QtGui.QStandardItem(tds[j].string.decode("gbk"))
                            self.model.setItem(i, j, item)

            self.Views.setModel(self.model)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = GetGrade()
    sys.exit(app.exec_())
