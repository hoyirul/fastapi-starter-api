from datetime import datetime
from sqlalchemy.future import select
from sqlmodel import SQLModel, Session
from .errors import DuplicateRecord
from sqlalchemy.sql import func

class DuplicateChecker:
    def __init__(self, model: SQLModel, session: Session):
        self.model = model
        self.session = session

    async def check(self, filters: dict) -> bool:
        """
        This method checks if a record with the given filters already exists in the database.
        
        :param filters: The filters to be used in the query
        :return: True if the record exists, False otherwise
        """
        # Make a query to check if the record already exists based on the filters
        conditions = []
        
        for key, value in filters.items():
            column = getattr(self.model, key)

            # If the value is a string, compare the lowercase version of the column and the value
            if isinstance(value, str):
                conditions.append(func.lower(func.trim(column)) == func.lower(func.trim(value)))
            elif isinstance(value, bool):
                # For boolean values, compare directly
                conditions.append(column == value)
            elif isinstance(value, (int, float)):
                # For integer or float values, compare directly
                conditions.append(column == value)
            else:
                # If the value is not a string, compare the column and the value
                conditions.append(func.trim(func.cast(column, str)) == func.trim(str(value)))
        
        # Create the query
        stmt = select(self.model).where(*conditions)
        
        # Execute the query
        result = await self.session.execute(stmt)
        existing_data = result.scalars().first()
        
        if existing_data:
            raise DuplicateRecord()
        
        return False

