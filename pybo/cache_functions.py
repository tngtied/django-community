import redis
import json
from django.conf import settings

# Redis 연결 설정
redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

# 딕셔너리를 Redis에 JSON 형식의 문자열로 저장하는 함수
def save_dict_to_redis_as_string(key, data, ttl=None):
    json_data = json.dumps(data)
    if ttl:
        redis_client.setex(key, ttl, json_data)
    else:
        redis_client.set(key, json_data)

# Redis에서 JSON 형식의 문자열을 가져와 딕셔너리로 변환하는 함수
def get_dict_from_redis_string(key):
    json_data = redis_client.get(key)
    if json_data:
        return json.loads(json_data)
    return None

def get_element_from_redis_dict(key, sub_key):
    dict_data = get_dict_from_redis_string(key)
    if dict_data:
        return dict_data.get(sub_key)
    return None

def add_to_redis_dict(key, sub_key, data):
    dict_data = get_dict_from_redis_string(key)
    if dict_data:
        dict_data[sub_key] = data
        save_dict_to_redis_as_string(key, dict_data)
    else:
        save_dict_to_redis_as_string(key, {sub_key: data})