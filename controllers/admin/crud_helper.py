from config.mongo_collection import ADMIN
from controllers.util.crud import find_one_on_db, insert_one_on_db
from models.user.admin import Admin, OutputAdmin


async def get_admin_on_db(criteria: dict) -> OutputAdmin:
    admin = await find_one_on_db(criteria=criteria, collection=ADMIN)
    if admin:
        return OutputAdmin(**admin)
    return None


async def insert_admin_to_db(admin: Admin):
    await insert_one_on_db(collection=ADMIN, data=admin.dict())
