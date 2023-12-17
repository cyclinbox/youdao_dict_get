# youdao_dict_get

A command line client of youdao dictionary, based on python3(requests + bs4)

一个基于python3的命令行有道词典客户端，通过requests与bs4进行网页爬虫实现

## dependence:

[Python3](https://www.python.org/)(with [Python Standard Library](https://docs.python.org/3.7/library/index.html)),  [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/),  [requests](https://requests.readthedocs.io/en/latest/index.html)

+ Both `bs4` and `requests` can be installed by [pip](https://pypi.org/) or [conda](https://anaconda.org). 


## installation:

just download youdao_dict_get.py and give executable permission by running `chmod +x youdao_dict_get.py` command (for Windows user, only need to download file, don't need to add executable permission)

直接下载 youdao_dict_get.py 文件并使用 `chmod +x youdao_dict_get.py` 指令授予可执行权限既可（windows用户仅需下载，无需授予可执行权限）

## usage:

### REPL mode:

For linux and macOS user:

```bash
./youdao_dict_get.py
```

For Windows user:

```bash
python3 youdao_dict_get.py
```

### Command line argument mode:

You can search word from command line. 

```bash
python3 youdao_dict_get.py [Your word]
```

For example:

```text
~$ python3 youdao_dict_get.py --help

All available commands:
    /?          print this information
    /help       print this information
    /exit       quit program
    /quit       quit program
    /clear      clear screen output
    /version    print program version

If you want to search any word, just type word after prompt.

~$ python3 youdao_dict_get.py submission

Word meaning:
        n.屈服，投降；提交，呈递；提交的文件，呈递材料；<法律>（向法官提出的）看法，意见；<正式> 意见，建议；<古> 谦恭，温顺；（摔跤）制服

Derived words:
        复数submissions
```







