from lxml import etree
import requests
import json
from urllib import parse
import math
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import re
import random
import time

ips = [{"ip":"58.218.92.171","port":"19095"},{"ip":"58.218.214.142","port":"17455"},{"ip":"119.7.153.36","port":"4378"},{"ip":"58.218.92.169","port":"19646"},{"ip":"106.6.235.135","port":"4345"},{"ip":"58.218.214.154","port":"15747"},{"ip":"58.218.92.78","port":"18410"},{"ip":"114.230.64.20","port":"4326"},{"ip":"58.218.214.147","port":"13398"},{"ip":"58.218.92.75","port":"18621"}]
proxies = [{'https': '58.218.92.171:19095'},
{'https': '58.218.214.142:17455'},
{'https': '119.7.153.36:4378'},
{'https': '58.218.92.169:19646'},
{'https': '106.6.235.135:4345'},
{'https': '58.218.214.154:15747'},
{'https': '58.218.92.78:18410'},
{'https': '114.230.64.20:4326'},
{'https': '58.218.214.147:13398'},
{'https': '58.218.92.75:18621'}]

timeout = 5
headers = {
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
     "cookie": "RK=FADdoZ6pc6; ptcz=f958c1d5fe4e177576f73c8a1de65f7a47f49d730c97614bdc6e59e42c020a38; pgv_pvid=3915876096; pgv_pvi=3685343232; tvfe_boss_uuid=7bfa8cbb0363bba5; o_cookie=614000736; _ga=amp-fymc5eazEyOMQ41828Sx2w; eas_sid=l1j5b7775677R0X0P6d5b3M312; ied_qq=o0614000736; pgv_si=s3499580416; pgv_info=ssid=s5398318358; ts_refer=www.baidu.com/link; ts_uid=6650280698; yqq_stat=0; userAction=1; qqmusic_uin=0614000736; qqmusic_key=@x242u9Bnt; qqmusic_fromtag=6; ts_last=y.qq.com/portal/singer_list.html",
    'origin': 'https://y.qq.com',

}

USER_AGENTS = [
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'
]

def get_random_head():
    headers_new = headers
    choice = random.choice(USER_AGENTS)
    headers_new['agent'] = choice
    return headers_new


data =  '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":%d,"sin":%d,"cur_page":%d}}}' %(1,0,1)
url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI8410120336851343&' \
      'g_tk=392074887&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
      'notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(data))

# 拿到每个分区下，有多少页
def get_Page(url):
    print("get_Page....begin.....")
    try:
        proxy = random.choice(proxies)
        headers_new = get_random_head()
        response = requests.get(url,timeout=timeout,headers=headers_new,proxies=proxy).json()
        total = response['singerList']['data']['total']
        page_size = len(response['singerList']['data']['singerlist'])
        # print("total:{},page_size:{}".format(total,page_size))
        page_count = math.ceil(total / page_size) # 拿到每个分区的页数
        print("get_Page ......Done")
        return page_count
    except:
        print("get_Page{}....timeout.....".format(url))
        return 0


# 给定哪一页，拿到该页下所有歌手
def get_SingerId(url):
    print("get_SingerId....begin.....")
    singers = []
    try:
        proxy = random.choice(proxies)
        headers_new = get_random_head()
        response = requests.get(url,timeout=timeout,headers=headers_new,proxies=proxy).json()
        singerlist = response['singerList']['data']['singerlist']
        for singer in singerlist:
            singer_mid = singer['singer_mid']
            # print(singer_mid)
            singers.append(singer_mid)
        print("get_SingerId ......Done")
        time.sleep(0.5)
    except:
        pass
    return singers

def get_ZoneSingers(zone):
    print("get_ZoneSingers....begin.....")
    data =  '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list",' \
                '"param":{"area":-100,"sex":-100,"genre":-100,"index":%d,"sin":%d,"cur_page":%d}}}' %(zone,0,1)
    url =  'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI8410120336851343&' \
      'g_tk=392074887&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
      'notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(data))
    page_count = get_Page(url) # 每个分区下面的页数
    singers = []
    sin = 0
    for page in range(1,page_count+1):
        # 拿到每一页下面的歌手ID
        data =  '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list",' \
              '"param":{"area":-100,"sex":-100,"genre":-100,' \
                '"index":%d,"sin":%d,"cur_page":%d}}}' %(zone,sin,page)

        url =  'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI8410120336851343&' \
      'g_tk=392074887&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
      'notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(data))
        singer_of_page = get_SingerId(url)
        singers.append(singer_of_page)
        sin += 80

        # if page > 2:
        #     break
    print("get_ZoneSingers ......Done")
    time.sleep(0.5)
    return singers






# 给定歌手，拿到该歌手的所有歌曲
def get_Song(singer):
    print("get_Song....begin.....")
    begin = 0
    num = 1
    data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
           '"param":{"order":1,"singerMid":"%s","begin":%d,"num":%d},"module":"musichall.song_list_server"}}' %(singer,begin,num)

    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9621321373752951&g_tk=1140163968&loginUin=0&hostUin=0&' \
          'format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(data)
    try:
        proxy = random.choice(proxies)
        headers_new = get_random_head()
        response = requests.get(url,timeout=timeout,headers=headers_new,proxies=proxy).json()
        total = response['singerSongList']['data']['totalNum']
        songs = []
        while begin+num < total:
            num = 80
            data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
               '"param":{"order":1,"singerMid":"%s","begin":%d,"num":%d},"module":"musichall.song_list_server"}}' %(singer,begin,num)

            url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9621321373752951&g_tk=1140163968&loginUin=0&hostUin=0&' \
              'format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(data)
            response = requests.get(url,timeout=timeout,headers=headers_new).json()
            songList = response['singerSongList']['data']['songList']
            for song in songList:
                songs.append(song['songInfo']['name'])
            begin = begin + num
        url_singer = "https://y.qq.com/n/yqq/singer/{}.html".format(singer)
        response_2 = requests.get(url_singer,timeout=timeout,headers=headers_new).text
        html = etree.HTML(response_2)
        name = html.xpath("//head/title/text()")[0]
        name = re.split(r'-',name)[0]
        with open("music.txt",'a+',encoding='utf8') as f:
            f.write(str({"name":name,"songs":songs}) + '\n')
        print("{} ... Done".format(name))
        return {"name":name,"songs":songs}
    except:
        print("get_Song_of {}....timeout.....".format(singer))




#---------------------单线程--------------------------
# def spider():
#     # 分区
#     all_singers = []
#     for i in range(1,27): # A-Z
#         zone_singers = get_ZoneSingers(i)
#         all_singers.append(zone_singers)
#         # if (i > 2):
#         #     break
#     for zone_singers in all_singers:
#         for page_singers in zone_singers:
#             for singer in page_singers:
#                 url = "https://y.qq.com/n/yqq/singer/{}.html".format(singer)
#                 get_Song(url)
#----------------------------------------------------


# 爬取每个分页下的歌手信息
def crawl_page(page_singers):
    for singer in page_singers:
        time.sleep(1.5)
        get_Song(singer)
    return


# 爬取每个分区下的歌手信息，一个线程负责一页下的所有歌手
def crawl_zone(zone_singers):
    with ThreadPoolExecutor(max_workers=18) as executor:
        for page_singers in zone_singers:
            executor.submit(crawl_page,page_singers)
    return

# 一个进程负责一个分区下的所有歌手
def spider():
    # 分区
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i in range(1,27): # A-Z
            zone_singers = get_ZoneSingers(i)
            executor.submit(crawl_zone,zone_singers)
    return


import time

if __name__ == '__main__':
    spider()