#import requests
import grequests
from bs4 import BeautifulSoup 
from urllib.parse import unquote


class Ad():
    def __init__(self, title, url, company):
        self.title = title
        self.url = url
        self.company = company
    def __str__(self):
        return self.title


def get_work_async(num_pages):
    ads = []
    urls = []
    town = 'покровск'
    town_url = str(town.encode()).upper().replace('\\X', '%')[2:-1]
    for i in range(1, num_pages+1):
        #url = f'https://rabota.ua/%D1%85%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2?pg={i}'
        url = f'https://rabota.ua/{town}?pg={i}'
        urls.append(url)
    rs = (grequests.get(u) for u in urls)
    for r in grequests.map(rs):
        if r:
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                items = soup.findAll('div', class_='card-main-content')
                for item in items:
                    link_url = item.find('a', class_='ga_listing')
                    link = 'https://rabota.ua' + link_url.get('href')
                    title = link_url.get('title')
                    company_url = item.find('a', class_='company-profile-name')
                    company = company_url.get('title')
                    ads.append(Ad(title, link, company))
            except Exception as ex:
                print(ex)
    return ads


def generate_html(ads, page_name):
    payload_text = ''
    for ad in ads:
        title_no_bs = ad.title.replace(' ', '__')
        payload_text += f'<div class="ad"><a href={ad.url}>{ad.title}</a> [{ad.company}]<a id="bl" target="_blank" href = go_to_bl?{title_no_bs}>-</a></div>'
    with open(page_name) as fr, open('pages/index.html', 'w', encoding='utf-8') as fw:
        html_text = fr.read()
        res_html_text = html_text.replace('{{generate_text}}', payload_text)
        fw.write(res_html_text)


def apply_blacklist(ads):
    bl = []
    with open('blacklist.txt', encoding='utf-8') as fr:
        for line in fr:
            bl.append(line.replace('\n', '').replace(' ', '__').lower())
    ads_new = []
    for ad in ads:
        bl_flag = False
        for word in ad.title.split():
            if word.lower() in bl: #if one word in black list
                bl_flag = True
            if ad.title.replace(' ', '__').lower() in bl: #if whole ad in blacklist
                bl_flag = True
        if not bl_flag:
            ads_new.append(ad)
    return ads_new


def go_to_bl(url):
    text = unquote(url).replace('__', ' ')
    text += '\n'
    print(text)
    with open('blacklist.txt', 'a', encoding='utf-8') as fw:
        fw.write(text)


def go():
    ads = get_work_async(2)
    ads = apply_blacklist(ads)
    generate_html(ads, 'pages/html_template.html')



if __name__ == '__main__':
    go()