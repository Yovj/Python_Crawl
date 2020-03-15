import requests

# response = requests.get("http://http.tiqu.qingjuhe.cn/getip?num=10&type=2&pack=47376&port=11&lb=1&pb=4&regions=").text
# print(response.text)
#
# ips = response['data']

url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong9621321373752951&g_tk=1140163968&loginUin=0&hostUin=0&' \
          'format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
           '"param":{"order":1,"singerMid":"000HzpCs2ODxnC","begin":1,"num":20},"module":"musichall.song_list_server"}}'

response = requests.get(url)
print(response.text)