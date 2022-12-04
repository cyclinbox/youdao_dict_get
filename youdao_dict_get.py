#!/usr/bin/env python
#coding=utf-8
# 爬取有道词典的单词数据
# 2022-12-3

import requests
from bs4 import BeautifulSoup
import sys

def searchDict(word):
    url="https://dict.youdao.com/result?word={}&lang=en".format(word)
    req=requests.get(url)
    req.encoding='utf-8'
    txt=req.text
    bs4obj = BeautifulSoup(txt,"lxml")
    c0= bs4obj.body.contents[1].contents[0].contents[0].contents[0].contents[1].contents[0].contents[0].contents[1].contents[1]
    # 获取词性和意义
    c1 = c0.contents[1].contents[0].contents[0].contents[1]
    n = len(c1)
    means = []
    for i in range(0,n-2):
        means.append(c1.contents[i].get_text())
    # 获取派生词
    try:
        c2 = c1.contents[n-1]
        n = len(c2)
        deris = []
        for i in range(0,n):
            deris.append(c2.contents[i].get_text())
    except:
        deris = []
    return means,deris


def help():
    help_text="""
All available commands:
    /?      print this information
    /help   print this information
    /exit   quit program
    /quit   quit program

If you want to search any word, just type word after prompt.
    """
    print(help_text)

def command(cmd):
    if(cmd=="/exit"): sys.exit(0)
    elif(cmd=="/quit"): sys.exit(0)
    elif(cmd=="/help"): help()
    elif(cmd=="/?"   ): help()
    else:
        print("{} is not recognized as an command.".format(cmd))
        help()

if(__name__=='__main__'):
    print("Youdao_dict_get, get word meaning from youdao dict.")
    print("input `/help` for help")
    while(True):
        word = input('input word >>> ')
        if(word[0]=='/'):
            command(word)
        else:
            try:
                means,deris = searchDict(word)
                print("\nWord meaning:")
                for mean in means:print("\t{}".format(mean))
                if(len(deris)>0):
                    print("\nDerived words:")
                    for deri in deris:print("\t{}".format(deri))
            except:
                print("Cannot find word:{}".format(word))
            finally:
                print("\n\n")










        




