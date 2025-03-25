# app.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

import uvicorn
from src.main import app
from src.configs import Config

if __name__ == "__main__":
    uvicorn.run(app, host=Config.APP_HOST, port=Config.APP_PORT)
