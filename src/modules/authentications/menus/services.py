# src/modules/authentications/menus/services.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Mochammad Hairullah

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .schemas import (
    MenuRequestSchema,
    GiveMenuToRoleSchema,
    GiveMenuToUserSchema,
    SelectMenuSchema
)
from .models import Menu, RoleMenu, UserMenu
from src.modules.logs.audit_logs.models import AuditLog
from sqlmodel import select, desc, cast, String
from fastapi import status, Request
from typing import Optional
from sqlalchemy.orm import joinedload
from src.utils.logging import Logging, ActivityLog
from src.utils.actions import ActionType
from sqlalchemy import func

class MenuService:
    # you can delete the function below if you don't need it
    def __init__(self):
        self.logger = Logging(level="DEBUG")
        self.activity_log = ActivityLog(level="DEBUG")
        self.action_type = ActionType()

    async def all(self, request: Request, session: AsyncSession, keywords: Optional[str] = None, skip: int = 0, limit: int = 10) -> dict:
        # Checking if the record is trashed (deleted)
        trashed = await AuditLog().is_trashed(Menu)

        # Build the query for fetching data
        q = (
            select(Menu)
            .select_from(Menu)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Menu.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Menu.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Menu.audit_logs),
                joinedload(Menu.audit_logs).joinedload(AuditLog.user),
                joinedload(Menu.audit_logs).joinedload(AuditLog.action),
            )
            .filter(~trashed)  # Exclude trashed data
            .order_by(desc(Menu.id))  # Order by Menu.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(Menu.id)).select_from(Menu).filter(~trashed)
        if keywords:
            count_query = count_query.filter(Menu.name.ilike(f"{keywords}"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the data along with pagination information
        return {"current_page": current_page,"total_count": total_count,"per_page": limit,"total_pages": total_pages,"data": response,}
        
    async def find(self, id: int, request: Request, session: AsyncSession) -> Optional[Menu]:
        trashed = await AuditLog().is_trashed(Menu)
        q = (
            select(Menu)
            .options(
                joinedload(Menu.audit_logs),
                joinedload(Menu.audit_logs).joinedload(AuditLog.user),
                joinedload(Menu.audit_logs).joinedload(AuditLog.action),
            )
            .where(Menu.id == id)
            .filter(~trashed)
        )
        menu = await session.execute(q)
        response = menu.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
            )
        return response

    async def select(self, request: Request, session: AsyncSession) -> dict:
        trashed = await AuditLog().is_trashed(Menu)
        q = select(Menu).filter(~trashed)
        result = await session.execute(q)
        response = result.scalars().all()

        return response

    async def create(self, request: Request, body: MenuRequestSchema, session: AsyncSession) -> dict:
        body = Menu(**body.dict())
        body.parent_id = None if body.parent_id == 0 else body.parent
        session.add(body)
        await session.commit()

        await self.activity_log(request=request,body={"action_id":await self.action_type("CREATE", session),"record_id":body.id,"model_name":Menu.__tablename__},session=session)
        
        return body

    async def update(
        self, id: int, request: Request, body: MenuRequestSchema, session: AsyncSession
    ) -> dict:    
        response = await self.find(id, request, session)
        for key, value in body.dict().items():
            if key == "parent_id":
                value = None if value == 0 else value
            setattr(response, key, value)
        await session.commit()
                
        await self.activity_log(request=request,body={"action_id":await self.action_type("UPDATE", session),"record_id":id,"model_name":Menu.__tablename__},session=session)

        return response
    
    async def give_menu_to_role(self, request: Request, body: GiveMenuToRoleSchema, session: AsyncSession) -> dict:
        given_menus = []
        
        try:
            for menu_id in body.menu_id:
                role_menu = RoleMenu(role_id=body.role_id, menu_id=menu_id)
                
                session.add(role_menu)
                await session.commit()
                
                given_menus.append(menu_id)

            return {"status": "success", "message": f"Menu {given_menus} has been assigned to role {body.role_id}"}
        
        except Exception as e:
            await session.rollback() 
            return {"status": "error", "message": str(e)}

    async def give_menu_to_user(self, request: Request, body: GiveMenuToUserSchema, session: AsyncSession) -> dict:
        given_menus = []
        
        try:
            for menu_id in body.menu_id:
                user_menu = UserMenu(user_id=body.user_id, menu_id=menu_id)
                
                session.add(user_menu)
                await session.commit()
                
                given_menus.append(menu_id)

            return {"status": "success", "message": f"Menu {given_menus} has been assigned to user {body.user_id}"}
        
        except Exception as e:
            await session.rollback() 
            return {"status": "error", "message": str(e)}

    # revoke_menu_to_role
    async def revoke_menu_to_role(self, request: Request, body: GiveMenuToRoleSchema, session: AsyncSession) -> dict:
        revoked_menus = []
        
        try:
            for menu_id in body.menu_id:
                q = select(RoleMenu).where(RoleMenu.role_id == body.role_id, RoleMenu.menu_id == menu_id)
                role_menu = await session.execute(q)
                response = role_menu.scalars().first()
                print(response)
                if response is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
                    )
                
                await session.delete(response)
                await session.commit()
                
                revoked_menus.append(menu_id)

            return {"status": "success", "message": f"Menu {revoked_menus} has been revoked from role {body.role_id}"}
        
        except Exception as e:
            await session.rollback() 
            return {"status": "error", "message": str(e)}

    # revoke_menu_to_user
    async def revoke_menu_to_user(self, request: Request, body: GiveMenuToUserSchema, session: AsyncSession) -> dict:
        revoked_menus = []
        
        try:
            for menu_id in body.menu_id:
                q = select(UserMenu).where(UserMenu.user_id == body.user_id, UserMenu.menu_id == menu_id)
                user_menu = await session.execute(q)
                response = user_menu.scalars().first()
                if response is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
                    )
                
                await session.delete(response)
                await session.commit()
                
                revoked_menus.append(menu_id)

            return {"status": "success", "message": f"Menu {revoked_menus} has been revoked from user {body.user_id}"}
        
        except Exception as e:
            await session.rollback() 
            return {"status": "error", "message": str(e)}

    async def destroy(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find(id, request, session)
        # await session.delete(response) # This hard delete the record, you can change it to soft delete with:
        # await session.commit()
                
        await self.activity_log(request=request,body={"action_id":await self.action_type("DELETE", session),"record_id":id,"model_name":Menu.__tablename__},session=session)

        return response
    
    async def trash(self, request: Request, session: AsyncSession, keywords: Optional[str] = None, skip: int = 0, limit: int = 10) -> dict:
        # Checking if the record is trashed (deleted)
        trashed = await AuditLog().is_trashed(Menu)

        # Build the query for fetching data
        q = (
            select(Menu)
            .select_from(Menu)
            .outerjoin(AuditLog, AuditLog.record_id == cast(Menu.id, String))
        )

        # Apply search keyword filter
        if keywords:
            q = q.filter(Menu.name.ilike(f"%{keywords}%"))

        q = (
            q.options(
                joinedload(Menu.audit_logs),
                joinedload(Menu.audit_logs).joinedload(AuditLog.user),
                joinedload(Menu.audit_logs).joinedload(AuditLog.action),
            )
            .filter(trashed)  # Just trashed data
            .order_by(desc(Menu.id))  # Order by Menu.id descending
            .offset(skip)  # Pagination offset (skip)
            .limit(limit)  # Pagination limit (number of records per page)
        )

        # Execute the query for data data with pagination
        result = await session.execute(q)
        response = result.unique().scalars().all()

        # Count the total number of records without pagination
        count_query = select(func.count(Menu.id)).select_from(Menu).filter(trashed)
        if keywords:
            count_query = count_query.filter(Menu.name.ilike(f"{keywords}"))
        count_response = await session.execute(count_query)
        total_count = count_response.scalar()

        # Calculate the total number of pages
        total_pages = (
            total_count + limit - 1
        ) // limit  # This is the ceiling of total_count / limit

        # Calculate the current page based on skip and limit
        current_page = skip // limit + 1 if total_count > 0 else 0

        # Return the data along with pagination information
        return {
            "current_page": current_page,
            "total_count": total_count,
            "per_page": limit,
            "total_pages": total_pages,
            "data": response,
        }

    async def find_trash(self, id: int, request: Request, session: AsyncSession) -> Optional[Menu]:
        trashed = await AuditLog().is_trashed(Menu)
        q = (
            select(Menu)
            .options(
                joinedload(Menu.audit_logs),
                joinedload(Menu.audit_logs).joinedload(AuditLog.user),
                joinedload(Menu.audit_logs).joinedload(AuditLog.action),
            )
            .where(Menu.id == id)
            .filter(trashed)
        )
        menu = await session.execute(q)
        response = menu.scalars().first()
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
            )
        return response

    async def restore(self, id: int, request: Request, session: AsyncSession) -> dict:
        response = await self.find_trash(id, request, session)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
            )

        await self.activity_log(request=request,body={"action_id":await self.action_type("RESTORE", session),"record_id":id,"model_name":Menu.__tablename__},session=session)

        return response
