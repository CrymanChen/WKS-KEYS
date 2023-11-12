# -*- coding: utf-8 -*-
# Module: KEYS-L3
# Created on: 11-10-2021
# Authors: -∞WKS∞-
# Version: 1.1.0

# Modified by: CrymanChen
# Modified on: November 12, 2023

import os
import sys
import base64, requests, sys, xmltodict
import binascii
import json
# 增加了一个第三方库pyperclip, 目的是将key(有时是多个key)快速复制到剪贴板中
import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt

os.system('cls')
help_text = '''
   l3mubi.py

Instructions: 
    -Key ID: (Can be described as) Public key. [Required]
    Format accepted: 1) 08053232-9530-448C-8728-BABDB21EE327 (Dashes and Capital not required)
                     2) CAUyMpUwRIyHKLq9sh7jJw==
    -License URL: No need to change unless you know how to edit Line 68.
    -dt-custom-data: A param in the headers of the license request. [Required]
You may need: 
    -Finding Key ID by installing Tampermonkey and EME logger (https://greasyfork.org/en/scripts/373903-eme-logger)
                    or searching in the .mpd file.
    -dt-custom-data by opening developer tools in your browser by pressing F12 in general cases.
'''
if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
    print(help_text)
else:
    print('\n Tip: You can input -h or --help for better understanding. \n')


Input = input('Key ID: ')

def createpsshfromkid(kid_value):
   kid_value = kid_value.replace('-', '')
   assert len(kid_value) == 32 and not isinstance(kid_value, bytes), "wrong KID length"
   array_of_bytes = bytearray(b'\x00\x00\x002pssh\x00\x00\x00\x00')
   array_of_bytes.extend(bytes.fromhex("edef8ba979d64acea3c827dcd51d21ed"))
   array_of_bytes.extend(b'\x00\x00\x00\x12\x12\x10')
   array_of_bytes.extend(bytes.fromhex(kid_value.replace("-", "")))
   return base64.b64encode(bytes.fromhex(array_of_bytes.hex())).decode('utf-8')

def inputjudging(Input):
    if len(Input.replace('-', '')) == 32: 
        pssh = createpsshfromkid(Input)
    elif '=' in Input: 
        try:
            decoded = base64.b64decode(Input)
            kid = decoded.hex()
            pssh = createpsshfromkid(kid)
        except binascii.Error:
            print('Input must be either base64-encoded or in hex. ')
    return pssh

pssh = inputjudging(Input)
print('PSSH:', pssh)
lic_url = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'
print('License URL:', lic_url)
dt_custom_data = input('dt-custom-data: ')

def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
    widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers={
        'dt-custom-data': dt_custom_data
        })
    license_b64 = widevine_license.json()["license"]
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
