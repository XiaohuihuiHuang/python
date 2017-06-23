# -*- coding:utf-8 -*-
# !/usr/bin/python2.7
# author: xiaohuihui

import cookielib
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import sys


'''To prevent the Chinese error'''
reload(sys)
sys.setdefaultencoding("gbk")


'''login'''
def login():
    try:
        '''get login viewstate'''
        login_url = 'http://jwc1.wtc.edu.cn/default3.aspx'
        login_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}

        view = urllib2.urlopen(urllib2.Request(login_url, headers=login_headers)).read()
        soup = BeautifulSoup(view, "html.parser")
        tmp = soup.find('input', attrs={'name': '__VIEWSTATE'})
        viewstate = tmp['value']

        '''get login values'''
        StudentNo = raw_input("输入你的学号:")
        PassWord = raw_input("请输入你的密码:")

        login_data = urllib.urlencode({
            "__VIEWSTATE": viewstate,
            "TextBox1": StudentNo,
            "TextBox2": PassWord,
            "ddl_js": u'学生',
            "Button1": "+%B5%C7+%C2%BC+"
        })

        '''make a handler = opener
        request = urllib2.Request(login_url,login_data,login_headers)
        result = opener.open(request)
        两种登录的方法下面那种方法需要使用 "opener.addheaders" 修改http头
        '''
        mycookie = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie))

        '''login and get cookie'''
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0')]
        result = opener.open(login_url, login_data)

        '''find error'''
        soup = BeautifulSoup(result.read(), "html.parser")
        error = soup.find_all('script')
        source = error[0].get_text().encode("utf-8")

        PassWord_error = "密码错误！！"
        PassWord_tmp = source.find(PassWord_error)
        StudentNo_error = "用户名不存在或未按照要求参加教学活动！！"
        StudentNo_tmp = source.find(StudentNo_error)

        try:
            if PassWord_tmp != -1:
                sys.exit(0)
        except:
            print PassWord_error
            print "请重新",
            main()

        try:
            if StudentNo_tmp != -1:
                sys.exit(0)
        except:
            print StudentNo_error
            print "请重新",
            main()

        '''get StudentName'''
        xs_main_url = "http://jwc1.wtc.edu.cn/xs_main.aspx?xh=" + StudentNo
        xs_main = opener.open(xs_main_url)
        soup = BeautifulSoup(xs_main.read(), "html.parser")
        tmp = soup.find(id="xhxm")
        StudentName = str(tmp.string.decode('gbk')[:-2])

        result_url = "http://jwc1.wtc.edu.cn/xscj_gc.aspx?xh=" + StudentNo + "&xm=" + StudentName + "&gnmkdm=N121605"
        viewstate_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
            'Referer': xs_main_url,
        }
        result_headers = {
            'Referer': result_url,
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }

        '''get result viewstate'''
        request_gra1 = urllib2.Request(result_url, headers=viewstate_headers)
        result = opener.open(request_gra1)
        soup = BeautifulSoup(result.read(), "html.parser")
        tmp = soup.find('input', attrs={'name': '__VIEWSTATE'})
        viewstate = tmp['value']

        '''get Inquiry mode'''
        Inquiry_mode = raw_input("请选择按学年(1)还是学期(2)查询输入1或2:")
        if Inquiry_mode == '1':
            Inquiry_mode = '1'
            Button = 'Button5'
            Value = '按学年查询'
            Semester = ''
        elif Inquiry_mode == '2':
            Inquiry_mode = '2'
            Semester = raw_input("请输入第几学期(1或2):")
            Button = 'Button1'
            Value = '按学期查询'
        else:
            print "请键入1或2"
            main()
        Interval = raw_input("请输入学年区间例(2015-2016):")

        result_data = urllib.urlencode({
            '__VIEWSTATE': viewstate,
            'ddlXN': Interval,
            'ddlXQ': Semester,
            Button: Value
        })

        '''login and get result then return'''
        result = urllib2.Request(result_url, result_data, result_headers)
        result = opener.open(result)
        return result.read()
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            return e.code


'''Processing result'''
def getResult():
    pageCode = login()
    soup = BeautifulSoup(pageCode, 'html.parser')
    table = soup.find("table", class_="datelist")
    trs = table.find("tr")
    tds = trs.find_all("td")

    for i in range(len(tds)):
        if i == 0 or i == 1 or i == 3 or i == 4 or i == 6 or i == 7 or i == 8:
            print tds[i].string.decode("gbk"), ' ',
    print '\n'

    trs = table.find_all("tr")
    for i in range(len(trs)):
        if i > 0:
            tds = trs[i].find_all("td")
            for j in range(len(tds)):
                if j == 0 or j == 1 or j == 3 or j == 4 or j == 6 or j == 7 or j == 8:
                    print tds[j].string.decode("gbk"), ' ',
            print '\n'


'''main()'''
def main():
    sure = '1'
    while sure == '1':
        getResult()
        sure = raw_input('继续请键入1退出请按回车：')
    else:
        print "Thank's for your use!"
        os._exit(0)


if __name__ == '__main__':
    main()