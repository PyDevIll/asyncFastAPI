import asyncio

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uuid
from pydantic import BaseModel

app = FastAPI()
tasks = {}      # хранит статусы задач
asyncio_tasks = []


class TaskModel(BaseModel):
    duration: int


async def task_worker(task_id, duration):
    await asyncio.sleep(duration)
    tasks[task_id] = "done"


#            параметры в запросе POST попадают в параметры функции, в соответствии с TaskModel
@app.post("/task", response_model=dict)
async def create_task(task_model: TaskModel):
    task_id = str(uuid.uuid4())
    tasks[task_id] = "running"
#            asyncio.create_task используется для создания объекта asyncio.Task из корутины,
#            чтобы можно было запускать ее параллельно, а не ждать его завершения
    _task = asyncio.create_task(task_worker(task_id, task_model.duration))
    asyncio_tasks.append(_task)
    return JSONResponse(content={"task_id": task_id})


#            параметр в скобках {} попадает в параметр функции.
#            Можно указать тип в параметре ф-ии, и он будет преобразован в этот тип
@app.get("/task/{task_id}", response_model=dict)
async def check_task(task_id: str):
    return JSONResponse(content={"status": tasks[task_id]})
