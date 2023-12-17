#!/usr/bin/env python
#coding=utf-8
# 爬取有道词典的单词数据
# 2022-12-3
# 2023-2-4 updated
# 2023-8-29 updated: add `clear` command
# 2023-12-17 updated: now can search word from command line arguments

version="1.3 (2023-12-17)"

import requests
from bs4 import BeautifulSoup
import sys
import os

def baiduFanyi(word):
    query = word
    from hashlib import md5
    import json
    # Proxy setting
    proxies={
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    # Set your own appid/appkey.
    appid = '20201212000645063'
    appkey = 'HEhjErB3C9EQzQdtZklq'
    # Set url
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    # It is recommend to use a random num as `salt` to enhance security. But I think is unnecessary.
    salt = 65500 
    sign = md5((appid + query + str(salt) + appkey).encode("utf-8")).hexdigest()
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': "en", 'to': "zh", 'salt': salt, 'sign': sign}
    # Send request
    try:
        r = requests.post(url, params=payload, headers=headers)
    except:
        r = requests.post(url, params=payload, proxies=proxies, headers=headers)
    finally:
        try:
            result = r.json()
        except:
            print("Error:request result={}".format(r))
            return ""
        # Get result
        try:
            trans_res = result['trans_result']
            res = "" # translated text
            for p in trans_res:
                res += p["dst"]
                res += "\n"
            return res
        except:
            print("Error:")
            print(json.dumps(result, indent=4, ensure_ascii=False))
            return ""

def searchDict(word):
    # Proxy setting
    proxies={
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    try: # First we try youdao dict
        url="https://dict.youdao.com/result?word={}&lang=en".format(word)
        try:
            req=requests.get(url)
        except:
            req=requests.get(url,proxies=proxies)
        finally:
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
    except: # We can use Baidu Translation as an alternation
        print("use baidu alternately.")
        means = [baiduFanyi(word)]
        deris = []
    finally:
        return means,deris


def help():
    help_text="""
All available commands:
    /?          print this information
    /help       print this information
    /exit       quit program
    /quit       quit program
    /clear      clear screen output
    /version    print program version

If you want to search any word, just type word after prompt.
    """
    print(help_text)

def command(cmd):
    if(cmd=="/exit"): sys.exit(0)
    elif(cmd=="/quit"): sys.exit(0)
    elif(cmd=="/version"): print("\nversion: {}\n\n".format(version))
    elif(cmd=="/clear"):
        if("win" in sys.platform): os.system("cls")
        else:                      os.system("clear")
    elif(cmd=="/help"): help()
    elif(cmd=="/?"   ): help()
    else:
        print("{} is not recognized as an command.".format(cmd))
        help()

if(__name__=='__main__'):
    # New: search word from command line
    if(len(sys.argv)>1):
        option = (" ".join(sys.argv[1:])).strip()
        if(option[0] in ["-","/"] ): # process command call-back
            option = option.replace("-","").replace("/","")
            option = "/"+option
            command(option)
            sys.exit(0)
        else: # search word, print word meaning and exit
            try:
                means,deris = searchDict(option)
                print("\nWord meaning:")
                for mean in means:print("\t{}".format(mean))
                if(len(deris)>0):
                    print("\nDerived words:")
                    for deri in deris:print("\t{}".format(deri))
            except:
                print("Cannot find word:{}".format(word))
            finally:
                sys.exit(0)
    # Default mode: search word in REPL mode
    print("Youdao_dict_get, get word meaning from youdao dict.")
    print("input `/help` for help")
    while(True):
        word = input('input word >>> ')
        if(len(word)<1):continue
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
