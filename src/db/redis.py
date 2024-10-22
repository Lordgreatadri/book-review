
from redis.asyncio import Redis
from src.config import Config



# Create a Redis connection
token_list = Redis(
    host=Config.redis_host, 
    port=Config.redis_port,
    db=0
)


async def add_jti_to_blocklist(jti:str)->None:
    await token_list.set( 
        name=jti, 
        value="",
        ex=Config.jti_expiry
    )



async def token_in_blocklist(jti:str)->bool:
    jti = await token_list.get(jti)
    return jti is not None