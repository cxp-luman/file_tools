import requests


def get_code():
    url = 'http: // openapi.baidu.com/oauth/2.0/authorize?response_type = {}&client_id = {}&redirect_uri = 您应用的授权回调地址&
scope = basic, netdisk&
device_id = 您应用的AppID'
GET 

以上链接示例中参数仅给出了必选参数，其中device_id为硬件应用下的必选参数。
关于应用的相关信息，您可在控制台，点进去您对应的应用，查看应用详情获得。


def auth():
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code=d5a53cd0ca7799d033399487b23ec992&client_id=EVaI5x0U6lEmP125G0Su55ROEXZtItdD&client_secret=VPgfmrt8UBM5kgkeUemwRVmr5AjhFuEV&redirect_uri=oob"

    payload = {
        'response_type': 'code',
        'client_id': 'Ds7a6NRDkqSxWByxdTzK6BhDy2pZDEcN',
        'redirect_uri': 'oob',
        'scope':'basic,netdisk'
    }
    headers = {
    'User-Agent': 'pan.baidu.com'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))