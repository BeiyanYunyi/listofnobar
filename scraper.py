'''
此python程序会爬取所有楼层的ID
和楼中楼的第一页的所有ID(不保证)
然后会把爬取的ID和PeopleList.txt比对并更新
可以通过更改URL来改变爬的帖子.
默认爬取"这↑里↓是召唤塔，即将根据金吧遗留帖子顺序进行召唤"一贴
'''

import requests
from bs4 import BeautifulSoup
import ast 

url = "https://tieba.baidu.com/p/6597831409"
lst = ""
max_page = 0
ids = set()


#判断总共有多少页
main_page = BeautifulSoup(requests.get(url).text, features="lxml")
max_tag = main_page.find(attrs={"max-page": True})
max_page = int(max_tag["max-page"])

print("总共有{}页".format(max_page))

#爬虫
for cnt in range(1, max_page + 1):
  print("处理第{}页中...".format(cnt))
  raw = requests.get("{}?pn={}".format(url, cnt)).text

  soup = BeautifulSoup(raw, features="lxml")

  for item in soup.find_all(attrs={"data-field": True}):

    #格式化,然后用eval转成字典
    s = item["data-field"].replace("false", "False")
    s = s.replace("null", 'None')

    d = ast.literal_eval(s)
    if "un" in d.keys():
      ids.add(d["un"])

#比对人名
print("以下为新增人员:")
with open("PeopleList.txt", "r+", encoding="UTF-8") as f:
  people_list = []

  #去掉\n
  for i in f.readlines():
    people_list.append(i.strip())

  for people in ids:
    if people not in people_list:
      print(people)
      print(people, file=f)

#排序
ls = []
with open("PeopleList.txt", 'r', encoding="UTF-8") as f:
    ls = f.readlines()
    ls.sort()

with open("PeopleList.txt", 'w', encoding="UTF-8") as f:
    f.writelines(ls)
