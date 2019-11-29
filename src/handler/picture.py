import base64
import logging
import asyncio
import aiofiles
from pymysql.err import IntegrityError

from .base import Base
from src.utils import gen_code

logger = logging.getLogger("web")


class Picture(Base):

    static_path = "./static/picture"

    async def check_code(self, code: str) -> bool:
        sql = f"SELECT code FROM picture WHERE code={code}"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                return bool(await cur.fetchone())

    async def post_picture(self, data: str) -> str:
        image_str, image_data = data.split(",", 1)
        image_suf = image_str.split(";")[0].split("/")[-1]
        image_bytes = base64.decodestring(image_data.strip().encode())
        code, fname = await self.insert_picture(image_suf)

        path = f"{self.static_path}/{fname}"
        async with aiofiles.open(path, "wb") as w:
            await w.write(image_bytes)
        return code

    async def insert_picture(self, suf: str) -> (str, str):
        sql = "INSERT INTO picture(code, fname) values('{code}', '{fname}');"
        async with self, self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                while 1:
                    code = gen_code()
                    fname = code+"."+suf
                    try:
                        await cur.execute(sql.format(
                            code=code,
                            fname=fname
                        ))
                        await conn.commit()
                    except IntegrityError:
                        logger.warn(f"{code} is already exists.")
                        continue
                    logger.info(f"{code} have inserted.")
                    return code, fname


picture = Picture()
