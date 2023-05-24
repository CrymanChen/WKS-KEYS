# -*- coding: utf-8 -*-
# Module: KEYS-L3
# Created on: 11-10-2021
# Authors: -∞WKS∞-
# Version: 1.1.0

# Modified by: CrymanChen
# Modified on: April 7, 2023

import base64, requests, sys, xmltodict
import headers
# 增加了一个第三方库pyperclip, 目的是将key(有时是多个key)快速复制到剪贴板中
import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
import urllib3

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

pssh = input('\nPSSH: ')
lic_url = input('License URL: ')
drmToken = input('drmToken: ')


def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
    challengeb64 = str(b64encode(wvdecrypt.get_challenge()),"utf-8")
    data = {"drmToken":drmToken,"rawLicenseRequestBase64":challengeb64}
    widevine_license = requests.post(url=lic_url, json=data, headers=headers.headers)

    print(f"\n[+] License Request: {widevine_license.request.body}")
    print(f"\n[+] License Response: {base64.b64encode(widevine_license.content)}")
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt   
correct, keys = WV_Function(pssh, lic_url)

print()
for key in keys:
    print('--key ' + key)

# 建立key_string字符串, 使得所有key进行如下变换: ①添加前缀"--key" ②使得每一个带有前缀的key以空格的形式连接起来(方便multi-keys时一键复制)
key_string = ' '.join([f"--key {key}" for key in keys])
# 使用导入的pyperclip库, 将key_string字符串复制至剪贴板, 省去手动选择"--key {key}"、复制、粘贴的麻烦
pyperclip.copy(key_string)