# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib
import socket
import re


game_url = input("Input Game's URL:")
game_id = re.search('https://store.steampowered.com/app/(.+?)/', game_url)[1]
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
}

proxies = { 
    "http": "http://127.0.0.1:1087", 
    "https": "https://127.0.0.1:1087"
}

# print(review_html)

filename = 'game_review.csv'
f = open(filename, 'w', encoding = 'utf-8')

csv_headers = "Helpful, Recommend, Hours, Posted_Date, Text, User, Game_Number\n"
f.write(csv_headers)

offset = 0

while True:

    if offset == 20:
        break 
    game_review_url = 'https://steamcommunity.com/app/' + game_id + '/homecontent/?userreviewsoffset=' + str(10 * (offset - 1)) + '&p=' + str(offset) + \
        '&workshopitemspage=' + str(offset) + '&readytouseitemspage=' + str(offset) + '&mtxitemspage=' + str(offset) + '&itemspage=' + str(offset) + \
        '&screenshotspage=' + str(offset) + '&videospage=' + str(offset) + '&artpage=' + str(offset) + '&allguidepage=' + str(offset) + '&webguidepage=' + \
        str(offset) + '&integratedguidepage=' + str(offset) + '&discussionspage=' + str(offset) + '&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=433850&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1'
    try:
        review_html = requests.get(game_review_url, headers = headers, timeout = 10, proxies = proxies).text
    except urllib.error.URLError as e:
        break
    review_page_soup = BeautifulSoup(review_html, 'lxml')
    review_list = review_page_soup.findAll('div', {'class': 'apphub_Card modalContentLink interactable'})

    for single_review in review_list:
        
        found_helpful = single_review.find('div', {'class' : 'found_helpful'}).text.strip()
        #推荐 / 不推荐
        title = single_review.find('div', {'class': 'title'}).text.strip()
        #游戏时间
        hours = single_review.find('div', {'class': 'hours'}).text
        hours = re.search('总时数(.+?)小时', hours)
        hours = hours[1].strip()
        hours = str.replace(hours, ',', '')
        review_text_and_date_posted = single_review.find('div', {'class': 'apphub_CardTextContent'})
        #评论日期
        review_data_posted = review_text_and_date_posted.div.text.strip()
        review_data_posted = re.search('(\d+)年(\d+)月(\d+)日', review_data_posted)
        review_data_posted = '-'.join([review_data_posted[i] for i in range(1, 4)])
        #评论文字
        review_text = review_text_and_date_posted.text.strip()
        review_text = re.search('\n(.*?)$', review_text)[1].strip()
        review_text = str.replace(review_text, ',', ' ')
        #用户信息
        user_profile = single_review.find('div', 'apphub_friend_block')
        user_name = user_profile.a.text
        number_text = user_profile.find('div', {'class': 'apphub_CardContentMoreLink ellipsis'}).text
        game_number = re.search('有(.+?)项', number_text)[1].strip()

        f.write(found_helpful + ',' + title + ',' + hours + ',' + review_data_posted + \
            ',' + review_text + ',' + user_name + ',' + game_number + '\n')
    
    print("Scrape page:", offset + 1)
    offset += 1


f.close()