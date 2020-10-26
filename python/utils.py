import redis

redis_host = '101.37.146.151'
redis_port = 11010
redis_password = 'yuZhI_reDis_18518!'
redis_db = 0


def redis_conn_master001():
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db, decode_responses=True)
    return r
