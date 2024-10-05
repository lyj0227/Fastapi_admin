import importlib
import sys
import pytest
from pathlib import Path
from tortoise import Tortoise

sys.path.append(str(Path(__file__).resolve().parent.parent))
main_module = importlib.import_module("main")
app = main_module.app


# 测试mysql连接
@pytest.fixture(scope="module", autouse=True)
async def init_sql():
    await Tortoise.init(
        db_url="mysql://root:lyj227@localhost:3306/fastapi_admin",
        modules={"models": ["api.v1.admin_user.models"]},
        timezone="Asia/Shanghai",
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
