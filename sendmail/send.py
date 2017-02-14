# -*- coding: utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
import os
import os.path  
import mimetypes
import getopt
import sys


"""
不支持群发，批量单对单发邮件
只支持单个附件
"""

reload(sys)
sys.setdefaultencoding( "utf-8" )


class Single_Send(object):
    
    from_addr = "username@163.com" #发件地址
    password = "password"  #邮箱密码
    false_list = []

    def __init__(self, to_addr, smtp_server, smtp_port, content, title, fake_addr = "", attach=""):#
        self.fake_addr = fake_addr
        self.to_addr = to_addr
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.content = content
        self.attach = attach
        self.title = title

    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))
        
    def get_msg(self):
    #设置 伪造发件地址／收件地址／邮件标题
        msg = MIMEMultipart()

        if self.fake_addr == "":
            msg['From'] = self._format_addr(u"%s" % self.from_addr)
        else: 
            msg['From'] = self._format_addr(self.fake_addr)

        msg['To'] = self._format_addr(u'%s <%s>' % (self.to_addr, self.to_addr))
        msg['Subject'] = Header(u'%s' % self.title, 'utf-8').encode()

    #设置邮件内容，支持html和文本格式
        filename = os.path.basename(self.content)
        filetype = os.path.splitext(filename)[-1]
        with open(self.content,'r') as crf:
            mail_c = crf.read()
        try:
            if filetype == '.txt':   
                msg.attach(MIMEText(mail_c, 'plain', 'utf-8'))
            if filetype == '.html':
                msg.attach(MIMEText(mail_c, 'html', 'utf-8'))
        except Exception as e:
            print "错误：邮件内容只支持html和文本格式, %s" % e

    #设置邮件附件
        if self.attach == "":
            pass
        else:
            with open(self.attach, 'rb') as arf:
                ctype,encoding = mimetypes.guess_type(self.attach)  
                if ctype is None or encoding is not None:  
                    ctype = 'application/octet-stream'  
                maintype,subtype = ctype.split('/',1)  
                file_msg = MIMEBase(maintype, subtype)  
                file_msg.set_payload(arf.read())
                encoders.encode_base64(file_msg)
                ## 设置附件头
                basename = os.path.basename(self.attach)  
                file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头  
                msg.attach(file_msg) 
        
        return msg

    def send_msg(self):
    #发送邮件
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)  #设置smtp服务器
        server.starttls()                              #smtp加密 
        # server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr], self.get_msg().as_string())
            print "     *＾.＾* 成功发送给了%s" % self.to_addr
            server.quit()
        except Exception as e:
            print """     ╮(╯_╰)╭ 发送失败：%s, 
            >>原因：%s""" % (self.to_addr,e)
            self.false_list.append(to_addr)
            pass


def tolist(path=''):  
    to_addr = []
    with open(path,'r') as rf:
        for i in rf:
            to_addr.append(i.strip())
    return to_addr

def inputinfo():
    helpinfo = """
    #########################################################################################
    usage:
        伪造发件地址  如 xiaoming<xiaoming@123.com>（可不设置）
        目标邮箱列表  如 list.txt
        smtp服务器    如 smtp.163.com:25, smtp.qq.com:587
        邮件标题信息  如 hacking by black3y
        邮件内容信息  如 content/ahtml.html (支持html和文本格式)
        邮件附件文件  如 attach/test.jpg（可不设置）

    友情提示:
        smtp服务器对应表
            雅虎邮箱           smtp.mail.yahoo.com:465             smtp.mail.yahoo.com:587
            谷歌邮箱           smtp.gmail.com:465                  smtp.gmail.com:587
            163邮箱            smtp.163.com:25                     smtp.163.com:465
            office365          smtp.office365.com:587
            nate邮箱           smtp.mail.nate.com:465
            aol邮箱            smtp.aol.com:587
            outlook            smtp-mail.outlook.com:25
     #########################################################################################
        """
    print helpinfo
    from_addr = raw_input('     伪造发件地址(可选): ')
    dest_list = raw_input('     目标邮箱列表(必填): ')
    smtp_server = raw_input('     smtp服务器(必填): ')
    title = raw_input('     邮件标题信息(必填): ')
    content = raw_input('     邮件内容信息(必填): ')
    attach = raw_input('     邮件附件文件(可选): ')
    print """
     *****************************************************************************************
     """
    try:
        smtpsr = smtp_server.split(":")[0]
        smtport = smtp_server.split(":")[1]

        addrs = tolist(dest_list)


        for addr in addrs:
            send = Single_Send(addr,smtpsr,smtport,content,title,from_addr,attach)
            send.send_msg()

        
    except Exception as e:
        print "     请输入必填信息，谢谢合作!!!"
        pass


if __name__ == '__main__':
    inputinfo()

