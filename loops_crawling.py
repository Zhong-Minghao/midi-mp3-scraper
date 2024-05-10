import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import urllib.error
import os
import json

root_path = r'./'

category = ["Bass", "Bass Guitar", "Bass Synth", "Bass Wobble", "Drum", "Flute", "Guitar Acoustic", "Guitar Electic",
            "Harp", "Percussion", "Piano", "Scratch", "Strings", "Synth", "Violin"]


category_cid = [2, 43, 44, 39, 1, 7, 33, 3, 41, 20, 21, 12, 10, 4, 29]


# music_to_crawl = 30000
music_to_crawl = 2000*len(category_cid)

music_in_one_page = 25

meta_keys = ["bpm", "genre", "key", "description", "url"]

metadata = dict()

# Create Folders
os.makedirs(r'./Looperman_Loops', exist_ok=True)
for this_category in category:
    os.makedirs(fr'./Looperman_Loops/{this_category}', exist_ok=True)

# count how many pages to crawl of each category
x = 0
y = 0
ca_sum_list = list()

for i in range(len(category)):

    this_url = f"https://www.looperman.com/loops?page=1&cid={category_cid[i]}&dir=d"
    response = requests.get(this_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ca_sum = int(soup.find_all(class_='pagination-counters')[0].get_text(strip=True).split(' ')[-1])
    ca_sum_list.append(ca_sum)
    if ca_sum < music_to_crawl/len(category):
        x += ca_sum
        y += 1

# for those categories with more music:
extra_crawl_num = (music_to_crawl - x) / (len(category) - y)

for i in range(len(category)):
    this_ca = category_cid[i]
    this_ca_name = category[i]
    print("="*10 + "crawling:" + this_ca_name + "="*10)

    if ca_sum_list[i] > extra_crawl_num:
        # require those categories with more music have enough bars to fill in the gaps.
        last_page = int(extra_crawl_num / music_in_one_page) + 1
    else:
        last_page = int(ca_sum_list[i] / music_in_one_page) + 1

    # last_page = 5

    # test whether we can crawl the last page??????
    final_page_url = f"https://www.looperman.com/loops?page={last_page}&cid={this_ca}&dir=d"
    response = requests.get(final_page_url)
    print(last_page)
    print("total page:" + str(last_page))

    # json
    this_ca_dict = dict()

    # 翻页
    for j in range(1, last_page + 1):

        this_url = f"https://www.looperman.com/loops?page={j}&cid={this_ca}&dir=d"
        response = requests.get(this_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find_all(id='body-left')[0]
        audio_rel = body.find_all(class_='player-wrapper')
        audio_tag = body.find_all(class_='tag-wrapper')
        audio_url = body.find_all(class_='player-title')
        audio_desc = body.find_all(class_='desc-wrapper')

        # if len(audio_rel) != len(audio_tag):
        #     raise SystemExit('number of tag not equal to number of music!')

        print(f' page:{j}', end='  ')
        # Any way to get the information without using loop?
        for k in range(len(audio_rel)):

            this_rel = audio_rel[k]['rel']
            this_name = this_rel.split('/')[-1].split('?')[0]
            this_tag = audio_tag[k]
            link_url = audio_url[2*k]['href']
            this_desc = audio_desc[k].get_text(strip=True)

            tags = [a.get_text(strip=True) for a in this_tag.find_all('a')]
            # another way: tags = [a.get_text(strip=True) for a in this_tag.select('.tag-wrapper a')]
            meta_tags = [tags[0], tags[1], tags[5].split(' ')[-1], this_desc, link_url]

            print(this_rel)

            this_dict = dict(zip(meta_keys, meta_tags))

            # problem1: get the rel but cannot download?
            try:
                urlretrieve(url=this_rel, filename=rf'./Looperman_Loops/{this_ca_name}/' + this_name)  # 下载歌曲
                this_ca_dict[this_name[:-4]] = this_dict  # "-4" means get rid of ".mp3"
            except urllib.error.HTTPError as e:
                print(f"HTTP Error {e.code}: {e.reason}")

    metadata[this_ca_name] = this_ca_dict
    with open(rf'./Looperman_Loops/{this_ca_name}_meta.json', 'w') as meta_file:
        json.dump(this_ca_dict, meta_file, indent=4)

with open(r'./Looperman_Loops/meta.json', 'w') as meta_file:
    json.dump(metadata, meta_file, indent=4)




