# 2.1.4 实战：中国大学排名定向爬取
import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30) 
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
		
def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children: 
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            # 根据实际提取需要的内容，
            ulist.append([tds[0].string, tds[1].string, tds[3].string])  
			
# 对中英文混排输出问题进行优化:对format()，设定宽度和添加参数chr(12288)
def printUnivList(ulist, num=20):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format('排名', '学校名称', '总分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))
		
u_info = [] # 存储爬取结果的容器
url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html'

html = getHTMLText(url)
fillUnivList(u_info, html) # 爬取

printUnivList(u_info, num=30) # 打印输出30个信息


# 2.2.4 实战：爬取丁香园-用户名和回复内容

from lxml import etree
import requests

url = "http://www.dxy.cn/bbs/thread/626626#626626"

req = requests.get(url)
html = req.text
# html

tree = etree.HTML(html) 
user = tree.xpath('//div[@class="auth"]/a/text()')
# print(user)
content = tree.xpath('//td[@class="postbody"]')

results = []
for i in range(0, len(user)):
    # print(user[i].strip()+":"+content[i].xpath('string(.)').strip())
    # print("*"*80)
    # 因为回复内容中有换行等标签，所以需要用string()来获取数据
    results.append(user[i].strip() + ":  " + content[i].xpath('string(.)').strip())
# 打印爬取的结果

for i,result in zip(range(0, len(user)),results):
    print("user"+ str(i+1) + "-" + result)
    print("*"*100)
	
# 2.3.4 实战：淘宝商品比价定向爬虫
import requests
import re

# 1. 提交商品搜索请求，循环获取页面
def getHTMLText(url):
    """
    请求获取html，（字符串）
    :param url: 爬取网址
    :return: 字符串
    """
    try:
        # 添加头信息,
        kv = {
            'cookie': 'thw=cn; v=0; t=ab66dffdedcb481f77fd563809639584; cookie2=1f14e41c704ef58f8b66ff509d0d122e; _tb_token_=5e6bed8635536; cna=fGOnFZvieDECAXWIVi96eKju; unb=1864721683; sg=%E4%B8%8B3f; _l_g_=Ug%3D%3D; skt=83871ef3b7a49a0f; cookie1=BqeGegkL%2BLUif2jpoUcc6t6Ogy0RFtJuYXR4VHB7W0A%3D; csg=3f233d33; uc3=vt3=F8dBy3%2F50cpZbAursCI%3D&id2=UondEBnuqeCnfA%3D%3D&nk2=u%2F5wdRaOPk21wDx%2F&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTU2MjUyMzkyMw%3D%3D; tracknick=%5Cu4E36%5Cu541B%5Cu4E34%5Cu4E3F%5Cu5929%5Cu4E0B; lgc=%5Cu4E36%5Cu541B%5Cu4E34%5Cu4E3F%5Cu5929%5Cu4E0B; _cc_=WqG3DMC9EA%3D%3D; dnk=%5Cu4E36%5Cu541B%5Cu4E34%5Cu4E3F%5Cu5929%5Cu4E0B; _nk_=%5Cu4E36%5Cu541B%5Cu4E34%5Cu4E3F%5Cu5929%5Cu4E0B; cookie17=UondEBnuqeCnfA%3D%3D; tg=0; enc=2GbbFv3joWCJmxVZNFLPuxUUDA7QTpES2D5NF0D6T1EIvSUqKbx15CNrsn7nR9g%2Fz8gPUYbZEI95bhHG8M9pwA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=32_1; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; swfstore=97213; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=UIHiLt3xThH8t7YQouiW&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTaGqj%2FcX1yKw%3D%3D&tag=8&lng=zh_CN; JSESSIONID=A502D8EDDCE7B58F15F170380A767027; isg=BMnJJFqj8FrUHowu4yKyNXcd2PXjvpa98f4aQWs-RbDvsunEs2bNGLfj8BYE6lWA; l=cBTDZx2mqxnxDRr0BOCanurza77OSIRYYuPzaNbMi_5dd6T114_OkmrjfF96VjWdO2LB4G2npwJ9-etkZ1QoqpJRWkvP.; whl=-1%260%260%261562528831082',
            'user-agent': 'Mozilla/5.0'
        }
        r = requests.get(url, timeout=30, headers=kv)
        # r = requests.get(url, timeout=30)
        # print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "爬取失败"
# 2. 对于每个页面，提取商品名称和价格信息
def parsePage(glist, html):
    '''
    解析网页，搜索需要的信息
    :param glist: 列表作为存储容器
    :param html: 由getHTMLText()得到的
    :return: 商品信息的列表
    '''
    try:
        # 使用正则表达式提取信息
        price_list = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        name_list = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(price_list)):
            price = eval(price_list[i].split(":")[1])  #eval（）在此可以去掉""
            name = eval(name_list[i].split(":")[1])
            glist.append([price, name])
    except:
        print("解析失败")
		
# 3. 将信息输出到屏幕上

def printGoodList(glist):
    tplt = "{0:^4}\t{1:^6}\t{2:^10}"
    print(tplt.format("序号", "商品价格", "商品名称"))
    count = 0
    for g in glist:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
		
# 根据页面url的变化寻找规律，构建爬取url
goods_name = "书包"  # 搜索商品类型
start_url = "https://s.taobao.com/search?q=" + goods_name
info_list = []
page = 3  # 爬取页面数量

count = 0
for i in range(page):
    count += 1
    try:
        url = start_url + "&s=" + str(44 * i)
        html = getHTMLText(url)  # 爬取url
        parsePage(info_list, html) #解析HTML和爬取内容
        print("\r爬取页面当前进度: {:.2f}%".format(count * 100 / page), end="")  # 显示进度条
    except:
        continue

printGoodList(info_list)