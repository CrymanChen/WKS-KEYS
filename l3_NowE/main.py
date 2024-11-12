# -*- coding: utf-8 -*-
# Module: KEYS-L3 for NowE
# Created on: 30-08-2024
# Authors: CrymanChen
# Version: 0.1.4

import requests
import os
import time
import random
import json
import sys
sys.path.insert(0, sys.path[0] + "/../")
from zhconv import convert
import binascii
import re
import keyboard
import subprocess

from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
from chrome_version import get_chrome_version
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

requests.packages.urllib3.disable_warnings()

os.system('')
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

chrome_ver = get_chrome_version().split(".")[0] + ".0.0.0"
headers = {
    'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36',
}

contentUrl = input(f'{CYAN}\nVideo link: {RESET}')
time.sleep(1)

def get_primary_data():
    # Only type in your account and password here. Do not edit anything elsewhere.
    account = "<INPUT YOUR ACCOUNT HERE>"
    password = "<INPUT YOUR PASSWORD HERE>"

    driver = webdriver.Chrome()
    try:
        driver.get("https://www.nowe.com/signin")
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "psdInput"))
        )
        username_input.send_keys(account)
        continue_button_xpath = "/html/body/div[1]/form[1]/div[4]/button"
        continue_button = driver.find_element(By.XPATH, continue_button_xpath)
        continue_button.click()

        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/form/div[3]/input"))
        )
        password_input.send_keys(password)
        login_button_xpath = "/html/body/div[1]/form/div[5]/button"
        login_submit_button = driver.find_element(By.XPATH, login_button_xpath)
        login_submit_button.click()

        print('[+] Waiting for cookies...')
        time.sleep(10)
        all_cookies = driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in all_cookies}
        with open('nowe_cookies.json', 'w') as file:
            json.dump(cookies_dict, file)
        return cookies_dict
    finally:
        driver.quit()


if os.path.exists('nowe_cookies.json'):
    with open('nowe_cookies.json', 'r') as file:
        cookies_dict = json.load(file)
        if cookies_dict:
            print(f'{GREEN}\nCookies extracted! Number of cookies: {RESET}{len(cookies_dict)}')
        else:
            print(f'{RED}\nCookies extraction failed! Please check your cookies in nowe_cookies.json! {RESET}')
else:
    cookies_dict = get_primary_data()
    print('[+] Using new cookies.')

timescale = int(time.time())


def callerReferenceNo():
    return "W" + str(int(time.time() * 1000)) + str(random.randint(1000, 1899))


def contentId():
    contentId = contentUrl.split('/')[-2]
    return contentId


def contentType():
    return 'Vod'


def deviceId():
    if cookies_dict.get('NMAF_uuid'):
        return cookies_dict.get('NMAF_uuid')
    else:
        print('deviceId: None')
        exit()


def deviceName():
    return 'Browser'


def deviceType():
    return 'WEB'


def mupId():
    if cookies_dict.get('NMAF_mupid'):
        return cookies_dict.get('NMAF_mupid')
    else:
        print('mupId: None')
        exit()


def profileId():
    if cookies_dict.get('OTTSESSIONID'):
        return cookies_dict.get('OTTSESSIONID')
    else:
        print('profileId: None')
        exit()


secureCookie = profileId()
pin = ''  # The pin value is Null.


def getVodURL():
    data = {
        "callerReferenceNo": callerReferenceNo(),
        "contentId": contentId(),
        "contentType": "Vod",
        "deviceId": deviceId(),
        "deviceName": deviceName(),
        "deviceType": deviceType(),
        "mupId": mupId(),
        "pin": "",
        "profileId": profileId(),
        "secureCookie": profileId()
    }
    r = requests.post(
        url='https://webtvapi.nowe.com/16/1/getVodURL',
        headers=headers,
        json=data,
        #proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
    )
    r_content = r.json()
    if r.status_code == 200 and r_content["responseCode"] == 'Success'.upper():
        print(f'{YELLOW}\nVOD URL successfully got! {RESET}')
        pass
    else:
        print(f'{RED}Error in getting VOD URL: {RESET}{r_content}')
        print(f'{YELLOW}Request body: {RESET}{r.request.body}')
        sys.exit()

    mpd_url = r_content["asset"]
    drmToken = r_content["drmToken"]
    return mpd_url, drmToken


mpd_url, drmToken = getVodURL()
print(f'{YELLOW}MPD URL: {RESET}{mpd_url}')
print(f'{YELLOW}drmToken: {RESET}{drmToken}')


def mpd_status_check():
    r2 = requests.get(url=mpd_url,
                      headers=headers,
                      #proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
                      )
    if r2.status_code != 200:
        print(f'{RED}Error in fetching .mpd resource: {RESET}{r2.raise_for_status()}')
        sys.exit()
    else:
        print(f'{GREEN}\nMPD status OK! {RESET}')
        pass


mpd_status_check()


def getProductDetail():
    episodeTitle = ''
    synopsis = ''
    r3 = requests.post(url='https://bridge.nowe.com/BridgeEngine/getProductDetail',
                       headers=headers,
                       json={
                           'callerReferenceNo': callerReferenceNo(),
                           'lang': 'zh',
                           'productIdList': [contentId()]
                       },
                       #proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
                       )
    r3_content = r3.json()
    if r3.status_code != 200 and r3_content["responseCode"] != 'Success'.upper():
        print(f'{RED}Error in getting episode details: {RESET}{r3.raise_for_status()}')
        sys.exit()
    else:
        print(f'{GREEN}Episode details successfully got! {RESET}')
        pass

    brandName = convert(r3_content["productDetailList"][0]["brandName"], 'zh-cn')
    episodeNum = r3_content["productDetailList"][0]["episodeNum"]
    episodeTitle = convert(r3_content["productDetailList"][0]["episodeTitle"], 'zh-cn')
    synopsis = convert(r3_content["productDetailList"][0]["synopsis"], 'zh-cn')
    return brandName, episodeNum, episodeTitle, synopsis


brandName, episodeNum, episodeTitle, synopsis = getProductDetail()
print(
    f'{YELLOW}\nVideo name: {RESET}{brandName}{YELLOW}, Episode number: {RESET}{episodeNum}{YELLOW}, Episode title: {RESET}{episodeTitle}')
print(f'{YELLOW}Synopsis: {RESET}{synopsis}')


def pssh():
    first_part = mpd_url.split('/')[:-1]
    base_url = '/'.join(first_part) + '/'
    init_url = base_url + 'stream_1/init.m4i'

    r4 = requests.get(url=init_url, #proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
                      )
    init_file_hex = binascii.hexlify(r4.content).decode('utf-8')
    init_file_hex_length = len(init_file_hex)
    pattern = r'000000[0-9a-fA-F]{2}70737368'
    match = re.search(pattern, init_file_hex)
    if not match:
        return False, "No match found for pattern '000000xx70737368'"
    start_index = match.start()
    expected_sequence = "00000000edef8ba979d64acea3c827dcd51d21ed000000"
    if init_file_hex[start_index + 16:start_index + 16 + len(expected_sequence)] != expected_sequence:
        return False, "Expected sequence not found after '000000xx70737368'"
    length_hex = init_file_hex[start_index + 16 + len(expected_sequence):start_index + 16 + len(expected_sequence) + 2]
    length = int(length_hex, 16)
    data_hex = init_file_hex[start_index:start_index + 16 + len(expected_sequence) + 2 + length * 2]
    data_bytes = bytes.fromhex(data_hex)
    extracted_pssh_b64 = b64encode(data_bytes).decode('utf-8')
    return True, extracted_pssh_b64, init_file_hex_length, length


result, pssh, init_file_hex_length, length = pssh()
init_file_size = int(init_file_hex_length / 2)
payload_size = int(length / 2)
if result:
    print(f'{YELLOW}\ninit.mp4 file size: {RESET}{init_file_size} {YELLOW}Bytes. {RESET}')
    print(f'{YELLOW}PSSH payload: {RESET}{payload_size} {YELLOW}Bytes (In Hex). {RESET}')
    print(f'{YELLOW}PSSH: {RESET}{pssh}')
else:
    print("Error:", pssh)

lic_url = 'https://fwp.now.com/wrapperWV'


def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
    challengeb64 = str(b64encode(wvdecrypt.get_challenge()), "utf-8")
    data = {"drmToken": drmToken, "rawLicenseRequestBase64": challengeb64}
    widevine_license = requests.post(url=lic_url, json=data, headers=headers,
                                     #proxies={'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
                                     )
    print(f'{GREEN}\nLicense request: {RESET}{challengeb64}')
    widevine_license.raise_for_status()
    if widevine_license.status_code == 200:
        license_b64 = b64encode(widevine_license.content)
        print(f'{GREEN}License response: {RESET}{license_b64.decode()}')
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt


correct, keys = WV_Function(pssh, lic_url)

print(f'{GREEN}\nKeys: {RESET}')
for key in keys:
    print('--key ' + key)
key_string = ' '.join([f"--key {key}" for key in keys])


def command_v():
    command_v = 're.exe'
    command_v += f' "{mpd_url}"'
    command_v += f' {key_string}'
    command_v += ' --use-shaka-packager'
    if f'{brandName} 第{episodeNum}集' == episodeTitle:
        name_v = f'{brandName} 第{episodeNum}集'
    else:
        name_v = f'{brandName} 第{episodeNum}集 - {episodeTitle}'
    command_v += f' --save-name "{name_v}"'
    command_v += ' --select-video best'
    return name_v, command_v


def command_as():
    command_as = 're.exe'
    command_as += f' "{mpd_url}"'
    command_as += f' {key_string}'
    command_as += ' --use-shaka-packager'
    if f'{brandName} 第{episodeNum}集' == episodeTitle:
        name_as = f'{brandName} 第{episodeNum}集_as'
    else:
        name_as = f'{brandName} 第{episodeNum}集 - {episodeTitle}_as'
    command_as += f' --save-name "{name_as}"'
    command_as += ' --select-audio all'
    command_as += ' --select-subtitle all'
    command_as += ' -M mp4'
    #command_as += ' -mt'
    command_as += f' --thread-count {thread_count}'
    return name_as, command_as


thread_count = 1
name_v, command_v = command_v()
name_as, command_as = command_as()


def mp4box_merge():
    mp4box_merge = 'mp4box'
    mp4box_merge += f' -add "{name_as}.mp4"'
    mp4box_merge += f' -itags tool=:title="{episodeTitle}":comment="{synopsis}"'
    mp4box_merge += f' "{name_v}.mp4"'
    return mp4box_merge


def next_skip_or_continue(next_step, command):
    start_time = time.time()
    print(f'{MAGENTA}Press "Ctrl+C" to cancel "{next_step}" or "K" to skip it in 3 seconds. {RESET}')
    while time.time() - start_time < 3:
        try:
            if keyboard.is_pressed('Ctrl+C'):
                print(f'{RED}Task ({next_step}) canceled! {RESET}')
                sys.exit()
            elif keyboard.is_pressed('k'):
                if next_step == 'Download video':
                    print(f'{YELLOW}Task ({next_step}) skipped! {RESET}')
                    subprocess.run(command_as)
                    print(
                        f'{YELLOW}\nMuxing and writing metadata! Some unreadable characters may appear but they do not affect the process. {RESET}')
                    subprocess.run(mp4box_merge())
                    os.remove(f"{name_as}.mp4")
                    print(f'{GREEN}Task finished! {RESET}')
                    sys.exit()
                elif next_step == 'Download audio and subtitle':
                    pass
        except KeyboardInterrupt:
            print(f'{RED}Task ({next_step}) canceled by KeyboardInterrupt! {RESET}')
            sys.exit()
    subprocess.run(command)


print()
next_step = 'Download video'
next_skip_or_continue(next_step, command_v)

print()
next_step = 'Download audio and subtitle'
next_skip_or_continue(next_step, command_as)

print(
    f'{YELLOW}\nMuxing and writing metadata! Some unreadable characters may appear but they do not affect the process. {RESET}')
subprocess.run(mp4box_merge())
os.remove(f"{name_as}.mp4")
print(f'{GREEN}Task finished! {RESET}')
sys.exit()
