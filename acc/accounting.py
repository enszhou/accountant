import csv
from bs4 import BeautifulSoup
import requests
import re

#change the accountants_csv to your csv fie 
accountants_cvs = r'C:\Users\enszh\Documents\WeChat Files\wexin1554657859\FileStorage\File\2019-05\FIN_Audit.csv' # your csv file
url_query = 'http://cmispub.cicpa.org.cn/cicpa2_web/PersonIndexAction.do'
url_html = 'http://cmispub.cicpa.org.cn/cicpa2_web/public/query0/2/00.shtml'
host = 'http://cmispub.cicpa.org.cn'
item_num = 5 # the number of items you need


def get_names():
    names = []
    with open(accountants_cvs) as f:
        reader = csv.reader(f)
        i = 0
        for r in reader:
            i += 1
            if i > item_num * 2:
                break
            if i == 1:
                continue
            strs = r[3].split(',')
            for name in strs:
                if name in names:
                    continue
                names.append(name)
            # print(strs)
    return names


def query():
    times = 0
    session = requests.session()
    names = get_names()
    print(names)
    session.get(url=url_html)
    for name in names:
        times += 1
        if times > item_num:
            break
        post_data = {
            'method': 'indexQuery',
            'queryType': 2,
            'isStock': '00',
            'pageSize': '',
            'pageNum': '',
            'ascGuid': '',
            'offName': '',
            'perCode': '',
            'perName': name.encode('gb2312'),
        }
        response = session.post(url=url_query, data=post_data)
        content = response.content
        html = content.decode('GBK')
        html = BeautifulSoup(html, 'html.parser')
        tag_a = html.find(text=name).parent
        href = tag_a['href']
        guid = href.split("'")[1]
        url_detail = host + "/cicpa2_web/003/" + guid + ".shtml"
        html = session.get(url=url_detail).content.decode('GBK')
        # print(html)
        html = BeautifulSoup(html, 'html.parser')
        regex = re.compile('\\s*性别\\s*')
        gender_str = html.find(text=regex).parent.findNext('td').getText()
        gender = re.split(pattern='\\s+', string=gender_str)[1]
        print(name, gender)


if __name__ == '__main__':
    query()
