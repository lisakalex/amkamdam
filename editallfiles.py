#!/home/al/.amkamdam/bin/python3
import glob2
from bs4 import BeautifulSoup
import time
import shutil
from datetime import datetime

# https://beautiful-soup-4.readthedocs.io/en/latest/

start_time = time.time()
shutil.copytree('./replace/', './a/cryptonews.com/', dirs_exist_ok=True)


# noinspection PyInterpreter
def replace_header_footer(read_file1):
    with open('replace/me-index.xhtml', 'r', encoding='utf-8') as file1:
        soup = BeautifulSoup(file1.read(), features="html.parser")

    head = soup.find("head")
    header = soup.find("header")
    footer = soup.find("footer")

    soup1 = BeautifulSoup(read_file1, features="html.parser")

    header1 = soup1.find("head")
    if header1:
        header1.replace_with(head)

    header1 = soup1.find("header")
    if header1:
        header1.replace_with(header)

    footer1 = soup1.find("footer")
    if footer1:
        footer1.replace_with(footer)

    return str(soup1)




# with open("index.html") as file:
#     read_file = file.read()
#
# read_file = replace_header_footer(read_file)
# # read_file = insert_in_head(read_file)
# # count_replace = count_replace + 1
#
# with open("index-1.html", "w") as file:
#     file.write(read_file)

files = ['html', 'htm']
count_replace = 1
with open('replaced', "w", encoding='utf-8') as file:
    file.write('')

for fl in files:
    for filepath in glob2.iglob('./a/cryptonews.com/**/*.' + fl, recursive=True):
        print(str(count_replace) + ' ' + filepath)
        todaytime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        with open('replaced', "a", encoding='utf-8') as file:
            file.write(todaytime + ' ' + str(count_replace) + ' ' + filepath + '\n')

        with open(filepath, 'r', encoding='utf-8') as file:
            read_file = file.read()

        read_file = replace_header_footer(read_file)
        # read_file = insert_in_head(read_file)
        count_replace = count_replace + 1

        with open(filepath, "w", encoding='utf-8') as file:
            file.write(read_file)

shutil.rmtree('./html', ignore_errors=True)
shutil.copytree('./a/cryptonews.com/', './html/', dirs_exist_ok=True)
shutil.rmtree('./a/cryptonews.com', ignore_errors=True)

finish_time = time.time() - start_time
finish_time = round(finish_time / 60, 2)

print('copied ' + str(count_replace) + ' files, time taken ' + str(finish_time) + ' min')

todaytime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
with open('count_replace', "a", encoding='utf-8') as file:
    file.write('\n' + todaytime + ' files ' + str(count_replace) + ', time ' + str(finish_time) + ' min\n')

with open('replaced', "a", encoding='utf-8') as file:
    file.write(todaytime + ' files ' + str(count_replace) + ', time ' + str(finish_time) + ' min\n')

ha = None
