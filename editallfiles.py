#!/home/al/.venv/bin/python3
import glob2
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
import shutil
from datetime import datetime
import os

# https://beautiful-soup-4.readthedocs.io/en/latest/

start_time = time.time()
todaytime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

shutil.rmtree('./b/', ignore_errors=True)
shutil.rmtree('./public_html', ignore_errors=True)
shutil.copytree('./a/cryptonews.com', './b/', dirs_exist_ok=True)
shutil.copytree('./replace/', './b/', dirs_exist_ok=True)
shutil.rmtree('./b/tags/', ignore_errors=True)
shutil.rmtree('./b/events/', ignore_errors=True)
shutil.rmtree('./b/jobs/', ignore_errors=True)
shutil.rmtree('./b/price-tracker/', ignore_errors=True)
shutil.rmtree('./b/videos/', ignore_errors=True)

# fix exclusives
if os.path.exists('./b/exclusives/index.html'):
    os.remove('./b/exclusives/index.html')
else:
    print("The file does not exist")

shutil.copyfile('./b/exclusives/features/index.html', './b/exclusives/index.html')

with open('./b/exclusives/index.html', 'r') as file:
    soup = BeautifulSoup(file.read(), features="html.parser")
    breadcrumbs = soup.find('div', class_='breadcrumbs')
    breadcrumbs = breadcrumbs.findAll("a")

if breadcrumbs[2]:
    breadcrumbs[2].decompose()

with open('./b/exclusives/index.html', "w") as file:
    file.write(str(soup))

# delete section guides in /index.html
with open('./b/index.html', 'r') as file:
    soup = BeautifulSoup(file.read(), features="html.parser")

guides = soup.find('section', class_='container-fluid')
if guides is not None:
    guides.decompose()

with open('./b/index.html', "w") as file:
    file.write(str(soup))


# fix Recommended to do
with open('./me-index.html', 'r') as file:
    soup = BeautifulSoup(file.read(), features="html.parser")
    recommended = soup.find('a', class_='heading')
    breadcrumbs = recommended.findAll("a")

if breadcrumbs[2]:
    breadcrumbs[2].decompose()

with open('./b/exclusives/index.html', "w") as file:
    file.write(str(soup))


def replace_header_footer(read_file1):
    with open('./me-index.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    head = soup.find("head")
    header = soup.find("header")
    footer = soup.find("footer")

    soup1 = BeautifulSoup(read_file1, features="html.parser")

    head1 = soup1.find("head")
    if head1:
        head1.replace_with(head)

    header1 = soup1.find("header")
    if header1:
        header1.replace_with(header)

    footer1 = soup1.find("footer")
    if footer1:
        footer1.replace_with(footer)

    return str(soup1)


def replace_links(read_file1):
    soup = BeautifulSoup(read_file1, features="html.parser")
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href:
            if '/ext/' in href:
                href = href.replace('/ext/', 'https://cryptonews.com/ext/')
                link['href'] = href

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


def decompose_tags(read_file1):
    soup = BeautifulSoup(read_file1, features='html.parser')

    newsletter = soup.find('div', class_='newsletter')
    if newsletter:
        newsletter.decompose()

    newsletter_modal = soup.find('div', class_='modal')
    if newsletter_modal:
        newsletter_modal.decompose()

    iframes = soup.findAll('iframe')
    for iframe in iframes:
        if iframe:
            iframe.parent.decompose()

    widget_containers = soup.findAll('div', id='widget_container')
    for widget_container in widget_containers:
        if widget_container:
            widget_container.decompose()

    scripts = soup.findAll('script')
    for script in scripts:
        if script:
            script.decompose()

    socials = soup.findAll('div', class_='socials')
    for social in socials:
        if social:
            social.decompose()

    twitter = soup.find_all("h2")
    for t in twitter:
        if 'Twitter' in t.text:
            t.decompose()

    tags_links = soup.find_all("a")
    for t in tags_links:
        if t.has_attr('href'):
            if '/tags/' in t['href']:
                t.decompose()

    videos = soup.find_all("section")
    for v in videos:
        videosh2 = v.find("h2")
        if videosh2 is not None:
            if 'Videos' in videosh2.text:
                v.decompose()

    return str(soup)


def insert_ads(read_file1):
    with open('me-index.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    soup1 = BeautifulSoup(read_file1, features='html.parser')

    #  add page loading gif
    se_pre_con = soup.find('div', class_='se-pre-con')
    if soup1.body is not None:
        soup1.body.insert(1, se_pre_con)

    for dslot in soup1.findAll('div', class_='dslot'):
        for medslot in soup.findAll('div', class_='dslot'):
            if dslot.get('did') == medslot.get('did'):
                dslot.replace_with(medslot)

    return str(soup1)


def replace_text(read_file1):
    read_file1 = read_file1.replace('cryptonews', '<data class="replace-1" value=""></data>')
    read_file1 = read_file1.replace('Cryptonews', '<data class="replace-2" value=""></data>')
    read_file1 = read_file1.replace('CryptoNews', '<data class="replace-3" value=""></data>')
    read_file1 = read_file1.replace('CRYPTONEWS', '<data class="replace-4" value=""></data>')
    read_file1 = read_file1.replace('Crypto News', '<data class="replace-5" value=""></data>')
    return read_file1


files = ['html', 'htm']
count_replace = 1

for fl in files:
    for filepath in glob2.iglob('./b/**/*.' + fl, recursive=True):
        print(str(count_replace) + ' ' + filepath)
        with open(filepath) as file:
            read_file = file.read()

        # download_json_files(read_file)
        read_file = replace_text(read_file)
        read_file = replace_links(read_file)
        read_file = decompose_tags(read_file)
        read_file = replace_header_footer(read_file)
        read_file = insert_ads(read_file)
        count_replace = count_replace + 1

        with open(filepath, "w") as file:
            file.write(read_file)

shutil.copytree('./b/', './public_html/', dirs_exist_ok=True)
finish_time = time.time() - start_time
finish_time = round(finish_time / 60, 2)

print('copied ' + str(count_replace) + ' files, time taken ' + str(finish_time) + ' min')

with open('count_replace.txt', "a") as file:
    file.write(todaytime + ' files ' + str(count_replace) + ', time ' + str(finish_time) + ' min\n')

ha = None
