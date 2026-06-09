import os
import redis
from dotenv import load_dotenv
load_dotenv()
redis_key = os.environ.get("REDIS_HOST")
use_ssl = os.environ.get("REDIS_SSL", "false").lower() == "true"
r = redis.Redis(host=redis_key, port=6379, ssl=use_ssl, socket_keepalive=True, socket_connect_timeout=5, socket_timeout=5)