import redis
from rediscluster import RedisCluster


class RedisClient(object):
    def __init__(self, host=None, port=None, password=None, db=0, is_cluster=False, nodes=None):
        """
          :param host: 地址
          :param password: 密码
          :param db: 0-15
          :param is_cluster: 是否集群
          :param nodes: 集群节点信息
          :param decode_responses: 是否decode
        """
        self.host = host
        if port and not isinstance(port, int):
            port = int(port)
        self.port = port
        self.password = password
        if db and not isinstance(db, int):
            db = int(db)
        self.db = db
        self.is_cluster = is_cluster
        self.nodes = nodes
        self.__decode_responses = True  # 结果decode成字符串
        self.__encoding_errors = 'replace'  # 忽略decode非法字符
        self.__encoding = 'utf-8'
        self.__conn = None
        self.connect()

    def connect(self):
        """
           获取redis连接
           :return:
        """
        if not self.__conn:
            if self.is_cluster:
                self.__conn = RedisCluster(startup_nodes=self.nodes, password=self.password,
                                           decode_responses=self.__decode_responses,
                                           encoding_errors=self.__encoding_errors,
                                           encoding=self.__encoding)
            else:
                pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password,
                                            db=self.db, socket_connect_timeout=3, decode_responses=self.__decode_responses,
                                            encoding_errors=self.__encoding_errors, encoding=self.__encoding)
                self.__conn = redis.StrictRedis(connection_pool=pool)
        return self.__conn
