from fastapi.testclient import TestClient
import pytest
import asyncio
import time
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_task():
    response = client.post("/task", json={"duration": 1})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

    #await asyncio.sleep(10)
    time.sleep(10)

    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "done"}    # Всегда running !

