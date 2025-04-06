# src/utils/logging.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

import sys
from loguru import logger  # Use the global loguru logger
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status, Request
from sqlalchemy.sql import select
from datetime import datetime


class Logging:
    def __init__(self, level="DEBUG"):
        """
        Initializes the Logger instance with a specified log level.
        Default is 'DEBUG'.
        """
        self.level = level
        self.configure_logger()

    def configure_logger(self):
        """
        Configures the loguru logger with colorized output and custom log format.
        """
        logger.remove()  # Remove the default logger configuration (This should be called on the global `logger`)

        # Add a new handler for logging to the console with color and custom format
        logger.add(
            sys.stdout,  # Output to console
            # asctime, levelname, message
            format="{time:YYYY-MM-DD HH:mm:ss,SSS} <level>{level}</level> <level>{message}</level>",
            level=self.level,  # Set the log level dynamically
            colorize=True,  # Enable colorized output
        )

        # Customize log levels and their colors
        logger.level("INFO", color="<green>")  # Green for INFO
        logger.level("ERROR", color="<red>")  # Red for ERROR
        logger.level("WARNING", color="<yellow>")  # Yellow for WARNING
        logger.level("DEBUG", color="<cyan>")  # Cyan for DEBUG
        logger.level("CRITICAL", color="<magenta>")  # Magenta for CRITICAL

    def log(self, level, message):
        """
        Log a message at a specific level.
        """
        if level == "debug":
            logger.debug(message)
        elif level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        elif level == "critical":
            logger.critical(message)
        else:
            logger.info(message)

    def set_level(self, level):
        """
        Set the logging level dynamically (e.g., DEBUG, INFO, WARNING, etc.)
        """
        self.level = level
        logger.remove()  # Remove previous logger configuration
        self.configure_logger()  # Reconfigure logger with new level


class ActivityLog(Logging):
    def __init__(self, level="DEBUG"):
        """
        Initializes the ActivityLog instance with a specified log level.
        Default is 'DEBUG'.
        """
        super().__init__(level=level)

    async def __call__(self, request: Request, body: dict, session: AsyncSession):
        from src.modules.logs.audit_logs.models import AuditLog

        """
        Log an activity performed by a user.
        """
        log = dict(
            user_id=int(body["user_id"]) if "user_id" in body else int(request.state.authorize["user"]["id"]),
            action_id=int(body["action_id"]),
            record_id=str(body["record_id"]),
            ip_address=body["ip_address"] if "ip_address" in body else request.state.authorize["ip_address"],
            model_name=str(body["model_name"]),
            notes=body["notes"] if "notes" in body else f"User {request.state.authorize['user']['email']} has performed an action",
        )

        # First, check if there's already a log for this action_id and record_id
        action_id = log["action_id"]
        if request.method == "DELETE":
            # If the request method is DELETE, change the action_id to 3 (Delete)
            action_id = 4  # 4 is the ID for "Restore" action
        elif request.method == "PATCH":
            # If the request method is PATCH, change the action_id to 4 (Restore)
            if action_id == 4:
                action_id = 3  # 3 is the ID for "Delete" action

        q = select(AuditLog).where(
            (AuditLog.action_id == action_id)
            & (AuditLog.record_id == log["record_id"])
            & (AuditLog.model_name == log["model_name"])
        )
        audit_log = await session.execute(q)
        existing_log = audit_log.scalars().first()
        self.log("debug", f"Existing log: {existing_log}")

        if existing_log:
            # If the log exists, update it
            existing_log.actioned_at = datetime.now()
            existing_log.ip_address = log["ip_address"]
            existing_log.notes = log["notes"]

            self.log("debug", f"Existing log: {existing_log}")

            # Handle case when action_id == 3 (Delete) and action_id in log is 4 (Restore)
            if existing_log.action_id == 3:
                # Change action_id to "Restore" (action_id == 4)
                existing_log.action_id = 4
                self.log("warning", f"Activity restored: {log}")

            # Handle case when action_id == 4 (Restore) and the user performs delete again
            elif existing_log.action_id == 4:
                # Change action_id back to "Delete" (action_id == 3)
                existing_log.action_id = 3
                self.log("warning", f"Activity deleted again: {log}")

            await session.commit()
            self.log("dabug", f"Activity updated: {log}")
            return log

        # If no log exists, create a new one
        session.add(AuditLog(**log))
        await session.commit()
        self.log("info", f"Activity logged: {log}")
        return log
