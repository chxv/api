from flask import Blueprint, jsonify, current_app, request, g
from ..utils import time_record
from datetime import datetime

mod = Blueprint('paste', __name__, url_prefix='/api/paste')


@mod.route('/read/', defaults={'key': ''})
@mod.route('/read/<key>')
@time_record
def read(key: str):
    """

    :param key:
    :return: json response
    """
    result = read_from(g.redis, key.encode('utf8'))
    return jsonify({'common': {'status': True, 'msg': 'Success'}, 'result': result})


@mod.route('/write/', methods=["POST"])
@time_record
def write():
    """
    if specify key, this api will write data with id.
    else write data to public area.
    :return: json response
    """
    post_data = request.json
    if not isinstance(post_data, dict):
        return jsonify({'common': {'status': False, 'msg': 'Forbidden'}}), 403
    # data
    data = str(post_data.get('data', ''))
    if not data:
        return jsonify({'common': {'status': False, 'msg': 'Forbidden'}}), 403
    # expire time
    max_expire_time = current_app.config.get('MAX_DATA_EXPIRE_TIME')
    expire_time = post_data.get('expire_time', max_expire_time)
    if (isinstance(expire_time, str) and expire_time.isdigit()) \
            or isinstance(expire_time, int):
        expire_time = int(expire_time)
        if expire_time < 5:  # 设置的超时时间太短
            return jsonify({'common': {'status': True, 'msg': 'success'}}), 202
    else:
        return jsonify({'common': {'status': False, 'msg': 'Forbidden'}}), 403
    # key
    key = str(post_data.get('key', ''))
    # write to redis
    write_to(g.redis, key.encode('utf8'), data.encode('utf8'), expire_time)  # store
    return jsonify({'common': {'status': True, 'msg': 'success'}}), 201


def read_from(redis, key=b'') -> list:
    """涉及redis的一律使用bytes类型"""
    if key:
        # 用户已设置key
        r = redis.get(current_app.config.get('PASTE_SECRET_KEY_PREFIX') + key)
        return [r.decode('utf8') if r else '']
    else:
        # 用户未设置key,读取全部public
        keys = redis.keys(current_app.config.get('PASTE_PUBLIC_KEY_PREFIX') + b"*")
        result = [item.decode('utf8') if isinstance(item, bytes) else item  # 三元表达式
                  for key in keys for item in redis.smembers(key)]          # 列表生成式
        return result


def write_to(redis, key: bytes, data: bytes, expire_time: int) -> None:
    """涉及redis的一律使用bytes类型"""
    if key:  # 用户已设置key
        redis.set(current_app.config.get('PASTE_SECRET_KEY_PREFIX') + key, data, ex=expire_time)
    else:    # 用户未设置key
        today = datetime.utcnow().weekday()
        key = current_app.config.get('PASTE_PUBLIC_KEY_PREFIX') + str(today).encode('utf8')
        redis.sadd(key, data)

        # 检查并清空明天的keys下的列表
        tomorrow = (today + 1) % 7
        key = current_app.config.get('PASTE_PUBLIC_KEY_PREFIX') + str(tomorrow).encode('utf8')
        redis.delete(key)
    return




