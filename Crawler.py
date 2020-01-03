import re
import requests
from requests import RequestException
import time
from bs4 import BeautifulSoup
import bs4.element
import csv
import storeindatabase
from game_review import get_review

def get_a_page(url):
    print("Get the page connection……")
    try:
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Done.")
            return response.json()
        else:
            return None
    except RequestException as e:
        print(e)
        return None


def parse_a_page(json):
    print("Parse a page……")
    items = []
    result_html = json.get('results_html')
    sp = BeautifulSoup(result_html, 'lxml')
    attrs = ['data-ds-appid', 'href', 'src']
    nodes = sp.findAll('a', attrs={'class': 'tab_item'})
    # print(nodes[0]['href'])
    for node in nodes:
        if 'sub' in node['href']:
            continue
        items.append(parse_a_node(node, attrs))
    print("Done.")
    return items


def parse_a_node(node, attrs):
    item = {}
    if (isinstance(node, bs4.element.NavigableString)):
        pass
    elif (node.string != None):
        item[node.attrs['class'][0]] = node.string
    else:
        for attr in attrs:
            if (attr in node.attrs.keys()):
                item[attr] = node.attrs[attr]
        for i, child in enumerate(node.children):
            subitem = parse_a_node(child, attrs)
            if (item.get('top_tag') == None or subitem.get('top_tag') == None):
                item.update(subitem)
            else:
                item['top_tag'] += subitem['top_tag']
    return item


def write_to_file(records):
    print("Write to file……")
    with open('test.csv', 'w', encoding='utf-8-sig', newline='') as f:
        headers = ['data-ds-appid', 'href', 'src', 'discount_pct', 'discount_original_price', 'discount_final_price',
                   'tab_item_name', 'vr_required', 'vr_supported', 'top_tag']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(records)
        print("Done.")


def main():
    # url = 'https://store.steampowered.com/contenthub/querypaginated/specials/TopSellers/render/?query=&start=0&count=15&cc=US&l=schinese&v=4&tag='
    items = []
    url_base = 'https://store.steampowered.com/contenthub/querypaginated/specials/TopSellers/render/?query=&start='
    pages = input('Please enter pages you want to get: ')
    for i in range(int(pages)):
        url = url_base + str(i * 15) + '&count=15&cc=US&l=schinese&v=4&tag='
        html = get_a_page(url)
        for item in parse_a_page(html):
            items.append(item)
            get_review(item.get('href'))
            

    # print(items)
    write_to_file(items)
    fr = open('test.csv', 'r', encoding='utf-8')
    headers = ['data-ds-appid', 'href', 'src', 'discount_pct', 'discount_original_price', 'discount_final_price',
               'tab_item_name', 'vr_required', 'vr_supported', 'top_tag']
    reader = csv.DictReader(fr, headers)
    for i in reader:
        print(i)
        storeindatabase.write_pro(i)


if __name__ == '__main__':
    main()
    print('Get information successfully!')
