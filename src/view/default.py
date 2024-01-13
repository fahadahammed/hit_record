#  Copyright (c) Fahad Ahammed 2024.
import datetime

from src import app
from flask import jsonify
from src.ops.redisops import RedisOps
import socket


@app.route(f"/api", methods=["GET"])
@app.route(f"/api/{app.config.get('API_STATE')}", methods=["GET"])
@app.route(f"/api/{app.config.get('API_STATE')}/", methods=["GET"])
def index():
    to_return = {
        "msg": "Welcome to hit_record! I am going to record the hit count in redis.",
        "datetime": datetime.datetime.today().utcnow().replace(microsecond=0),
        "version": app.config.get("API_VERSION"),
        "hostname": str(socket.gethostname()),
        "app_state": f"{app.config.get('API_STATE')}"
    }
    try:
        RedisOps().rc.incr(name="hits")
        to_return["hit_count"] = int(RedisOps().rc.get(name="hits"))
    except Exception as ex:
        to_return["hit_count"] = 0
        to_return["msg"] = str(ex)
    return jsonify(to_return)
