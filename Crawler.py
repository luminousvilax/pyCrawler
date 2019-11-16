import re
import requests
from requests import RequestException
import time
from bs4 import BeautifulSoup
import bs4.element
import csv

def get_a_page(url):
    print("Get the page connection……")
    try:
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Done.")
            return response.text
        else:
            return None
    except RequestException as e:
        print (e)
        return None

def parse_a_page(html):
    print("Parse a page……")
    items=[]
    sp = BeautifulSoup(html,'lxml')
    attrs = ['data-ds-appid','href','src']
    nodes = sp.findAll('a',attrs={'class':'tab_item'})
    for node in nodes:
        items.append(parse_a_node(node,attrs))
    print("Done.")
    #print(items)
    write_to_file(items)
        
def parse_a_node(node,attrs):
    item = {}
    if(isinstance(node,bs4.element.NavigableString)):
        pass
    elif (node.string != None):
        item[node.attrs['class'][0]] = node.string
    else:
        for attr in attrs:
            if (attr in node.attrs.keys()):
                item[attr] = node.attrs[attr]
        for i,child in enumerate(node.children):
            subitem = parse_a_node(child,attrs)
            if (item.get('top_tag') == None or subitem.get('top_tag') == None):
                item.update(subitem)
            else:
                item['top_tag'] += subitem['top_tag']
    return item

def write_to_file(records):
    print("Write to file……")
    with open('D:/test.csv','w',encoding='utf-8',newline='') as f:
        headers = ['data-ds-appid','href','src','discount_pct','discount_original_price','discount_final_price','tab_item_name','vr_required','vr_supported','top_tag']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(records)
        print("Done.")

def main():
    url = 'https://store.steampowered.com/specials#p=5&tab=TopSellers'
    html = get_a_page(url)
    parse_a_page(html)

if __name__ == '__main__':
    main()
    print('Get information successfully!')
