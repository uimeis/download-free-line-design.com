import requests
from bs4 import BeautifulSoup
import random
import re
import json
import time
import os

header = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'free-line-design.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}
cook = {'Cookie':'PHPSESSID=k4o91h0mjsuglj6nnlenbk0997; _ga=GA1.2.1505319313.1510016503; _gid=GA1.2.785824010.1510016503; _gat=1'}

# url = 'http://free-line-design.com/?paged=21'
# def article_url(list_url):
#     result = []
#     res = requests.get(list_url, headers = header, cookies = cook)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     #
#     for i in soup.select('#mainList span'):
#         result.append(i.a['href'])
#     return result #取出文章链接,组成列表
#
# #获取整站所有文章链接
# total_article_url = []
# for i in range(1,36):
#     total_article_url.extend(article_url('http://free-line-design.com/?paged={}'.format(i)))
#     time.sleep(random.randint(3, 6))  # 限制爬取时间
# print(total_article_url)
#
# with open ('free-line-design.json','w') as f:
#     json.dump(total_article_url, f)


# #取出文章图片链接函数
# # article_url = 'http://free-line-design.com/?p=486'
# def art_img_url_list(article_url):
#     img_url_list = []
#     art_res = requests.get(article_url, headers = header, cookies = cook)
#     art_soup = BeautifulSoup(art_res.text,'html.parser')
#     for i in art_soup.select('#mainList li img'):
#         img_url_list.append('http://free-line-design.com/' + i['src'])
#     return img_url_list #取出图片链接，组成列表
#
# #取出一个文章页所有内容函数
# def article_total(article_url):
#     result = {}
#     art_res = requests.get(article_url, headers = header, cookies = cook)
#     art_soup = BeautifulSoup(art_res.text,'html.parser')
#
#     result['png_download_url'] = 'http://free-line-design.com/' + \
#                        art_soup.select('#mainList li img')[0]['src'].replace('png/','')\
#                            .rstrip('_0M.png') + 'pngset.zip' #png下载地址
#     result['ai_download_url'] = 'http://free-line-design.com/' + \
#                       art_soup.select('#mainList li img')[0]['src'].replace('png/','')\
#                           .rstrip('0M.png') + 'ai.zip' #ai下载地址
#     result['img_list'] = art_img_url_list(article_url) #图片地址
#     result['article_url'] = article_url
#     return result
#
# def aaa():
#     total = []
#     with open('free-line-design.json','r') as f:
#         list = json.load(f)
#         print(list)
#         for url in list:
#             total.append(article_total(url))
#             print('第' + url + '页')
#             time.sleep(random.randint(5, 10))  # 限制爬取时间
#         return total
#
# with open('article_total.json','w') as n:
#     json.dump(aaa(), n)

下载保存文件
with open('article_total.json','r') as f:
    for i in json.load(f):
        file_name = i['article_url'].split('/')[-1].lstrip('?p=') #文件夹名称
        png_name = i['png_download_url'].split('/')[-1].lstrip('b_') #png名称
        ai_name = i['ai_download_url'].split('/')[-1].lstrip('b_') #ai名称
        #
        file_path = os.path.exists('{}'.format(file_name))
        if not file_path:
            os.mkdir('{}'.format(file_name))
            print('{}'.format(file_name) + '目录创建成功')
            for img in i['img_list']:
                img_name = img.split('/')[-1].lstrip('b_') #图片名称
                img_url = requests.get(img)
                with open('{}\{}'.format(file_name, img_name), 'wb') as img_file:
                    img_file.write(img_url.content)  # 保存图片
                time.sleep(random.randint(1,2))  # 限制爬取时间

            png = requests.get(i['png_download_url'])
            with open('{}\{}'.format(file_name, png_name), 'wb') as png_file:
                png_file.write(png.content)  # 保存png文件

            ai = requests.get(i['ai_download_url'])
            with open('{}\{}'.format(file_name, ai_name), 'wb') as ai_file:
                ai_file.write(ai.content)  # 保存ai文件

            time.sleep(random.randint(5, 10))  # 限制爬取时间
        else:
            print('{}'.format(file_name) + '目录已存在')
