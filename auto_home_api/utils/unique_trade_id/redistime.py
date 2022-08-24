from redis import Redis
import time
import hashlib


def unique_id_redis():
	conn = Redis()
	if not conn.get('unique_id_redis'):
		conn.set("unique_id_redis", int(time.time()))
	conn.incrby("unique_id_redis", amount=1)
	res = conn.get("unique_id_redis")
	md = hashlib.md5()
	md.update(res)
	md.update(str(time.time()).encode())

	conn.close()
	return md.hexdigest()
