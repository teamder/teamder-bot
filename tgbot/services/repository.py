from typing import Any, Dict, Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from tgbot.database.tables import users


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn: AsyncConnection):
        self.conn: AsyncConnection = conn

    # users
    async def add_user(
        self,
        user_id: int,
        firstname: str,
        lastname: Optional[str],
        username: Optional[str],
        lang: Optional[str] = None
    ) -> None:
        """Store user in DB, ignore duplicates

        :param user_id: User's telegram id
        :type user_id: int
        :param firstname: User's firstname
        :type firstname: str
        :param lastname: User's lastname
        :type lastname: Optional[str]
        :param lastname: User's username
        :type lastname: Optional[str]
        :param lang: Language str in ISO 639-1 standart
        :type lang: Optional[str]
        """
        # Create insert statement
        stmt = insert(users).values(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            username=username,
            lang=lang
        ).on_conflict_do_nothing()

        # Execute statement
        await self.conn.execute(stmt)
        # Commit changes
        await self.conn.commit()
        return

    async def get_user(self, user_id: int) -> Optional[dict]:
        """Returns user from database by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: User data from database or None if user not exists
        :rtype: Optional[dict]
        """
        # Create statement
        stmt = select(users).where(
            users.c.user_id == user_id
        )

        # Execute statement
        res = self.conn.execute(stmt)
        try:
            # Try to return one result
            return res.mappings().one()

        except NoResultFound:
            # If no results found return None
            return None

    async def list_users(self) -> Optional[Dict[str, Any]]:
        """List all bot users"""
        # Create statement
        stmt = select(users)

        # Execute statement
        res = await self.conn.execute(stmt)
        # Return all found data in list of dicts or None
        return res.mappings().all()

    async def update_user_lang(self, user_id: int, lang: str) -> None:
        """Updates user language

        :param user_id: User's telegram id
        :type user_id: int
        :param lang: Language str in ISO 639-1 standart
        :type lang: str
        """
        # Create statement
        stmt = update(users).values(
            lang=lang
        ).where(
            users.c.user_id == user_id
        )

        await self.conn.execute(stmt)
        await self.conn.commit()
        return
