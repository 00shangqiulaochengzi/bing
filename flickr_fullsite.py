import json
import requests
import os
import flickrapi
from lxml import etree
import urllib3
import pymysql


requests.packages.urllib3.disable_warnings()
api_key = 'db56b3d45e96eed2a704242c9efa8bac'
api_secret = 'c25d9296319b105f'
flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)
base_url = 'https://www.flickr.com/people/13827054@N03/contacts/?filter=&page=1'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36'
}


def get_user_id():
    user_id_list = []
    response = requests.get(base_url, headers=headers, verify=False)
    html = etree.HTML(response.text)
    user_imgs = html.xpath('//img/@src')
    for user_img in user_imgs:
        if 'staticflickr.com' in user_img:
            user_id = user_img.split('#')[-1]
            user_id_list.append(user_id)
    # print(user_id_list)
    save2Mysql(user_id_list)


def save2Mysql(user_id_list):
    db = pymysql.connect("localhost", "root", "123456", "chenyan", charset='utf8')
    cursor = db.cursor()
    for user_id in user_id_list:
        sql = "insert into flickr_user_id(user_id) value('%s')"%(user_id)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    cursor.close()
    db.close()


if __name__ == '__main__':
    get_user_id()