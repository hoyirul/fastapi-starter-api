# src/databases/__init__.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa


# This file is used to import all the modules in the configs package
from .db import Database
from .redis import RedisDB

db = Database()
