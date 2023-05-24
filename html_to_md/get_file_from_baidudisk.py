import os
import threading
import time
from datetime import datetime

import requests

client_id = 'Ds7a6NRDkqSxWByxdTzK6BhDy2pZDEcN'
client_secret = 'APU2mQCZN9H76023xcHprjGcXclxS8Q4'
refresh_token = ''
access_token = ''

def get_code():
    url = 'http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={}&redirect_uri={}&scope=basic,' \
          'netdisk&device_id={}'.format(
        'Ds7a6NRDkqSxWByxdTzK6BhDy2pZDEcN',
        'oob',
        '31435215'
    )
    print(url)
    resp = requests.get(url=url)
    if resp.status_code != 200:
        print("获取code失败")

def group_paths_by_prefix(path_list):
    """Given a list of file paths, group them by common prefix and return as a list of lists."""
    # Create a dictionary to store the paths by prefix
    paths_by_prefix = {}
    for path in path_list:
        # Get the prefix by splitting the path at the last directory separator
        prefix = os.path.dirname(path)
        # Add the path to the list for the prefix in the dictionary
        if prefix not in paths_by_prefix:
            paths_by_prefix[prefix] = [path]
        else:
            paths_by_prefix[prefix].append(path)
    
    # Return the values (lists of paths) from the dictionary as a list
    return list(paths_by_prefix.values())

def get_access_token(code):
    global access_token, refresh_token
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code" \
          "={}&client_id={}&client_secret" \
          "={}&redirect_uri=oob".format(code, client_id, client_secret)

    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(response.text.encode('utf8'))
    resp_json = response.json()
    access_token = resp_json['access_token']
    refresh_token = resp_json['refresh_token']
    filename = './access_token.txt'
    if os.path.exists(filename):
        mode = "a"  # 如果文件存在则追加内容
    else:
        mode = "w"  # 如果文件不存在则创建文件并写入内容和当前时间

    with open(filename, mode) as file:
        file.write("access_token:" + access_token)
        file.write(" " + str(datetime.now()) + "\n")
        file.write("refresh_token:" + refresh_token)
        file.write(" " + str(datetime.now()) + "\n")
    return access_token

def refresh_token(input_refresh_token=None):
    global access_token, refresh_token
    if input_refresh_token != None:
        refresh_token = input_refresh_token
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}".format(
        refresh_token, client_id, client_secret)

    payload = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(response.text.encode('utf8'))
    resp_json = response.json()
    access_token = resp_json['access_token']
    refresh_token = resp_json['refresh_token']
    return response.json()

def get_file_list_all(folder_path, input_access_token=None):
    global access_token
    if input_access_token != None:
        access_token = input_access_token
    url = "http://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall&path=/{}&access_token={" \
          "}&web=1&recursion=1&start=0&order=name".format(folder_path, access_token)

    payload = {}
    files = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    if response.status_code != 200:
        print(response.text.encode('utf8'))
        return
    resp_json = response.json()
    with open('asdasd.json', "w", encoding='utf-8') as f:
        f.write(str(resp_json['list']))
    return resp_json

def extract_fs_ids(response):
    """
    Extracts fs_id and path from response and stores files with same prefix in dict
    
    Args:
    response (dict): Response object to be parsed
    
    Returns:
    dict: Files with same prefix in dict with key as prefix and value as dict with filename as key and fs_id as value
    """
    files = response['list']
    file_dict = {}
    
    for f in files:
        if f['isdir'] == 0:  # Only consider files, ignore directories
            fs_id = f['fs_id']
            path = f['path']
            dirname, basename = os.path.split(path)
            extension = basename.split('.')[-1]
            course_dirname = dirname.split('/')[-1]
            if extension == 'html':
                prefix = course_dirname  # Use os.sep for cross-platform compatibility
                
                if prefix not in file_dict:
                    file_dict[prefix] = [fs_id]
                else:
                    file_dict[prefix].append(fs_id)
    return file_dict

def get_dlink(fs_id_list, input_access_token=None):
    global access_token
    if input_access_token != None:
        access_token = input_access_token
    url = "http://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas&access_token={}&fsids={}&thumb=1&dlink=1&extra=1".format(access_token, fs_id_list)

    payload = {}
    files = {}
    headers = {
    'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data = payload, files = files)
    resp_json = response.json()
    file_info_list = resp_json['list']
    dlink_list = [{file_info['filename']: file_info['dlink']} for file_info in file_info_list]
    if response.status_code != 200:
        print(response.text.encode('utf8'))
    return dlink_list

def download(folder_path, dlink_dict, input_access_token=None):
    global access_token
    if input_access_token != None:
        access_token = input_access_token
    file_name = next(iter(dlink_dict))
    dlink = dlink_dict[file_name]
    print(folder_path, file_name, dlink)
    url = "{}&access_token={}".format(dlink, access_token)
    payload = {}
    files = {}
    headers = {
    'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data = payload, files = files)
    if response.status_code != 200:
        print("缺失文件！")
        exit(1)
    # print(response.content.decode("utf8","ignore").encode("utf-8","ignore"))
    response.encoding = 'utf-8'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(folder_path+'/'+file_name, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("write {} success!".format(file_name))
    # print(response.text.encode('utf8'))

# 处理函数，将链接请求并写入文件
def process(file_path, url_list):
    for url in url_list:
        # TODO: 发送HTTP请求并写入文件
        download(file_path, url)
def split_list(lst, num_splits=10):
    """
    Splits a list into num_splits sub-lists of roughly equal size.
    """
    split_size = len(lst) // num_splits
    remainder = len(lst) % num_splits
    splits = []
    start = 0
    for i in range(num_splits):
        split_len = split_size + (i < remainder)
        splits.append(lst[start:start+split_len])
        start += split_len
    return splits

def get_file(file_path):
    # get_code()
    # get_access_token('4b5bea3d250fcb8e7ad2b5330007c28c')
    file_path = file_path[2:]
    # file_path = '极客时间/专栏/79-消息队列高手课'
    file_info_json = get_file_list_all(file_path, '121.adf12df2d4f2fedfe5da4d4d684e8edd.Y_58ut0kYV-udAwATJx1lr4OErGd1xOH9JAJTnY.xQhGPQ')
    res = extract_fs_ids(file_info_json)
    thread_list = []
    key = file_path.split('/')[-1]
    fs_id_list = res[key]
    url_list = get_dlink(fs_id_list, '121.adf12df2d4f2fedfe5da4d4d684e8edd.Y_58ut0kYV-udAwATJx1lr4OErGd1xOH9JAJTnY.xQhGPQ')
    chunks = split_list(url_list)
    for i in range(len(chunks)):
        sub_list = chunks[i]
        t = threading.Thread(target=process, args=(file_path, sub_list))
        thread_list.append(t)
        

    # 启动多个线程并发处理
    for t in thread_list:
        t.start()

    # 等待所有线程完成
    for t in thread_list:
        t.join()
    