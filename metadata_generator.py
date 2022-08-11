import glob
import json
import random
import os
import re

chapters = glob.glob('pic_test/*.png')
ind = list(range(len(chapters)))
random.shuffle(ind)
ipfs = ''
labels = {
    'HotspotSensitive': 'Polity',
    'PersonalAttack': 'Abuse',
    'SexJoke': 'Porn',
    'Arms': 'Terror',
    'ProfileDrainage': 'Ad',
    'E-commercePromotion': 'Ad',
    'ProhibitedBehavior': 'Illegal',
    'Violent': 'Terror',
    'Contraband': 'Illegal',
    'Anti-China': 'Polity',
    'TerroristIncident': 'Terror',
    'DiggingAd': 'Ad',
    'Gamble': 'Illegal',
    'PervertedPorn': 'Porn'}


def parse_title(title):
    title_list = title.split('_')
    if title[:2] == '三国':
        book = '三国演义'
    elif title[:2] == '红楼':
        book = '红楼梦'
    elif title[:2] == '西游':
        book = '西游记'
    elif title[:2] == '水浒':
        book = '水浒传'

    num = title_list[0].replace(book, '')
    label = title_list[-1].replace('sublabel(', '').replace(')', '')
    attr = {'Polity': set(),
                'Abuse': set(),
                'Porn': set(),
                'Terror': set(),
                'Ad': set(),
                'Illegal': set()}
    attributes = []

    label_list = label.split(',')
    if len(label_list[0]) >= 1:
        for l in label_list:
            ll = re.sub(r'[0-9]+', '', l)
            attr[labels[ll]].add(ll)

    for k, v in attr.items():
        if len(v) > 0:
            v = ','.join(sorted(v))
            attributes.append({"trait_type": k, "value": v.replace('China', 'Country')})
        else:
            attributes.append({"trait_type": k, "value": "None"})

    return book, num, attributes


for i in ind:
    title = chapters[i].replace('.png', '').replace('pic_test\\', '').replace('pic\\', '')
    book, num, attr = parse_title(title)
    metadata = {'name': f'洁净文学 #{str(i+1)}',
                'description': f'符合新时代语言规范的洁净文学选段： 《{book}》第{num}回',
                'image': ipfs + f'/{str(i+1)}.png',
                'attributes': attr
                }
    os.rename(chapters[i], f'pic_test\\{str(i+1)}.png')
    with open(f'pic_test\\{str(i+1)}.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
