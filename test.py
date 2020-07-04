import requests
from lxml import etree

url="http://pic.netbian.com/"
req=requests.get(url)

#print(req.text)
web_text=req.text

html=etree.HTML(web_text)
result=etree.tostring(html)
pic_url=html.xpath("//*[@id='main']/div[3]/ul/li[3]/a/span/img")
for v in pic_url:
    print(v)
