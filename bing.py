import os
import re
import requests
from multiprocessing import Pool
import threadpool
import hashlib


GET_KEY_PATH = 'D:/chenyan/爬虫关键字/必应.txt'
SAVE_PIC_PATH = 'D:/chenyan/图片下载/'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36'
}


# 获取文件夹中关键字
def get_keyword():
    if os.path.exists(GET_KEY_PATH):
        with open(GET_KEY_PATH, 'r') as f:
            keywords = f.readlines()
    else:
        print('文件夹不存在')
    return keywords


def get_img(keyword):
    base_url = 'https://cn.bing.com/images/async?'
    for page_num in range(1, 100):
        data = {
            "q": keyword,
            "first": str(page_num * 35),
            "count": "35",
            "relp": str(page_num * 35),
            "qft": " filterui:imagesize-wallpaper",
            "scenario": "ImageBasic",
            "datsrc": "N_I",
            "layout": "ColumnBased",
            "mmasync": "1",
            "dgState": "c*4_y*2760s2686s2747s2630_i*60_w*197",
            "IG": "2FF8956B884E430F8259AAD338D7FF36",
            "SFX": str(page_num),
            "iid": "images.5234"
        }
        try:
            response = requests.get(base_url, params=data, headers=headers)
            a = re.findall(r'murl&quot;:&quot;http://([\s\S]*?)&', response.text)
            for i in a:
                download(keyword, i)
        except Exception as e:
            print(e)
            pass


def download(keyword, url):
    try:
        finally_url = 'http://' + url
        folder = GET_KEY_PATH.split('/')[-1].split('.')[0]
        if not os.path.exists(SAVE_PIC_PATH + folder):
            os.mkdir(SAVE_PIC_PATH + folder)
        if not os.path.exists(SAVE_PIC_PATH + folder + '/' + keyword):
            os.mkdir(SAVE_PIC_PATH + folder + '/' + keyword)
        response = requests.get(finally_url, headers=headers)
        m = hashlib.md5()
        m.update(response.content)
        file_md5 = m.hexdigest()
        if not os.path.exists(SAVE_PIC_PATH + folder + '/' + keyword + '/' + file_md5 + '.jpg'):
            with open(SAVE_PIC_PATH + folder + '/' + keyword + '/' + file_md5 + '.jpg', 'wb') as f:
                f.write(response.content)
                print(keyword, '--------->>', file_md5, '--------->>', '图片下载成功')
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    keywords = get_keyword()
    pool = Pool(2)
    for keyword in keywords:
        keyword = keyword.strip()
        pool.apply_async(get_img, (keyword,))
    pool.close()
    pool.join()