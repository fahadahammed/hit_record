#  Copyright (c) Fahad Ahammed 2024.
import os

from flask import Flask

app = Flask(__name__)
app.config["API_VERSION"] = os.environ.get("API_VERSION", "v1")
app.config["REDIS_HOST"] = os.environ.get("REDIS_HOST", "127.0.0.1")
app.config["REDIS_PORT"] = int(os.environ.get("REDIS_PORT", 6379))
app.config["REDIS_DB"] = int(os.environ.get("REDIS_DB", 0))
app.config["DEBUG"] = os.environ.get("DEBUG", True)
app.config["HOST"] = os.environ.get("HOST", "0.0.0.0")
app.config["PORT"] = int(os.environ.get("PORT", 22000))

from src.view.default import index
