# src/modules/authentications/menus/routers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from fastapi import APIRouter, status, Depends, Request, Query
from fastapi.exceptions import HTTPException
from .schemas import (
    MenuRequestSchema, 
    MenuSchema, 
    MenuResponseSchema,
    GiveMenuToRoleSchema,
    GiveMenuToUserSchema,
    SelectMenuSchema
)
from .models import Menu
from .services import MenuService
from src.databases import db
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.utils.dependency import AccessTokenBearer, AccessControlBearer

router = APIRouter(
    dependencies=[Depends(AccessTokenBearer())],
)

service = MenuService()
session = db.session


@router.get("/", response_model=MenuResponseSchema, status_code=status.HTTP_200_OK)
async def index(request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "view:menus"])),
):
    return await service.all(request, session, keywords, skip, limit)


@router.get("/{id}", response_model=MenuSchema, status_code=status.HTTP_200_OK)
async def show(
    id: int, 
    request: Request, 
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "show:menus"])),
):
    return await service.find(id, request, session)

@router.get("/select/all", response_model=List[SelectMenuSchema], status_code=status.HTTP_200_OK)
async def select_all(
    request: Request,
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "select:menus"])),
):
    return await service.select(request, session)

@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED)
async def store(
    request: Request, 
    body: MenuRequestSchema, 
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "create:menus"])),
):
    return await service.create(request, body, session)

@router.put("/{id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def update(
    id: int, 
    request: Request, 
    body: MenuRequestSchema, 
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "update:menus"])),
):
    return await service.update(id, request, body, session)

@router.patch(
    "/give-menu-roles", status_code=status.HTTP_200_OK
)
async def give_menu_to_role(
    request: Request,
    body: GiveMenuToRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:menus", "grant:role-menus"])
    ),
):
    return await service.give_menu_to_role(request, body, session)

@router.patch(
    "/give-menu-users", status_code=status.HTTP_200_OK
)
async def give_menu_to_user(
    request: Request,
    body: GiveMenuToUserSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:menus", "grant:user-menus"])
    ),
):
    return await service.give_menu_to_user(request, body, session)

@router.patch(
    "/revoke-menu-roles", status_code=status.HTTP_200_OK
)
async def revoke_menu_to_role(
    request: Request,
    body: GiveMenuToRoleSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:menus", "revoke:role-menus"])
    ),
):
    return await service.revoke_menu_to_role(request, body, session)

@router.patch(
    "/revoke-menu-users", status_code=status.HTTP_200_OK
)
async def revoke_menu_to_user(
    request: Request,
    body: GiveMenuToUserSchema,
    session: AsyncSession = Depends(session),
    _: bool = Depends(
        AccessControlBearer(permissions=["manage:menus", "revoke:user-menus"])
    ),
):
    return await service.revoke_menu_to_user(request, body, session)

@router.delete("/{id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def delete(
    id: int, 
    request: Request, 
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "delete:menus"])),
):
    return await service.destroy(id, request, session)

@router.get("/trash/all", response_model=MenuResponseSchema, status_code=status.HTTP_200_OK)
async def trash(request: Request,
    session: AsyncSession = Depends(session),
    keywords: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "trash:menus"])),
):
    return await service.trash(request, session, keywords, skip, limit)


@router.patch("/{id}", response_model=Menu, status_code=status.HTTP_200_OK)
async def patch(
    id: int, 
    request: Request, 
    session: AsyncSession = Depends(session),
    _: bool = Depends(AccessControlBearer(permissions=["manage:menus", "restore:menus"])),
):
    return await service.restore(id, request, session)
