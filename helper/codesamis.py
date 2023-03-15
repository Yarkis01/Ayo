import aiosqlite

class Database:
    def __init__(self, path: str):
        self.__path = path

    async def __get(self, request: str) -> tuple:
        async with aiosqlite.connect(self.__path) as db:
            async with db.execute(request) as cursor:
                return await cursor.fetchall()
            
    async def __set(self, request: str) -> None:
        async with aiosqlite.connect(self.__path) as db:
            await db.execute(request)
            await db.commit()

    async def create_if_not_exists(self):
        await self.__set("""
            CREATE TABLE IF NOT EXISTS "CA" ("id" TEXT, "ds" TEXT, "wiiu" TEXT, "switch" TEXT, "pogo" TEXT, "shuffle" TEXT, "master" TEXT, "home" TEXT, "cafemix" TEXT, PRIMARY KEY("id"));
        """)

    async def is_user_exists(self, user_id: int) -> bool:
        data = await self.__get(f"SELECT * FROM 'CA' WHERE id = {user_id}")
        print(data)