import urllib
import urllib.request
import zlib

import redis

redis_host = '101.37.146.151'
redis_port = 11010
redis_password = 'yuZhI_reDis_18518!'
redis_db = 0
redis_w_key = "w:token:exchange_rate"


def redis_conn_master001():
    """
    wowtoken.py
    """
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db, decode_responses=True)
    return r


def get_token_rate():
    """
    dd373.py
    """
    with redis_conn_master001() as r:
        return float(r.get(redis_w_key))


def curl_get(url, timeout=5, proxy=False, headers=None, gzip=False):
    """
    wowtoken.py
    dd373.py
    crawler_515fa.py
    crawler_amac.py
    crawler_for_some_site.py
    """
    if headers is None:
        headers = {}
    opener = urllib.request.build_opener()
    if proxy:
        proxy_info = {'host': '127.0.0.1',
                      'port': 7890}
        proxy_support = urllib.ProxyHandler(
            {"http": "http://%(host)s:%(port)d" % proxy_info})
        opener = urllib.build_opener(proxy_support)

    request = urllib.request.Request(url, headers=headers)

    resp = opener.open(request, timeout=timeout)
    resp_html = resp.read()
    if gzip:
        resp_html = zlib.decompress(resp_html, 16 + zlib.MAX_WBITS)
    return resp_html
