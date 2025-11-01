import redis
from src.config import Config


JTI_EXPIRY = 3600

# This is for our redis configuration, this is enough to get a connect to our redis
token_blocklist = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)


# This function enough add our jti to our block list
def add_jti_to_blocklist(jti: str) -> None:
    token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


def token_in_blocklist(jti) -> bool:
    jti = token_blocklist.get(jti)
    return jti is not None
