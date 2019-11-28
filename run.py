"""
模型服务入口
"""

import os
import base64
import aiofiles
import asyncio
import logging
import logging.config

from sanic import Sanic
from aiofiles import os as async_os
from sanic.blueprints import Blueprint
from sanic.response import json, file_stream

# from handler.user import User
# from handler.picture import Picture

CURRENT_WORK_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(CURRENT_WORK_DIR, "conf", "logging.conf"))


app = Sanic("faceplus")
logger = logging.getLogger("web")


@app.route("/", methods=["GET"])
async def index(request):
    file_path = "./data/classmate.jpeg"
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}
    return await file_stream(file_path, headers=headers, chunked=False)


@app.route("/picture", methods=["POST"])
async def post_picture(request):
    print("have request")
    data = request.json.get("pic", None)
    if not data:
        return json({
            "isSuccess": "false",
            "msg": "paramter pic is not find",
            "data": {
                "code": ""
            }
        })
    # result = picture.post_picture(data)
    image_str, image_data = data.split(",", 1)
    print(image_str)
    image_format = image_str.split(";")[0].split("/")[-1]
    print(image_format)
    image = base64.decodestring(image_data.strip().encode())
    async with aiofiles.open(f"./image/picture/chenenquan.{image_format}", "wb") as w:
        await w.write(image)
    return json({
            "isSuccess": "true",
            "msg": "",
            "data": {
                "code": '123456'
            }
    })


@app.route("/picture/<picture_id>", methods=["GET"])
async def get_picture(request, picture_id):
    pass


@app.route("/picture/<picture_id>", methods=["PUT"])
async def put_picture(request, picture_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, access_log=True, host="localhost", port=8080)
