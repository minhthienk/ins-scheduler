import os
import sys
import requests
import re
import time
from bs4 import BeautifulSoup as bs

def string_standardize(text):
    text = str(text)
    text = text.strip()
    text = re.sub(r'\s\s+', ' ', text, re.MULTILINE)
    return text

class CenterOnline(object):
    """docstring for TopKidDo"""
    def __init__(self, session):
        self.session = session
        self.login()

    def login(self):

        cookies = {
            '_ga': 'GA1.1.1585282442.1605495004',
            '_ga_S33MGBEV0G': 'GS1.1.1606723568.39.1.1606724084.0',
            '_ga_6LBTR78SZX': 'GS1.1.1615122483.154.0.1615122498.0',
            'XSRF-TOKEN': 'eyJpdiI6Im9ERkh3WUEweG9oRDAyRW5FU0psdkE9PSIsInZhbHVlIjoiK2FSK0dDK1JvWU1Nd0xtQ0JqNkVmQT09IiwibWFjIjoiMTQ3NDUxMWI3YWM1OGExNTlmNmM2ZDQ2OTVkOGIyNzE4ZjBlYjc5Y2Y5ZTE2ZjE1MThhMTE3MzczNjM4YTk2YSJ9',
            'centeronline_session': 'eyJpdiI6ImtZM2FhQ2tYcXM1UytFYmtoZGZuUnc9PSIsInZhbHVlIjoiMGg2YUp6TTRETERiYldkWlpKT1N4VGVWOUpsR1d0dUNkaDgzNmFOQkpucmIxa0JZelB4OHdtTDVKR20rYVhTVSIsIm1hYyI6IjE5ZTdmMmZiYmRiYjdkZDMwMDJkZTM3ODU3NDRjYTdiNTkzNGJhZjVmMDJhNTAxNDJjNmM1MzE2YzFiOWIyMjYifQ%3D%3D',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://ins.center.edu.vn/login',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        }

        data = '{"username":"admin@admin.com","password":"admin","remember":true}'

        while True:
            response = self.session.get('https://ins.center.edu.vn/', headers=headers, cookies=cookies)
            if response.status_code==200: 
                print('>>>>>>>>>> logged in successfully')
                break
            else:
                print('>>>>>>>>>> failed to log in', response.status_code)
                time.sleep(1)

    def get_class_list(self):
        i = 1
        response = self.session.get('https://ins.center.edu.vn/training/class?page='+str(i))
        class_list = []
        self.get_class_list_per_page(response.text)
        return class_list

    def get_class_list_per_page(self, html):
        soup = bs(html, 'html.parser')
        bs
        soup = bs(soup.prettify(),'html.parser')
        table = soup.find('div', id="table-content")
        rows = table.find_all('tr')
        class_list = []
        for row in rows[1:]:
            cols = row.find_all('td')
            cl = {}
            cl['class-name'] = string_standardize(cols[1].find('b').text)
            cl['student-number'] = string_standardize(cols[3].text)
            cl['lesson-number'] = string_standardize(re.findall(r'\d.+\d', cols[5].text)[0])
            cl['id'] = re.findall(r"\d+", string_standardize(cols[1].find('a', href=True)['href']))[0]
            class_list.append(cl)
        return class_list

    def teacher_proportion(self, class_id):
        response = self.session.get('https://ins.center.edu.vn/training/class/curriculum/index/' + str(class_id))
        return response.text


with requests.Session() as session:
    centeronline = CenterOnline(session)
    teachers = centeronline.teacher_proportion('31166')

soup = bs(teachers, 'html.parser')
teachers = [re.sub(r' \(.+\)', '', string_standardize(teacher.parent.text))
    for teacher in soup.find_all('i', attrs={'class': "fa fa-user"})]
print(teachers)

'''

        



from bs4 import BeautifulSoup as bs
with open("class_list.html", 'r') as file:
    html = file.read()
'''