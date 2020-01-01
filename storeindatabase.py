import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client['test']
coll_pro = db['property']
coll_comment = db['comment']


def write_pro(list_proper):  # proper 是抓取下来的游戏特性，是列表
    dic_proper = {'id': list_proper[0], 'href': list_proper[1], 'href_pic': list_proper[2],
                  'discount': list_proper[3], 'origin_price': list_proper[4], 'discount_price': list_proper[5],
                  'game_name': list_proper[6], 'needVR': list_proper[7], 'supportVR': list_proper[8]}
    condition = {'id': dic_proper.id}
    coll_pro.update(condition, dic_proper)


def write_comment(comment):
    if coll_comment.find_one(comment) is None:
        coll_comment.insert(comment)


def find_pro(game_name):  # game_name 是字符串，返回值是字典，就是储存的内容。
    return coll_pro.find_one(game_name)


def find_comment(comment_name):  # comment_name 是字符串，返回值是字典，一个是评论内容，一个是评论数目
    comment = coll_comment.find(comment_name)
    count = coll_comment.find(comment_name).count()
    res = {'comment': comment, 'count': count}
    return res
