import requests
from bs4 import BeautifulSoup 


class Ad():
    def __init__(self, title, url, company):
        self.title = title
        self.url = url
        self.company = company
    def __str__(self):
        return self.title

def get_work(num_pages):
    ads = []
    for i in range(1, num_pages+1):
        url = f'https://rabota.ua/%D1%85%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2?pg={i}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.findAll('div', class_='card-main-content')
        for item in items:
            link_url = item.find('a', class_='ga_listing')
            link = 'https://rabota.ua' + link_url.get('href')
            title = link_url.get('title')
            company_url = item.find('a', class_='company-profile-name')
            company = company_url.get('title')
            ads.append(Ad(title, link, company))
    return ads


def generate_html(ads, page_name):
    payload_text = ''
    for ad in ads:
        payload_text += f'<a href={ad.url}>{ad.title}</a> [{ad.company}]</br>'
    with open(page_name) as fr, open('pages/index.html', 'w', encoding='utf-8') as fw:
        html_text = fr.read()
        res_html_text = html_text.replace('{{generate_text}}', payload_text)
        fw.write(res_html_text)


def apply_blacklist(ads):
    bl = []
    with open('blacklist.txt', encoding='utf-8') as fr:
        for line in fr:
            bl.append(line.replace('\n', '').lower())
    ads_new = []
    for ad in ads:
        bl_flag = False
        for word in ad.title.split():
            if word.lower() in bl:
                bl_flag = True
        if not bl_flag:
            ads_new.append(ad)
    return ads_new


def go():
    ads = get_work(1)
    ads = apply_blacklist(ads)
    generate_html(ads, 'pages/html_template.html')





if __name__ == '__main__':
    go()