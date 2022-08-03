import base64
import glob
import configparser
import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tms.v20201229 import tms_client, models


punctuation = """！？，。＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
config = configparser.ConfigParser()
config.read('.env')
chapters = glob.glob('novel/*.txt')

if __name__ == "__main__":
    dirty_words_lib = {}
    cred = credential.Credential(config['apiKey']['secretId'], config['apiKey']['secretKey'])
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tms.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tms_client.TmsClient(cred, "eu-frankfurt", clientProfile)
    req = models.TextModerationRequest()
    params = {'BizType': 'purify_novel',
              'Action': 'TextModeration',
              'Region': 'eu-frankfurt'}

    for chapter in chapters:
        with open(chapter, encoding='utf-8') as f:
            lines = f.readlines()

        purified_lines = []
        record_of_dirtyword = {'label': {}, 'sublabel': {}}
        for line in lines:
            try:
                # line = line.strip('\n')
                out = base64.b64encode(line.encode('utf-8'))
                params['Content'] = out.decode()
                req.from_json_string(json.dumps(params))
                resp = client.TextModeration(req)
            except TencentCloudSDKException as err:
                print(err)

            if len(resp.Keywords) > 0:
                for detail in resp.DetailResults:
                    for keyword in detail.Keywords:
                        # line_no_punctuation = line.translate(str.maketrans("", "", punctuation))
                        # keyword_no_punctuation = keyword.translate(str.maketrans("", "", punctuation))
                        dw = keyword
                        if line.find(keyword) >= 0:
                            # ind = line_no_punctuation.index(keyword_no_punctuation)
                            # purify process based on non-punctuation string
                            # doing this way to handle the fusion match results
                            line = line.replace(keyword, '口'*len(keyword))
                        else:
                            print('The following line need to check:')
                            print(line)
                            print('dirty word: ' + keyword)
                            fix = input('Change word: ')
                            line = line.replace(fix, '口'*len(fix))
                            dw = fix
                        dirty_words_lib[dw] = detail.Label + '_' + detail.SubLabel

                    record_of_dirtyword['label'][detail.Label] = record_of_dirtyword['label'].get(detail.Label, 0) + 1
                    record_of_dirtyword['sublabel'][detail.SubLabel] = record_of_dirtyword['sublabel'].get(detail.SubLabel, 0) + 1

            purified_lines.append(line)

            time.sleep(0.1)

        name_string = 'label('
        for k, v in record_of_dirtyword['label'].items():
            name_string = name_string + k + str(v) + ','
        name_string = name_string.rstrip(',') + ')_sublabel('
        for k, v in record_of_dirtyword['sublabel'].items():
            name_string = name_string + k + str(v) + ','
        name_string = name_string.rstrip(',') + ')'

        with open(chapter.replace('.txt', '_clean_{}.txt'.format(name_string)), 'w', encoding='utf-8') as f:
            f.writelines(purified_lines)

        print('finish' + chapter)

    with open('dirty_library.txt', 'w', encoding='utf-8') as f:
        for k, v in dirty_words_lib.items():
            f.write(k + str(v) + '\n')
