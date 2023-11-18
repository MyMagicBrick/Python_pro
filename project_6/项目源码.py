#!/usr/bin/python2
#-*- coding:utf-8 -*-
import urllib,hashlib
import random
import requests,sys
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams,LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getTransText(text): #����
	q = text
	fromLang = 'auto'  #����Դ����=�Զ����
	toLang1 = 'auto'    #�������� = �Զ����

	appid = '20170711000064108'
	salt = random.randint(32768, 65536)
	secretKey = '0y2JkztWWwGFfgivKz2N' #��Կ

	#����sign
	sign = appid+q+str(salt)+secretKey
	#����ǩ��sign(���ַ���1��md5���ܣ�ע�����md5֮ǰ����1����ΪUTF-8����)
	m1 = hashlib.md5(sign.encode('utf-8'))
	sign = m1.hexdigest()

	#������������
	myurl = '/api/trans/vip/translate'
	myurl = myurl+'?appid='+appid+'&q='+q+'&from='+fromLang+'&to='+toLang1+'&salt='+str(salt)+'&sign='+sign
	url = "http://api.fanyi.baidu.com"+myurl

	# ��������
	url = url.encode('UTF-8')
	res = requests.get(url)
	#ת��Ϊ�ֵ�����
	res = eval(res.text)
	return (res["trans_result"][0]['dst'])

def pdf_to_txt():
    fp = open("/home/xuna/����/python/1.pdf","rb")  #��ȡ�ĵ�����,��·�������Լ��ľ��У���д��һ���������ļ�
    parser = PDFParser(fp) #����һ�����ĵ�������Ľ�����
    doc = PDFDocument(parser) #PDF�ĵ�����洢�ĵ��ṹ
    if not doc.is_extractable: #����ļ��Ƿ������ı���ȡ
        raise PDFTextExtractionNotAllowed

    resource = PDFResourceManager(caching=False) #����PDF��Դ������
    laparam = LAParams()    #����������
    device = PDFPageAggregator(resource,laparams = laparam) #����һ���ۺ���
    interpreter = PDFPageInterpreter(resource,device) #����PDFҳ�������
    #ѭ�������б�ÿ�δ���һ��page����
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)  #���ܸ�ҳ���LTPage����
        layout = device.get_result()
        #����layout��һ��LTPage���������������page�������ĸ��ֶ���
        #һ�����LTTextBox,LTFigure,LTImage,LTTextBoxHorizontal�ȵ�
        result=""
        s=0
        for x in layout:
            #���x���ı�����Ļ�
            if(isinstance(x,LTTextBoxHorizontal)):
                with open('/home/xuna/����/python/3.txt','a') as f:
                    res1 = x.get_text()
                    result+=res1
                    result+='\n'
                    res1 = res1.replace('\n',' ') #������

                    res2 = getTransText(res1).decode('unicode_escape').encode('utf8')
                    result+=res2
                    result+='\n'
                    f.write(result + '\n')
        return result
print pdf_to_txt()