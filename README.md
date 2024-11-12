# WKS-KEYS

## 更新 Update
### 2024.11.12
l3_NowE 文件夹  (l3_NowE Folder)  

简介：该文件夹是一个用于下载[NowE](https://www.nowe.com/ "NowE")当中受Widevine保护的视频资源，且该项目为全自动实现，只需输入视频的URL即可自动获取所有所需的数据，并自动通过[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE "N_m3u8DL-RE")和[mp4box](https://github.com/gpac/gpac/wiki/mp4box "mp4box")来下载、解密和对视频进行混流。  
Introduction: This folder is designed for downloading Widevine-protected video resources from [NowE](https://www.nowe.com/ "NowE"). The project is fully automated; simply input the video URL to automatically retrieve all the necessary data and use [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE "N_m3u8DL-RE") and [mp4box](https://github.com/gpac/gpac/wiki/mp4box "mp4box") to download, decrypt, and mux the video.  
1. 通过`selenium`实现自动登录和登录token的获取。  
2. 通过`zhconv`将例如视频标题自动转换成简体中文（当然你也可以自己修改）  
3. 自动获取Chrome浏览器的版本号（该版本号至关重要）  

(a. Achieve automatic login and retrieval of login tokens using `selenium`.  
b. Automatically convert text, such as video titles, to Simplified Chinese using `zhconv` (of course, you can modify this as needed).  
c. Automatically obtain the version number of the Chrome browser (this version number is crucial).)  

提示：原则上来说，你只需要下载该文件夹到WKS-KEYS文件夹内，安装`requirements.txt`内的第三方库，运行`main.py`，输入视频的URL地址即可。  
**Note**: In principle, you only need to download this folder into the WKS-KEYS folder, install the third-party libraries listed in `requirements.txt`, run `main.py`, and input the video URL.  

再注：该程序为约一年前的作品，因为缺少维护，代码略显丑陋，请大家见谅。
**P.S.**: It's been around a year since I wrote this script, and it may look pretty ugly due to insufficient maintenance, about which I'm sorry.

### 2023.11.12
l3mubi.py 
1. 输入base64编码或十六进制的Key ID即可自动转化为PSSH.  
2. 优化标头部分，仅需要关键参数。  
3. 增加帮助部分，加入`-h`或`--help`即可阅读更详细的说明。  

(a. Either Key ID in base64 or in hex will convert to PSSH automatically.  
 b. Only critical params are needed in headers (rather than full headers).  
 c. Adding `-h` or `--help` will enable help text which is more datailed and beneficial to using this script.)

非常感谢 [Spectrumhsm](https://forum.videohelp.com/members/307425-Spectrumhsm) 的宝贵意见！
Really appreciate the great idea from [Spectrumhsm](https://forum.videohelp.com/members/307425-Spectrumhsm)!  
示例截图 Screenshot:  
![20231112001310](https://github.com/CrymanChen/WKS-KEYS/assets/106590233/65d22284-fc54-4fcc-b0bf-1ffd3d48437b)

## 简介 Abstract

### 项目名称 Project Name
WKS-KEYS

### 项目介绍 Introduction
这是一个经过修改的项目, 用于获取L3等级下, Widevine的密钥  
A repo modified for bypassing Widevine L3 DRM and obtaining keys.  
在这里我会不定期上传一些我写好的程序(下称脚本)，以方便新手直接使用。每个脚本都对应不同的网站。请注意，所有经过我编写的脚本均不得用于商业用途，且上传脚本并不是我的义务。  
I will upload some programs that I have edited from time to time (hereinafter referred to as scripts) for new-beginners' convenience. Each script works for getting keys from different websites. Please note that, no commercial usage to all my scripts, and it's not an obligation to update them so DO NOT rush please.

### 版权信息 Copyright Information
本项目原发行于[WKS-KEY](https://github.com/weapon121/WKS-KEY), 其中[WKS-KEY](https://github.com/weapon121/WKS-KEY)又来自于[WKS-KEY](https://github.com/WKS-uwu/WKS-KEY), 在此对两位作者[WKS-uwu](https://github.com/WKS-uwu)和[weapon121](https://github.com/weapon121)表示感谢。同时若[此修改版](https://github.com/CrymanChen/WKS-KEYS)不慎触犯了您的利益, 请第一时间与我联系。本项目无任何商业用途, 仅为个人学习, 方便个人使用。  
Copyright Information: This project came from [WKS-KEY](https://github.com/weapon121/WKS-KEY), and [WKS-KEY](https://github.com/weapon121/WKS-KEY) was forked from [WKS-KEY](https://github.com/WKS-uwu/WKS-KEY). I'd like to express my sincerest thanks to both developers [WKS-uwu](https://github.com/WKS-uwu) and [weapon121](https://github.com/weapon121). In case [this modified version](https://github.com/CrymanChen/WKS-KEYS) unintentionally infringes upon your interests, please contact me as soon as possible. This project is purely for personal learning and convenience, without any commercial purpose. This also means that if the modifications made to your project are unintentionally harmful, please contact me immediately.

## Usage (Chinese Simplified)
本项目需要一定的专业知识(A bit technical), 如果您对该领域不了解, 请不要进行尝试, 我亦不会对相应问题进行解答, 敬请谅解。

### 需要预先准备的东西
1. 本程序(WKS-KEYS.zip)  
2. 一个有效的CDM

### 步骤说明
1. 准备好CDM。
2. 将CDM放置在这个目录(WKS-KEYS\pywidevine\L3\cdm\devices\android_generic\)下。
3. 播放受DRM保护的视频, 收集需要的信息(包括但不限于PSSH和License URL)。
![image](https://user-images.githubusercontent.com/106590233/230447521-54db441e-9173-4fb0-828c-0e3a30bfb627.png)
![image](https://user-images.githubusercontent.com/106590233/230448001-3fd1440a-5d8b-4c0e-bd15-45c87975aa92.png)
4. 将收集的信息进行整理, 放置在相对应的Python文件中。
5. 输入PSSH和License URL, 等待服务器返回信息以及等待程序返回密钥。
6. 获得密钥, 请继续后续操作。

### 本项目修改之处
1. 对原项目进行了中文注释, 旨在提高代码的可识别性。
2. 对原项目进行了功能上的增加, 主要是增加了一个“自动复制密钥”的功能。

### 运行示意图
![image](https://user-images.githubusercontent.com/106590233/230448762-8e9a91fb-f7a5-44ee-8d43-88d230d272f0.png)
同时, 剪贴板上自动复制了你获得的密钥, 方便在使用例如[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)时, 可快速粘贴密钥信息, 无需手动逐一复制。  
你的剪贴板上的内容如下图所示: 
![image](https://user-images.githubusercontent.com/106590233/230449762-ad944337-0f7c-47af-9cb5-b8a9b528d708.png)
达到一键自动粘贴的功能, 无需手动复制粘贴。
