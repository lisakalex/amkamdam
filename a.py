#!/home/al/.venv/bin/python3
import glob2
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
import shutil
from datetime import datetime
import filetype
import magic
import os
import json
import re
from bs2json import BS2Json
import codecs

# https://beautiful-soup-4.readthedocs.io/en/latest/

start_time = time.time()
todaytime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
newsapi = ''


# with open('newsapi.json') as file:
#     try:
#         newsapi = json.loads(file.read())
#     except Exception as e:
#         print(e)
# pass

# shutil.rmtree('./b/', ignore_errors=True)
# shutil.rmtree('./public_html', ignore_errors=True)
# shutil.copytree('./replace/', './b/', dirs_exist_ok=True)
# shutil.copytree('./a/cryptonews.com', './b/', dirs_exist_ok=True)
# shutil.rmtree('./b/cryptonews.com/tags/', ignore_errors=True)


def replace_head(read_file1):
    with open('index.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    head = soup.find("head")
    # header = soup.find("header")
    # footer = soup.find("footer")

    soup1 = BeautifulSoup(read_file1, features="html.parser")

    head1 = soup1.find("head")
    if head1:
        head1.replace_with(head)

    # header1 = soup1.find("header")
    # if header1:
    #     header1.replace_with(header)
    #
    # footer1 = soup1.find("footer")
    # if footer1:
    #     footer1.replace_with(footer)

    return str(soup1)


def replace_links(read_file1):
    soup = BeautifulSoup(read_file1, features="html.parser")
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            if 'https://www.houseandgarden.co.uk' in href:
                href = href.replace('https://www.houseandgarden.co.uk', '')
                link['href'] = href

            # if 'https://kumkanot.com' in href:
            #     href = href.replace('https://kumkanot.com', '')
            #     link['href'] = href
            #
            # if '/ext/' in href:
            #     href = href.replace('/ext/', 'https://cryptonews.com/ext/')
            #     link['href'] = href

    # logo = soup.find('img', class_='header-logo-image')
    # if logo:
    #     logo['src'] = '/assets/img/amkamdam.com.svg'
    #
    # try:
    #     soup.head.insert(1, soup.new_tag("meta", charset="UTF-8.css"))
    # except Exception as e:
    #     print(e)
    #     pass

    return str(soup)


def download_files(url, path, file1):
    time.sleep(1)

    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        source = requests.get(url, headers=headers, timeout=None)

        Path(path).mkdir(parents=True, exist_ok=True)
        with open(path + file1, "w") as f:
            f.write(source.text)

    except Exception as e:
        print(e)
        pass


def download_json_files(read_file1):
    soup = BeautifulSoup(read_file1, features="html.parser")
    soup1 = soup.find_all("a")
    for link in soup1:
        loadmoretype = link.get('loadmoretype')
        if loadmoretype:
            url = 'https://cryptonews.com/paged/' + loadmoretype + '-1.json'
            print(url)
            path = './b/paged/'
            file1 = loadmoretype + '-1.json'
            download_files(url, path, file1)


def insert_ads(read_file1):
    with open('me-index.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    soup1 = BeautifulSoup(read_file1, features='html.parser')

    for dslot in soup1.findAll('div', class_='dslot'):
        for medslot in soup.findAll('div', class_='dslot'):
            if dslot.get('did') == medslot.get('did'):
                dslot.replace_with(medslot)

    return str(soup1)


def insert_cookie(read_file1):
    with open('me-index.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    scripts = soup.body.findAll('script')
    soup1 = BeautifulSoup(read_file1, features='html.parser')
    try:
        soup1.body.append(scripts[0])
    except Exception as e:
        print(e)
        pass

    try:
        soup1.body.append(scripts[1])
    except Exception as e:
        print(e)
    pass

    return str(soup1)


# global newsapi
# with open('newsapi.json') as file:
#     try:
#
#         newsapi = json.loads(file.read())
#     except Exception as e:
#         print(e)
# pass


def replace_text(read_file1, newsapi1):
    soup = BeautifulSoup(read_file1, features='html.parser')
    section = soup.find_all('article', class_='mb-15 mb-sm-30 article-item')
    for i in range(0, 4):
        n = newsapi1['articles'][i]
        article = section[i]
        link = article.find('a', class_='article__image')
        link['href'] = n['url']

        img = article.find('img')
        img['src'] = n['urlToImage']
        img['srcset'] = ''
        img['alt'] = n['title']

        badge_date = article.find('div', class_='article__badge-date')
        badge_date['data-utctime'] = n['publishedAt']

        link1 = article.find('a', class_='article__title')
        link1['href'] = n['url']
        link1.string = n['title']
        article.find_all('div')[6].string = n['content']

    section = soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20')
    for i in range(0, 5):
        n = newsapi1['articles'][i]
        article = section[i]
        link = article.find('a', class_='article__image')
        link['href'] = n['url']

        img = article.find('img')
        img['src'] = n['urlToImage']
        img['srcset'] = ''
        img['alt'] = n['title']

        badge_date = article.find('div', class_='article__badge-date')
        badge_date['data-utctime'] = n['publishedAt']

        link1 = article.find('a', class_='article__title')
        link1['href'] = n['url']
        link1.string = n['title']
        # article.find_all('div')[6].string = n['content']

    section = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30')
    for i in range(0, 16):
        n = newsapi1['articles'][i]
        article = section[i]
        link = article.find('a', class_='article__image')
        link['href'] = n['url']

        img = article.find('img')
        img['src'] = n['urlToImage']
        img['srcset'] = ''
        img['alt'] = n['title']

        badge_date = article.find('div', class_='article__badge-date')
        badge_date['data-utctime'] = n['publishedAt']

        link1 = article.find('a', class_='article__title')
        link1['href'] = n['url']
        link1.string = n['title']

    # article = section.findAll('article')
    # for s in scripts:
    #     if 'window.__PRELOADED_STATE__' in s.text:
    #         ss = s.text.replace("window.__PRELOADED_STATE__ = ", "")
    #         ss = ss[:-1]
    #         y = json.loads(ss)
    #         y['transformed']['scTheme']['typography']['fontFaces'] = ''
    #         y = json.dumps(y)
    #         y = y.replace('https://www.houseandgarden.co.uk', '')
    #         s.string.replace_with("window.__PRELOADED_STATE__ = " + y)
    #
    #     if 'window.dataLayer' in s.text:
    #         ss = s.text.replace("window.dataLayer = ", "")
    #         ss = ss[:-1]
    #         y = json.loads(ss)
    #         y[0]['page'] = ''
    #         y = json.dumps(y)
    #         y = y.replace('https://www.houseandgarden.co.uk', '')
    #         s.string.replace_with("window.dataLayer = " + y)

    # read_file1 = read_file1.replace('https:\u002F\u002Fwww.houseandgarden.co.uk', '')
    # read_file1 = read_file1.replace('https://www.houseandgarden.co.uk', '')

    # with open('index.html', 'r') as file1:
    #     da = file1.read()

    # try:
    #     data = re.search(r"window.__PRELOADED_STATE__ = (.*?);", read_file1).string
    #     data = json.loads(data)
    # except Exception as e:
    #     print(e)
    #     pass

    # bs2json = BS2Json(read_file1)

    # Convert soup to JSON
    # json_obj = bs2json.convert()
    # kk = '🅥'
    # kk1 = kk.encode('utf-8')
    # kk2 = b'\xf0\x9f\x85\xa5'.decode('utf-8')

    # kk = '\u002F'
    # kk1 = kk.encode('utf-8')
    # kk2 = b'/'.decode('utf-8')

    # x = read_file1
    # read_file2 = json.loads(read_file1)
    # read_file3 = json.dumps(read_file2)

    # x = read_file1.find('\u002F')
    # read_file1 = read_file1.replace('\u002F', '')
    # read_file1 = read_file1.replace('https://www.houseandgarden.co.uk', '')
    # read_file1 = read_file1.replace('<link rel="preload" id="oneTrustPreload" href="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js" as="script"/><script id="onetrust-script" src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js" data-domain-script="f6b16b4e-d2a0-420d-8eea-2f7a8d8a4516"></script>', '')

    # read_file1 = codecs.decode(read_file1, 'unicode-escape')
    # read_file1 = read_file1.replace(',{"isExternal":false,"showInTopNav":true,"text":"Top 100","url":"https://www.houseandgarden.co.uk/topic/interior-designers  ","forceLeftOfNav":true,"isActive":false},{"isExternal":false,"showInTopNav":true,"text":"The List","url":"https://thelist.houseandgarden.com","forceLeftOfNav":true,"isActive":false},{"isExternal":false,"showInTopNav":true,"text":"Video","url":"/video","forceLeftOfNav":false,"isActive":false},{"isExternal":false,"showInTopNav":false,"text":"How To","url":"https://howto.houseandgarden.co.uk","forceLeftOfNav":false,"isActive":false},{"isExternal":false,"showInTopNav":true,"text":"Shopping","url":"https://www.houseandgarden.co.uk/topic/shopping","forceLeftOfNav":false,"isActive":false},{"text":"Promotions","url":"https://www.houseandgarden.co.uk/topic/promotions","isActive":false}', '')
    # read_file1 = read_file1.replace('{"label":"Follow us on Facebook","network":"facebook","url":"https://www.facebook.com/houseandgardenuk/"},{"label":"Follow us on Instagram","network":"instagram","url":"https://www.instagram.com/houseandgardenuk/"},{"label":"Follow us on Pinterest","network":"pinterest","url":"https://www.pinterest.co.uk/houseandgarden/"},{"label":"Follow us on X","network":"twitter","url":"https://twitter.com/_houseandgarden"},{"label":"Follow us on YouTube","network":"youtube","url":"https://www.youtube.com/channel/UCBEqJ-MfSIxKM5mgwVB3ZDg"},{"label":"Follow us on TikTok","network":"TikTok","url":"https://www.tiktok.com/@houseandgardenuk"}', '')
    # read_file1 = read_file1.replace(
    #     '{"id":"618a1abbbd9ab40f43643687","text":"Subscribe to our print &amp; digital issue","template":"verso-ticker","link":{"href":"https://www.houseandgarden.co.uk/subscribe 4","text":"Order Now"},"image":{"modelName":"photo","collection":"photos","tags":[],"id":"6633715293bc74a543cac63d","caption":null,"altText":"","credit":null,"filename":"06_24Cover4ColNoPrice.jpg","aspectRatios":{"master":{"url":"https://gp-prd-global-clips-s3.s3.amazonaws.com/public/houseandgarden-services/production/2024/05/02/6633715193bc74a543cac63c_06_24Cover4ColNoPrice.jpg","width":2563,"height":3366,"format":"JPEG","modifications":null},"16:9":{"url":null,"width":2560,"height":1440,"format":null,"modifications":{"crop":{"height":1440,"width":2560,"x":1,"y":97}}},"3:2":{"url":null,"width":2562,"height":1708,"format":null,"modifications":{"crop":{"height":1708,"width":2562,"x":1,"y":76}}},"4:3":{"url":null,"width":2560,"height":1920,"format":null,"modifications":{"crop":{"height":1920,"width":2560,"x":3,"y":83}}},"1:1":{"url":null,"width":2563,"height":2563,"format":null,"modifications":{"crop":{"height":2563,"width":2563,"x":0,"y":94}}},"3:4":{"url":null,"width":2523,"height":3364,"format":null,"modifications":{"crop":{"height":3364,"width":2523,"x":20,"y":0}}},"2:3":{"url":null,"width":2244,"height":3366,"format":null,"modifications":{"crop":{"height":3366,"width":2244,"x":159.5,"y":0}}}},"contentWarnings":[],"segmentedSources":{"sm":[{"aspectRatio":"master","width":160,"url":"https://media.houseandgarden.co.uk/photos/6633715293bc74a543cac63d/master/w_160,c_limit/06_24Cover4ColNoPrice.jpg","srcset":"https://media.houseandgarden.co.uk/photos/6633715293bc74a543cac63d/master/w_120,c_limit/06_24Cover4ColNoPrice.jpg 120w","height":210}],"lg":[{"aspectRatio":"master","width":160,"url":"https://media.houseandgarden.co.uk/photos/6633715293bc74a543cac63d/master/w_160,c_limit/06_24Cover4ColNoPrice.jpg","srcset":"https://media.houseandgarden.co.uk/photos/6633715293bc74a543cac63d/master/w_120,c_limit/06_24Cover4ColNoPrice.jpg 120w","height":210}]},"contentType":"photo"}}',
    #     '')
    # read_file1 = read_file1.replace('https://www.houseandgarden.co.uk', '')
    # read_file1 = read_file1.replace('xxx', '')
    # read_file1 = read_file1.replace('xxx', '')
    # read_file1 = read_file1.replace('xxx', '')

    # read_file1 = read_file1.replace("&quot;dangerousHed&quot;", 'tihuy')
    # read_file1 = read_file1.replace("'https:\u002F\u002Fwww.houseandgarden.co.uk'", '')
    # mystr = 'https://www.houseandgarden.co.uk'
    # mystr = 'https:\u002F\u002Fwww.houseandgarden.co.uk'
    # mystr.encode('utf-8').decode('utf-8')
    # mystr = mystr.decode('utf-8')
    # s.encode().decode('unicode-escape')

    # s = "https:\u002F\u002Fwww.houseandgarden.co.uk"
    # s = "https://www.houseandgarden.co.uk"

    # encoded_string = s.encode('utf-8')
    # print('The encoded string in base64 format is :')
    # print(encoded_string)

    # read_file2 = read_file1.encode('utf-8')
    # read_file3 = read_file2.decode('utf-8')
    # read_file1 = read_file1.replace(decoded_string, '')

    # read_file1 = read_file1.replace('CryptoNews', 'Kumkanot')
    # read_file1 = read_file1.replace('CRYPTONEWS', 'KUMKANOT')
    # read_file1 = read_file1.replace('Crypto News', 'Kumkanot')
    # read_file1 = read_file1.replace('#930046', '#00b900')
    # read_file1 = read_file1.replace('#59008a', '#018001')

    # read_file1 = read_file1.encode().decode('unicode-escape')
    # read_file1.replace(u"\u002F", "*")
    # read_file1 = read_file1.replace(chr(47), "/")
    # read_file1 = read_file1.replace(ord(47), '/')
    # read_file1 = read_file1.replace('ku', 'huy')
    # read_file1.replace('/', "*")
    # read_file1.decode("utf-8").replace(u"\u002F", "*").encode("utf-8")
    # read_file1 = read_file1.replace("\u002F", "*")
    # read_file1 = read_file1.replace(u"\u002F", "/")
    # read_file1 = read_file1.replace(u"\u002F", "/").encode("utf-8")
    # regex = re.compile("u'2022'",re.UNICODE)
    # regex = re.compile("u'002F'",re.UNICODE)
    # newstring = re.sub(regex, something, yourstring, <optional flags>)
    # read_file1 = read_file1.find("\u002F")
    # return read_file1
    # return str(soup).encode().decode('unicode-escape')
    return str(soup)


def decompose_tags(read_file1):
    soup = BeautifulSoup(read_file1, features='html.parser')
    with open('index.html', 'r') as file1:
        soup1 = BeautifulSoup(file1.read(), features="html.parser")

    try:
        soup.find('div', id='app-root').next_element.decompose()
    except Exception as e:
        print(e)
    pass

    # approot = soup.find('div', id='app-root').next_element
    # if approot:
    #     approot.decompose()

    head = soup.find("head")
    head1 = soup1.find("head")
    if head:
        head.replace_with(head1)

    # d = soup.find('section', class_='header__global-message')
    # if d:
    #     d.decompose()
    #
    # uspbanner = soup.find('div', class_='uspBanner--wrapper')
    # if uspbanner:
    #     uspbanner.decompose()
    #
    # uspbanner = soup.find('div', class_='footer__subfooter')
    # if uspbanner:
    #     uspbanner.decompose()
    #
    # uspbanner = soup.find('div', class_='payment-icons')
    # if uspbanner:
    #     uspbanner.decompose()
    #
    # accordion = soup.find('button', id='xo-widget--recommended')
    # if accordion:
    #     accordion.decompose()
    #
    # accordion = soup.find('button', id='accordion-control--2')
    # if accordion:
    #     accordion.decompose()
    #
    # accordion = soup.find('button', id='accordion-control--5')
    # if accordion:
    #     accordion.decompose()
    #
    # accordion = soup.find('button', id='accordion-control--2')
    # if accordion:
    #     accordion.decompose()

    # newsletter_modal = soup.find('div', class_='modal')
    # if newsletter_modal:
    #     newsletter_modal.decompose()
    #
    # iframes = soup.findAll('iframe')
    # for iframe in iframes:
    #     if iframe:
    #         iframe.parent.decompose()
    #
    # widget_containers = soup.findAll('div', id='widget_container')
    # for widget_container in widget_containers:
    #     if widget_container:
    #         widget_container.decompose()
    #
    # scripts = soup.findAll('script')
    # for script in scripts:
    #     if script:
    #         script.decompose()
    #
    # socials = soup.findAll('div', class_='socials')
    # for social in socials:
    #     if social:
    #         social.decompose()
    #
    # twitter = soup.find_all("h2")
    # for t in twitter:
    #     if 'Twitter' in t.text:
    #         t.decompose()
    #
    # tags_links = soup.find_all("a")
    # for t in tags_links:
    #     if t.has_attr('href'):
    #         if '/tags/' in t['href']:
    #             t.decompose()
    #
    # videos = soup.find_all("section")
    # for v in videos:
    #     videosh2 = v.find("h2")
    #     if videosh2 is not None:
    #         if 'Videos' in videosh2.text:
    #             v.decompose()

    return str(soup)


def replace_text_1(read_file1):
    read_file1 = json.loads(read_file1)
    read_file1 = json.dumps(read_file1)
    return read_file1


def main():
    newsapi = []
    with open('newsapi/newsapi.json') as file:
        try:
            newsapi = json.load(file)
        except Exception as e:
            print(e)
        pass

    newstechnology = []
    with open('html/paged/newstechnology-news-1.json') as file:
        try:
            newstechnology = json.load(file)
        except Exception as e:
            print(e)

        pass

    for i in range(0, 3):
        newstechnology.append(
            "<article class=\"mb-30\">\n\t<div class=\"row\">\n        <div class=\"col-4 col-md-12\">\n\t\t    <a href=\"/news/could-chatgpts-latest-enhancement-herald-revolutionary-phase-for-crypto.htm\" class=\"article__image article__image--sm-wider mb-15  \">\n\t\t    \t<div class=\"img-sized\"><img alt=\"Could ChatGPT's Latest Enhancement Herald a Revolutionary Phase for Crypto?\" class=\"img-fluid\" loading=\"auto\" srcset=\"https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_1920_1080.jpg 1920w, https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_1200_675.jpg 1200w, https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_900_506.jpg 900w, https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_720_405.jpg 720w, https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_600_338.jpg 600w, https://cimg.co/news/125773/332072/responsive-images/polygons-ga28790590-1920___media_library_original_300_169.jpg 300w\" src=\"https://cimg.co/news/125773/332072/polygons-ga28790590-1920.jpg\" width=\"1920\"></div>\n\t\t    </a>\n        </div>\n        <div class=\"col-8 col-md-12\">\n            <div class=\"article__badge article__badge--sm \">\n\t\t\t\t <a class=\"article__badge article__badge--sm\" href=\"/news/technology-news/\"> Technology News </a>\t\t    \t<div class=\"article__badge-date d-md-inline-block\" data-utctime=\"2023-09-29 08:42:00\">&bull; Sep 29, 2023</div>\n\t\t    </div>\n\t\t    <a href=\"/news/could-chatgpts-latest-enhancement-herald-revolutionary-phase-for-crypto.htm\" class=\"article__title article__title--md article__title--featured\">\n\t\t      <h4>Could ChatGPT's Latest Enhancement Herald a Revolutionary Phase for Crypto?</h4>\n\t\t    </a>\n        </div>\n    </div>\n</article>\n"
            # "<article class=\"mb-30\">\n\t<div class=\"row\">\n        <div class=\"col-4 col-md-12\">\n\t\t    <a href=\"\/news\/could-chatgpts-latest-enhancement-herald-revolutionary-phase-for-crypto.htm\" class=\"article__image article__image--sm-wider mb-15  \">\n\t\t    \t<div class=\"img-sized\"><img alt=\"Could ChatGPT's Latest Enhancement Herald a Revolutionary Phase for Crypto?\" class=\"img-fluid\" loading=\"auto\" srcset=\"https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_1920_1080.jpg 1920w, https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_1200_675.jpg 1200w, https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_900_506.jpg 900w, https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_720_405.jpg 720w, https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_600_338.jpg 600w, https:\/\/cimg.co\/news\/125773\/332072\/responsive-images\/polygons-ga28790590-1920___media_library_original_300_169.jpg 300w\" src=\"https:\/\/cimg.co\/news\/125773\/332072\/polygons-ga28790590-1920.jpg\" width=\"1920\"><\/div>\n\t\t    <\/a>\n        <\/div>\n        <div class=\"col-8 col-md-12\">\n            <div class=\"article__badge article__badge--sm \">\n\t\t\t\t <a class=\"article__badge article__badge--sm\" href=\"\/news\/technology-news\/\"> Technology News <\/a>\t\t    \t<div class=\"article__badge-date d-md-inline-block\" data-utctime=\"2023-09-29 08:42:00\">&bull; Sep 29, 2023<\/div>\n\t\t    <\/div>\n\t\t    <a href=\"\/news\/could-chatgpts-latest-enhancement-herald-revolutionary-phase-for-crypto.htm\" class=\"article__title article__title--md article__title--featured\">\n\t\t      <h4>Could ChatGPT's Latest Enhancement Herald a Revolutionary Phase for Crypto?<\/h4>\n\t\t    <\/a>\n        <\/div>\n    <\/div>\n<\/article>\n",
        )


    #     # newstechnology1 = json.dumps(newstechnology, ensure_ascii=False)
    #     # with open('html/paged/newstechnology-news-1.json', "w") as file:
    #     #     # for i in newstechnology:
    #     #     file.write(newstechnology1)
    #
    with open('html/paged/newstechnology-news-1.json', 'w') as f:
        json.dump(newstechnology, f)

    # with open('html/paged/newstechnology-news-1.json', 'w', encoding='utf8') as json_file:
    #     json.dump(newstechnology, json_file, ensure_ascii=False)

    count_replace = 1
    for currentpath, folders, files in os.walk('html/ku'):
        # for currentpath, folders, files in os.walk('html/topic/houses-1.html'):
        for file in files:
            # if '.jpg' not in file and '.png' not in file and '.svg' not in file and '.gif' not in file and '.css' not in file and '.js' not in file and '.ico' not in file and '.woff2' not in file and '.woff' not in file:
            ku = (os.path.join(currentpath, file))
            print(str(count_replace) + ' ' + ku)
            with open(ku) as file1:
                try:
                    read_file = file1.read()
                except Exception as e:
                    print(e)
            pass

            # read_file = decompose_tags(read_file)
            read_file = replace_text(read_file, newsapi)
            # read_file = replace_text_1(read_file)

            # read_file = replace_links(read_file)

            count_replace = count_replace + 1

            with open(ku, "w") as file1:
                file1.write(read_file)

    finish_time = time.time() - start_time
    finish_time = round(finish_time / 60, 2)

    print('copied ' + str(count_replace) + ' files, time taken ' + str(finish_time) + ' min')

    with open('count_replace.txt', "a") as file:
        file.write(todaytime + ' files ' + str(count_replace) + ', time ' + str(finish_time) + ' min\n')


if __name__ == '__main__':
    main()
