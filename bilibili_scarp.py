

import html5lib
import re
from requests_html import HTMLSession
import json
from requests import get
# 读入cookie并赋值
cookie_file = open("cookie.txt", "r", encoding="utf-8")
cookie_str = cookie_file.read()
cookie_file.close()
# 设置cookies并字典化
cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookie_str.split(";")}
headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
#定义网页html爬取器
def web_text_scarp(uid,ps,pn):
    #设定查询参数
    url=f"https://api.bilibili.com/x/space/wbi/arc/search?mid={uid}&ps={ps}&pn={pn}"
    #设置浏览器访问
    session=HTMLSession()
    #发送请求
    resp_json=session.get(url=url,headers=headers,cookies=cookies).json()
    #将规范格式的json保存下来
    save_json=open("html.txt","w",encoding="utf-8")
    json.dump(resp_json,indent=4,fp=save_json,ensure_ascii=False)
    save_json.close()
uid=input("请输入up主的uid:")
ps=input("请输入图片下载数量(1~30):")
pn=input("请输入视频栏页面数:")
#启动ajax爬取函数
web_text_scarp(uid,ps,pn)
# #读取网页,找到图片封面下载地址
with open("html.txt","r",encoding="utf-8") as file:
    html_content=file.read()
data_dic=json.loads(html_content)
video_ls=data_dic['data']['list']['vlist']
#查找图片地址
cover_pic_ls=[]
for dic in video_ls:
    if "pic" in dic:
        cover_pic_ls.append(dic['pic'])
    if 'cover' in dic:
        cover_pic_ls.append(dic['cover'])

#去除重复的图片地址
deduplicated_pic_ls=list(set(cover_pic_ls))


#设定图片序列名
num=1
#下载图片
for src in deduplicated_pic_ls:
    # #获取图片数据
    img_data=get(url=src,cookies=cookies).content
    #设置图片名字
    img_name=f"{num}.jpg"
    #设置图片保存地址
    img_path=fr"img\{img_name}"
    with open(img_path,"wb") as fp:
        fp.write(img_data)
        print(f"{img_name}","下载成功！")
    num+=1
