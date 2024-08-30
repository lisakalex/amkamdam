#!/home/al/.venv/bin/python3
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta, date
import os
import json

# https://beautiful-soup-4.readthedocs.io/en/latest/

start_time = time.time()
todaytime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


# newsapi = ''


def replace_text(read_file1, path_file1):
    path_file1_list = path_file1.split('/')
    keyword = path_file1_list[len(path_file1_list) - 2]
    # y = date.today() - timedelta(days=1)
    # yesterday = y.strftime('%Y-%m-%d')
    # url = ('https://newsapi.org/v2/everything?'
    #        'q=' + keyword +
    #        '&' + yesterday +
    #        '&sortBy=publishedAt'
    #        '&language=en'
    #        '&apiKey=41e2e097fbb4457c9b714ee6acd4185b')
    #
    # newsapi = json.loads(requests.get(url).text)

    with open('test/newsapi-2024-08-28.json', "r") as f:
        newsapi = json.load(f)

    newsapi_articles = newsapi['articles']
    soup = BeautifulSoup(read_file1, features='html.parser')
    section = soup.find_all('article', class_='mb-15 mb-sm-30 article-item')
    try:
        for i in range(0, 4):
            article = section[i]
            link = article.find('a', class_='article__image')
            link['href'] = newsapi_articles[i]['url']

            img = article.find('img')
            img['src'] = newsapi_articles[i]['urlToImage']
            img['srcset'] = ''
            img['alt'] = newsapi_articles[i]['title']

            badge_date = article.find('div', class_='article__badge-date')
            badge_date['data-utctime'] = newsapi_articles[i]['publishedAt']

            link1 = article.find('a', class_='article__title')
            link1['href'] = newsapi_articles[i]['url']
            link1.string = newsapi_articles[i]['title']
            article.find_all('div')[6].string = newsapi_articles[i]['content']

        del newsapi_articles[0:4]
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-12 mb-20')
        for i in range(0, 5):
            # n = newsapi['articles'][i]
            article = section[i]
            link = article.find('a', class_='article__image')
            link['href'] = newsapi_articles[i]['url']

            img = article.find('img')
            img['src'] = newsapi_articles[i]['urlToImage']
            img['srcset'] = ''
            img['alt'] = newsapi_articles[i]['title']

            badge_date = article.find('div', class_='article__badge-date')
            badge_date['data-utctime'] = newsapi_articles[i]['publishedAt']

            link1 = article.find('a', class_='article__title')
            link1['href'] = newsapi_articles[i]['url']
            link1.string = newsapi_articles[i]['title']
            # article.find_all('div')[6].string = n['content']

        del newsapi_articles[0:5]
        section = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 col-xl-3 mb-30')
        for i in range(0, 16):
            # n = newsapi['articles'][i]
            article = section[i]
            link = article.find('a', class_='article__image')
            link['href'] = newsapi_articles[i]['url']

            img = article.find('img')
            img['src'] = newsapi_articles[i]['urlToImage']
            img['srcset'] = ''
            img['alt'] = newsapi_articles[i]['title']

            badge_date = article.find('div', class_='article__badge-date')
            badge_date['data-utctime'] = newsapi_articles[i]['publishedAt']

            link1 = article.find('a', class_='article__title')
            link1['href'] = newsapi_articles[i]['url']
            link1.string = newsapi_articles[i]['title']

        del newsapi_articles[0:16]
    except Exception as e:
        print(e)
    pass

    with open(path_file1, "w") as file1:
        file1.write(str(soup))

    with open('article.html', 'r') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    paged = []
    for i in newsapi['articles']:
        link = soup.find('a', class_='article__image')
        link['href'] = i['url']

        img = soup.find('img')
        img['src'] = i['urlToImage']
        img['srcset'] = ''
        img['alt'] = i['title']

        badge_date = soup.find('div', class_='article__badge-date')
        badge_date['data-utctime'] = i['publishedAt']

        link1 = soup.find('a', class_='article__title')
        link1['href'] = i['url']
        link1.string = i['title']
        paged.append(str(soup))

    with open('html/paged/' + keyword + '-1.json', 'w') as f:
        json.dump(paged, f)


# def paged(read_file, file):
# #     y = date.today() - timedelta(days=1)
# #     yesterday = y.strftime('%Y-%m-%d')
# #     keyword = file.replace('-1.json', '')
# #     url = ('https://newsapi.org/v2/everything?'
# #            'q=' + keyword +
# #            '&' + yesterday +
# #            '&sortBy=publishedAt'
# #            '&language=en'
# #            '&apiKey=41e2e097fbb4457c9b714ee6acd4185b')
#
# # newsapi = json.loads(requests.get(url).text)
#
# # with open('test/newsapi.json', "r") as f:
# #     newsapi = json.load(f)
#
#     with open('article.html', 'r') as file1:
#         soup = BeautifulSoup(file1.read(), features="html.parser")
#
#     for i in newsapi['articles']:
#         link = soup.find('a', class_='article__image')
#         link['href'] = i['url']
#
#         img = soup.find('img')
#         img['src'] = i['urlToImage']
#         img['srcset'] = ''
#         img['alt'] = i['title']
#
#         badge_date = soup.find('div', class_='article__badge-date')
#         badge_date['data-utctime'] = i['publishedAt']
#
#         link1 = soup.find('a', class_='article__title')
#         link1['href'] = i['url']
#         link1.string = i['title']
#         read_file.append(str(soup))
#
#     with open(path_file, 'w') as f:
#         json.dump(read_file, f)

# with open('test/newsapi-original.json', 'w') as f:
#     f.write(requests.get(url).text)

# print(str(count_replace) + ' ' + file)
# count_replace = count_replace + 1
#
# finish_time = time.time() - start_time
# finish_time = round(finish_time / 60, 2)
#
# print('copied paged' + str(count_replace - 1) + ' files, time taken ' + str(finish_time) + ' min')
#
# with open('count_replace.txt', "a") as file:
#     file.write(todaytime + 'paged files ' + str(count_replace - 1) + ', time ' + str(finish_time) + ' min\n')
#
# return read_file


def main():
    # count_replace = 1
    # for currentpath, folders, files in os.walk('html/paged'):
    #     for file in files:
    #         path_file = (os.path.join(currentpath, file))
    #         read_file = []
    #         with open(path_file) as file1:
    #             try:
    #                 read_file = json.load(file1)
    #             except Exception as e:
    #                 print(e)
    #             pass
    #
    #         read_file = paged(read_file, file)
    #         with open(path_file, 'w') as f:
    #             json.dump(read_file, f)
    #
    #         print(str(count_replace) + ' ' + file)
    #         count_replace = count_replace + 1
    #
    # finish_time = time.time() - start_time
    # finish_time = round(finish_time / 60, 2)
    #
    # print('copied paged' + str(count_replace - 1) + ' files, time taken ' + str(finish_time) + ' min')
    #
    # with open('count_replace.txt', "a") as file:
    #     file.write(todaytime + 'paged files ' + str(count_replace - 1) + ', time ' + str(finish_time) + ' min\n')

    count_replace = 1
    for currentpath, folders, files in os.walk('html/ku'):
        for file in files:
            if '.jpg' not in file and '.jpeg' not in file and '.png' not in file and '.svg' not in file and '.gif' not in file and '.css' not in file and '.js' not in file and '.ico' not in file and '.woff2' not in file and '.woff' not in file:
                path_file = (os.path.join(currentpath, file))
                with open(path_file) as file1:
                    try:
                        read_file = file1.read()
                    except Exception as e:
                        print(e)
                pass

                replace_text(read_file, path_file)

                # with open(path_file, "w") as file1:
                #     file1.write(read_file)

                print(str(count_replace) + ' ' + path_file)
                count_replace = count_replace + 1

    finish_time = time.time() - start_time
    finish_time = round(finish_time / 60, 2)

    print('copied ' + str(count_replace - 1) + ' files, time taken ' + str(finish_time) + ' min')

    with open('count_replace.txt', "a") as file:
        file.write(todaytime + ' files ' + str(count_replace - 1) + ', time ' + str(finish_time) + ' min\n')


if __name__ == '__main__':
    main()
