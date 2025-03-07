# src/main.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

import os
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import FileResponse
from src.routers import routers
from src.startup import on_startup, on_shutdown
from .utils.errors import register_all_errors
from .midlewares.middleware import Middleware

version = "v1"

app = FastAPI(
    title="FastAPI",
    description="FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.",
    version=version,
    openapi_url=f"/openapi/{version}.json",
    docs_url=f"/docs",
    redoc_url=f"/redoc",
)

# Setup Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Register middleware
middleware = Middleware(app, parent_url=f"/api/{version}")
middleware.register_middleware()

# Register all errors
register_all_errors(app)

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("templates/fastapi.svg")


@app.get("/")
async def root(request: Request):
    data = {
        "request": request,
        "title": "Welcome to FastAPI",
        "description": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.",
        "fastapi": "https://fastapi.tiangolo.com",
        "docs": f"/docs",
        "redoc": f"/redoc",
        "convention_id": "/docs/convention-id.md",
        "convention_en": "/docs/convention-en.md",
        "by": "Mochammad Hairullah",
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/docs/{filename}")
async def get_docs(filename: str):
    file_path = f"docs/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

try:
    app.include_router(routers, prefix=f"/api/{version}")
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# for route in app.routes:
# with method
# print(f"{route.path} - {route.methods}")


@app.on_event("startup")
async def startup():
    await on_startup()


@app.on_event("shutdown")
async def shutdown():
    await on_shutdown()
