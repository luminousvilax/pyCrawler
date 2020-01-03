import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['test']
coll_pro = db['property']
coll_comment = db['comment']


def write_pro(list_proper):  # proper 是抓取下来的游戏特性，是字典
    dic_proper = {'id': list_proper['data-ds-appid'], 'href': list_proper['href'], 'href_pic': list_proper['src'],
                  'discount': list_proper['discount_pct'], 'origin_price': list_proper['discount_original_price'],
                  'discount_price': list_proper['discount_final_price'], 'game_name': list_proper['tab_item_name'],
                  'needVR': list_proper['vr_required'], 'supportVR': list_proper['vr_supported']}
    # print(dic_proper)
    condition = {'id': dic_proper['id']}
    if coll_pro.find_one(condition) is None:
        coll_pro.insert(dic_proper)
    else:
        coll_pro.update(condition, dic_proper)


def write_comment(comment):
    if coll_comment.find_one(comment) is None:
        coll_comment.insert(comment)


def find_pro(game_id):  # game_name 是字符串，返回值是字典，就是储存的内容。
    result = coll_pro.find_one({'id': str(game_id)})
    return result


def find_comment(game_id):  # comment_name 是字符串，返回值是字典，一个是评论内容，一个是评论数目
    comment = coll_comment.find({'id': str(game_id)})
    count = coll_comment.find({'id': str(game_id)}).count()
    res = {'comment': comment, 'count': count}
    return res


def print_result(game_id):
    filename = 'database_result.csv'
    f = open(filename, 'w', encoding='utf-8')
    proper = find_pro(game_id)
    compound = find_comment(game_id)
    count=compound['count']
    comments=compound['comment']
    f.write(str(proper) + '\n')
    f.write('\n')
    f.write('The number of comments is:' + str(count) + '\n')
    for comment in comments:
        print(comment)
        f.write(str(comment) + '\n')
    f.close()




def main():
    game_id = input('Please input the game id you want to search for: ')
    print_result(game_id)


if __name__ == '__main__':
    main()
    print('Print information to file successfully!')
