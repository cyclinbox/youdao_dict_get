#!/usr/bin/env python
#coding=utf-8
# 从sqlite3数据库中读取单词数据并输出
# 词典文件来自GitHub存储库: https://github.com/skywind3000/ECDICT
# downloading URL:
#   https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip
# after downloading, it also need to unzip.
# 2024-2-22

version="1.0 (2024-2-22)"

import sys
import os
import sqlite3

columns = ["id","word","sw","phonetic","definition","translation" ,"pos" ,
    "collins","oxford","tag" ,"bnc" ,"frq" ,"exchange" ,"detail" ,"audio"]
col_n = len(columns)

con = sqlite3.connect("stardict.db")
cur = con.cursor()

## Maximum display limitation
# If multiple results are matched,  this varible indicate us how many
# results should we display. It can be changed by `/limit` command.
MAX_DISP_LIMIT = 5 

## Search precise level
# 0: double wildcard(eg: %word%). 1: prefix wildcard(eg: word%). 2: no wildcard(eg: word)
PRECISE_LEVEL = 2 

## Display result mode
# 0: Detail. 1: Simple
SIMPLE_DISP = 1 

def searchDataBase(word):
    if(  PRECISE_LEVEL==0): res = cur.execute("SELECT * FROM stardict WHERE word LIKE '%{}%'".format(word)).fetchall()
    elif(PRECISE_LEVEL==1): res = cur.execute("SELECT * FROM stardict WHERE word LIKE  '{}%'".format(word)).fetchall()
    else:                   res = cur.execute("SELECT * FROM stardict WHERE word LIKE  '{}' ".format(word)).fetchall()
    return res

def display_single_word(word_res):
    if(SIMPLE_DISP):
        print(word_res[4])
        print(word_res[5])
    else:
        for i in range(4,col_n):
            if(word_res[i] not in ["",None]):
                column = columns[i].upper()
                result = word_res[i]
                if(i == 4 or i == 5 or i == 12 or i == 13 or i == 14):
                    if('\n' in result):
                        result = result.replace("\n","\n\t")
                print(f"<{column}>\n\t{result}")
    print("\n")


def searchDict(word):
    res = searchDataBase(word)
    if(len(res)==0):
        print(f"Cannot find word:{word}\n\n")
    elif(len(res)==1):
        display_single_word(res[0])
    elif(len(res)<MAX_DISP_LIMIT):
        for i in range(len(res)):
            print(f"[{i}] {res[i][1]} :")
            display_single_word(res[i])
    else:
        print(f"Too many items are matched(total {len(res)} results). Display the top {MAX_DISP_LIMIT} results:")
        for i in range(MAX_DISP_LIMIT):
            print(f"[{i}] {res[i][1]} :")
            display_single_word(res[i])


def help():
    help_text="""
All available commands:
    /help   /?      print this help information
    /quit   /q      quit program
    /exit   /e      quit program
    /limit  /lim    check and change display limitation
    /precise /prc   change precise level
                        level 0 [LOS]: most loose
                        level 1 [MOD]: moderate loose
                        level 2 [PRC]: most precise
    /simple /sim    change display mode
                        simple  mode [SM]: only display defination and translation
                        verbose mode [VB]: display more details
    /clear  /cls    clear screen output
    /version /ver   print program version



If you want to search any word, just type word after prompt.
    """.strip()
    print(help_text)

def command(cmd):
    global MAX_DISP_LIMIT, PRECISE_LEVEL, SIMPLE_DISP
    if(  cmd=="/exit" or cmd=="/e"): sys.exit(0)
    elif(cmd=="/quit" or cmd=="/q"): sys.exit(0)
    elif(cmd=="/version" or cmd=="/ver"): print("\nversion: {}\n\n".format(version))
    elif(cmd=="/clear"   or cmd=="/cls"):
        if("win" in sys.platform): os.system("cls")
        else:                      os.system("clear")
    elif(cmd=="/limit" or cmd=="/lim"):
        print(f"Current max display limitation is {MAX_DISP_LIMIT}")
        new_limit = input("type new limit:")
        try:
            new_limit_int = int(new_limit)
            if(new_limit_int > 0 and new_limit_int < 1000):
                MAX_DISP_LIMIT = new_limit_int
                print(f"New max display limitation is {MAX_DISP_LIMIT}")
            else: print(f"Illegal limitation value: {new_limit_int}")
        except: pass
    elif(cmd=="/precise" or cmd=="/prc"):
        PRECISE_LEVEL += 1
        if(PRECISE_LEVEL==3): PRECISE_LEVEL=0
    elif(cmd=="/simple"  or cmd=="/sim"):
        SIMPLE_DISP = 1-SIMPLE_DISP
    elif(cmd=="/help" or cmd=="/?"): help()
    else:
        print("{} is not recognized as an command.".format(cmd))
        help()

if(__name__=='__main__'):
    # New: search word from command line
    if(len(sys.argv)>1):
        option = (" ".join(sys.argv[1:])).strip()
        if( option in ["/install","--install","-install"]):
            print("Installing offline dictionary...")
            os.system("wget https://github.com/skywind3000/ECDICT/releases/download/1.0.28/ecdict-sqlite-28.zip")
            os.system("unzip ecdict-sqlite-28.zip")
            os.system("rm ecdict-sqlite-28.zip")
            sys.exit(0)
        elif(option[0] in ["-","/"] ): # process command call-back
            option = option.replace("-","").replace("/","")
            option = "/"+option
            command(option)
            sys.exit(0)
        else: # search word, print word meaning and exit
            searchDict(option)
    # Default mode: search word in REPL mode
    print("Offline_dict_get, get word meaning from offline dict sqilte database.")
    print("input `/help` for help")
    while(True):
        prc_levl_idct = ["LOS","MOD","PRC"][PRECISE_LEVEL]
        sim_disp_idct = ["VB" ,"SM"       ][SIMPLE_DISP]
        prompt_text = f"({prc_levl_idct}:{sim_disp_idct}) >>> "
        word = input(prompt_text)
        if(len(word)<1):continue
        if(word[0]=='/'):
            command(word)
        else:
            searchDict(word)
            









                
