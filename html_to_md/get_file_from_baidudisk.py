import requests

client_id = 'Ds7a6NRDkqSxWByxdTzK6BhDy2pZDEcN'
client_secret = 'APU2mQCZN9H76023xcHprjGcXclxS8Q4'


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


def auth(code):
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code" \
          "={}&client_id={}&client_secret" \
          "={}&redirect_uri=oob".format(code, client_id, client_secret)

    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text.encode('utf8'))
    return response.json()


def refresh_token(refresh_token):
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}".format(
        refresh_token, client_id, client_secret)

    payload = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))

def get_file_list_all(access_token):
    url = "http://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall&path=/{}&access_token={" \
          "}&web=1&recursion=1&start=0&order=name".format("极客时间", access_token)

    payload = {}
    files = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    print(response.text.encode('utf8'))

def get_file_list(folder_name, access_token):
    url = "https://pan.baidu.com/rest/2.0/xpan/file?method=list&dir=/{}&order=name&start=0&web=web&folder=0&access_token={}".format(folder_name, access_token)

    payload = {}
    files = {}
    headers = {
        'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    print(response.text.encode('utf8'))

if __name__ == '__main__':
    get_code()
    token_info = auth()
    refresh_token(token_info['refresh_token'])
