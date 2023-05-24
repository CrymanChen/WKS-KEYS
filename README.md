# WKS-KEYS

## Abstract

### 项目名称
WKS-KEYS  
Project Name: WKS-KEYS  

### 项目介绍
这是一个经过修改的项目, 用于获取L3等级下, Widevine的密钥  
A repo modified for bypassing Widevine L3 DRM and obtaining keys.

### 版权信息
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
