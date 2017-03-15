from django.conf import settings
import redis
import os

# redis configuration for testing and production environment
if "REDIS_URL" in os.environ:
    connection_pool = redis.ConnectionPool.from_url(os.environ.get("REDIS_URL"))

else:
    if settings.TESTING:
        redis_config = settings.REDIS['test']
    else:
        redis_config = settings.REDIS['default']

    connection_pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'])

redis_client = redis.StrictRedis(connection_pool=connection_pool)