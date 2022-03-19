import requests
import os
import json
import re


def download(dccon, file_name):
    url = "https://dcimg5.dcinside.com/dccon.php"
    headers = {'referer': 'https://dccon.dcinside.com/'}
    query_string = {'no': dccon['path']}
    with open(file_name, "wb") as file:
        response = requests.get(url, headers=headers, params=query_string)
        file.write(response.content)


print('---- 깃허브: https://github.com/ppaka/DcinsideEmojiDownloader ----')
print('만두몰 진입 -> 디시콘 바로가기 -> 원하는 디시콘 모음집 우클릭 -> 링크 주소 복사')

path = os.path.dirname(os.path.abspath(__file__))

userinput_url = input('디시콘 페이지 주소 입력: ')
dccon_num = userinput_url[userinput_url.find('#')+1:]

url = "https://dccon.dcinside.com/index/package_detail"
payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"package_idx\"\r\n\r\n{dccon_num}\r\n-----011000010111000001101001--\r\n"
headers = {
    'content-type': "multipart/form-data; boundary=---011000010111000001101001",
    'x-requested-with': "XMLHttpRequest"
}

req = requests.request("POST", url, data=payload, headers=headers)
soup = json.loads(req.content)

title = str(soup['info']['title'])
while True:
    if title.endswith(' ') or title.startswith(' ') or 'ㅤ' in title:
        print('[제목 앞 또는 뒤에 공백이 존재합니다. 공백을 제거합니다.]')
        title = title.strip()
        title = re.sub("^\s+|\s+$", "", title, flags=re.UNICODE)
        title = title.replace('ㅤ', '')
    else:
        break
print('다음을 다운로드합니다...', '"'+title+'"')

if re.search('[\/:*?"<>|]', title):
    old_title = title
    title = re.sub('[\/:*?"<>|]', '', title)
    print(f'제목에 사용 불가능한 문자가 있어 폴더이름을 변경하여 저장합니다.\n{old_title} ▶▶ {title}')

dccons = soup['detail']

for x in title:
    print(ord(x))

print('찾은 디시콘 개수: ' + str(len(dccons)))

count = 0

for i in dccons:
    count += 1
    sav_dir = path.replace('\\', '/')+'/'+title+'/'

    if not os.path.exists(sav_dir):
        os.makedirs(sav_dir)

    # vid_dir = sav_dir+'/videos/'
    # if not os.path.exists(vid_dir):
    #     os.makedirs(vid_dir)

    filename = str(count)
    if i['ext'] == 'png':
        filename += '.png'
        download(i, sav_dir+filename)
    elif i['ext'] == 'jpeg':
        filename += '.jpeg'
        download(i, sav_dir+filename)
    elif i['ext'] == 'jpg':
        filename += '.jpg'
        download(i, sav_dir+filename)
    elif i['ext'] == 'gif':
        filename += '.gif'
        download(i, sav_dir+filename)
    # elif i['ext'] == 'mp4':
    #     filename += '.mp4'
    #     download(i, vid_dir+filename)
    #     convertFile(vid_dir+filename, sav_dir, str(count), TargetFormat.GIF)

print('----다운로드를 마쳤습니다----')
