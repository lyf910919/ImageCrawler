#-*-coding:utf8-*-
from apiclient.discovery import build

service = build("customsearch", "v1",
               developerKey="AIzaSyBN5NnKFKRR7-o-G3dInYqX_U8iV6oQC3o")

res = service.cse().list(
    q='番茄鸡蛋',
    cx='004707157896138204956:rjtivm6feck',
    searchType='image',
    num=None,
    imgType='photo',
    fileType='jpg',
    start=10,
    safe= 'off'
).execute()

f = open("list2.txt", "w+")
cnt = 0
if not 'items' in res:
    print 'No result !!\nres is: {}'.format(res)
else:
    for item in res['items']:
        #print('{}:\n\t{}'.format(item['title'].encode('utf-8'), item['link'].encode('utf-8')))
        print cnt
        cnt += 1
        f.write(item['link'].encode('utf-8') + '\n')
f.close()