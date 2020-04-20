import urllib
import requests
from lxml import etree
import os

# 定义一个空列表用于保存十个页面的地址
url_list = []
def get_url():
	# 十个页面的增加规律是每次加25
    for i in range(0, 226, 25):
        url_root = "https://movie.douban.com/top250?start=%d&filter=" % i
        # 将形成的网页地址添加到列表中
        url_list.append(url_root)


# 定义两个空列表,一个用于保存名称,另一个用于保存图片地址
title_list = []
image_url_list = []
def get_title(url, headers):
 
    res = requests.get(url=url, headers=headers)
    # 这里采用etree来解析xml会方便许多
    html = etree.HTML(res.text)
   	# 匹配名称所在的路径
    title = html.xpath("//img/@alt")
    for i in range(0, len(title) - 1):
        # 将提取到的名称保存到名称列表
        title_list.append(title[i])
 
def get_image_url(url, headers):
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    img_url = html.xpath("//img/@src")
    for i in range(0, len(img_url) - 1):
        image_url_list.append(img_url[i])
		
def main():
 
    headers = {
        "Host": "movie.douban.com",
        "Referer": "https://movie.douban.com/top250?start=225&filter=",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    }
    # 先获得十个页面的地址
    get_url()
    # 调用函数得到相应的列表
    for url in url_list:
        get_title(url, headers)
        get_image_url(url, headers)
	
    if os.path.exists("name_pic.txt") == True:
        os.remove("name_pic.txt")
	
    f = open("name_pic.txt", "a")
    for word in zip(title_list,image_url_list):
        f.write(str(word) + "\n")
    f.close()  # 关闭文件!!
	
	# 图片存放的路径
    movie_path = "movie_img"
    # 如果路径不存在,则新建路径
    if movie_path not in os.listdir():
        os.makedirs(movie_path)
    # 循环名称列表
    for i in range(0, len(title_list)):
    	# 循环图片地址列表
        for j in range(0, len(image_url_list)):
        	# 使名称放到相应的图片下
            if(i == j):
 
                movie_name = title_list[j] + ".jpg"
                filename = movie_path + "/" + movie_name
                # 将图片下载到本地,并命名
                print(movie_name)
                urllib.request.urlretrieve(url=image_url_list[i], filename=filename)
	
if __name__ == '__main__':
	main()