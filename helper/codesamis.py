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
        return bool(await self.__get(f"SELECT * FROM 'CA' WHERE id = {user_id}"))
    
    async def add_user(self, user_id: int) -> None:
        await self.__set(f"INSERT INTO 'CA' VALUES({user_id}, '0', '0', '0', '0', '0', '0', '0', '0')")

    async def create_user_if_not_exists(self, user_id: int) -> None:
        if not await self.is_user_exists(user_id):
            await self.add_user(user_id)

    async def get_friends_codes(self, user_id: int) -> tuple:
        if not await self.is_user_exists(user_id):
            return None

        data = await self.__get(f"SELECT ds, switch, home, pogo, master, shuffle, cafemix FROM 'CA' WHERE id = {user_id}")
        return data[0]
    
    async def change_friend_code(self, user_id: int, code_type: str, code: str) -> None:
        if not await self.is_user_exists(user_id):
            return
        
        await self.__set(f"UPDATE 'CA' SET {code_type} = '{code}' WHERE id = {user_id}")

    async def delete_friend_code(self, user_id: int, code_type) -> None:
        await self.change_friend_code(user_id, code_type, "0")



class CodeChecker:
    def __init__(self):
        super().__init__()

    def check(self, code_type: str, code: str) -> bool:
        match code_type:
            case code_type if code_type in {"ds", "pogo"}:
                return self.__check_common_code(code)
            case "switch":
                return self.__check_common_code(code.lower().replace("sw-", ""))
            case "home":
                return len(code) == 12 and code.isalpha()
            case "master":
                return self.__check_master(code)
            case "shuffle":
                return len(code) == 8 and code.isalnum()
            case "cafemix":
                return self.__check_common_code(code, True)
            case _:
                return False
            
    def format(self, code_type: str, code: str) -> str:
        match code_type:
            case code_type if code_type in {"ds", "pogo"}:
                return code if len(code) == 14 else f"{code[:4]}-{code[4:8]}-{code[8:12]}"
            case "switch":
                code = code.lower().replace("sw-", "")
                return "sw-" + (code if len(code) == 14 else f"{code[:4]}-{code[4:8]}-{code[8:12]}")
            case code_type if code_type in {"home", "shuffle"}:
                return code.upper()
            case "master":
                return code if len(code) == 19 else f"{code[:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"
            case "cafemix":
                return (code if len(code) == 14 else f"{code[:4]}-{code[4:8]}-{code[8:12]}").upper()
            case _:
                return "0"
            
    def __check_common_code(self, code: str, is_alnum: bool = False) -> bool:
        if len(code) not in [12, 14]:
            return False

        split = code.split("-") if len(code) == 14 else [code[:4], code[4:8], code[8:12]]

        if len(split) != 3 or len(split[0]) != 4 or len(split[1]) != 4 or len(split[2]) != 4:
            return False

        if is_alnum:
            return bool(split[0].isalnum() and split[1].isalnum() and split[2].isalnum())
        else:
            return bool(split[0].isdigit() and split[1].isdigit() and split[2].isdigit())
    
    def __check_master(self, code: str) -> bool:
        if len(code) not in [16, 19]:
            return False

        split = code.split("-") if len(code) == 19 else [code[:4], code[4:8], code[8:12], code[12:16]]
            
        if len(split) != 4 or len(split[0]) != 4 or len(split[1]) != 4 or len(split[2]) != 4 or len(split[3]) != 4:
            return False

        return bool(split[0].isdigit() and split[1].isdigit() and split[2].isdigit() and split[3].isdigit())