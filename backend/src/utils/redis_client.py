import redis
import time
from threading import Lock
import logging

class MemoryStore:
    """内存存储作为Redis的备选方案"""
    def __init__(self):
        self._storage = {}
        self._expiry = {}
        self._lock = Lock()

    def get(self, key):
        """获取值"""
        with self._lock:
            if key in self._storage:
                # 检查是否过期
                if key in self._expiry and self._expiry[key] < time.time():
                    self.delete(key)
                    return None
                return self._storage[key].encode('utf-8')
            return None

    def setex(self, key, seconds, value):
        """设置值，带过期时间"""
        with self._lock:
            if isinstance(value, str):
                value = value.encode('utf-8')
            self._storage[key] = value
            self._expiry[key] = time.time() + seconds
            return True

    def delete(self, key):
        """删除键"""
        with self._lock:
            self._storage.pop(key, None)
            self._expiry.pop(key, None)
            return True

class RedisClient:
    """Redis客户端"""
    def __init__(self):
        self._redis = None
        self._memory_store = MemoryStore()
        self._logger = logging.getLogger(__name__)

    def init_app(self, app):
        """初始化Redis连接"""
        try:
            self._redis = redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=False,
                socket_timeout=1
            )
            # 测试连接
            self._redis.ping()
            self._logger.info("Redis connection successful")
        except Exception as e:
            self._redis = None
            self._logger.warning(f"Redis connection failed, using memory store: {str(e)}")

    def get(self, key):
        """获取值"""
        if self._redis:
            try:
                return self._redis.get(key)
            except Exception as e:
                self._logger.error(f"Redis get error: {str(e)}")
        return self._memory_store.get(key)

    def setex(self, key, seconds, value):
        """设置值，带过期时间"""
        if self._redis:
            try:
                if isinstance(value, str):
                    value = value.encode('utf-8')
                return self._redis.setex(key, seconds, value)
            except Exception as e:
                self._logger.error(f"Redis setex error: {str(e)}")
        return self._memory_store.setex(key, seconds, value)

    def delete(self, key):
        """删除键"""
        if self._redis:
            try:
                return self._redis.delete(key)
            except Exception as e:
                self._logger.error(f"Redis delete error: {str(e)}")
        return self._memory_store.delete(key)

# 创建Redis客户端实例
redis_client = RedisClient() 