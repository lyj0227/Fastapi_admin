import importlib
import sys
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport

# 包导入有点问题
sys.path.append(str(Path(__file__).resolve().parent.parent))
main_module = importlib.import_module("main")
app = main_module.app


@pytest.mark.anyio
async def test_main():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:3000"
    ) as ac:
        response = await ac.post(
            "/admin/login", data={"username": "admins", "password": "123456"}
        )
        print(response)
        assert response.status_code == 200
