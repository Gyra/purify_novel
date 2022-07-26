import base64
import os
import configparser
import json
import fpdf
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tms.v20201229 import tms_client, models

config = configparser.ConfigParser()
config.read('.env')
replace_list = ['杀', '死']

if __name__ == "__main__":
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

    with open('novel/西游记4.txt', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        try:
            out = base64.b64encode(line.encode('utf-8'))
            params['Content'] = out.decode()
            req.from_json_string(json.dumps(params))
            resp = client.TextModeration(req)
            print(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
