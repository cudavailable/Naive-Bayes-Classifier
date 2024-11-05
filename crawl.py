import os
from bs4 import BeautifulSoup
from urllib import request

# 用request和BeautifulSoup处理网页
def requestOver(url):
    req = request.Request(url)
    response = request.urlopen(req)
    soup = BeautifulSoup(response, 'lxml')
    return soup

# 从网页下载标题和内容到txt文档
def download(title, url, y):
    soup = requestOver(url)
    tag = soup.find('div', class_="article")
    if(tag == None):
        return 0
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace('|', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('?', '')
    content = ""
    for p in tag.findAll('p'):
        if (p.string != None):
            content = content + p.string

    # 准备将爬取到的新闻存放到指定路径
    news_dir = "./news"
    if news_dir is not None and not os.path.exists(news_dir):
        os.mkdir(news_dir)
    filename = os.path.join(news_dir, f"{title}.txt")
    with open(filename, 'w', encoding='utf-8') as file_object:
        file_object.write('           ')
        file_object.write(title)
        file_object.write(tag.get_text())
    print('正在爬取第', y, '个新闻', title)

# 爬虫具体执行过程
def crawlAll(url, y):
    soup = requestOver(url)
    for tag in soup.findAll("a", target="_blank"):
        if tag.string != None:	#标题非空
            if len(tag.string) > 8: # 标题长度大于8
                if(("https://news.sina.com.cn/" in tag.attrs["href"]) or ("http://news.sina.com.cn/" in tag.attrs["href"])):
                    alllist.append(tag.attrs["href"])
                    if ((tag.attrs["href"] not in collection)):
                        collection.add(tag.attrs["href"])
                        try:
                            print(tag.attrs['href'])
                            download(tag.string, tag.attrs['href'], y)
                            y += 1
                        except Exception:
                            print("第" + str(y) + "个新闻爬取失败")
                        else:
                            crawlAll(tag.attrs['href'], y)
    return y

if __name__ == '__main__':
    y = 1
    collection = set() # 用于链接去重
    alllist = set()	# 用于存放你需要爬取的网页
    alllist = ["https://news.sina.com.cn/"]
    for n in alllist:
        target_url = n
        y = crawlAll(target_url, y)
