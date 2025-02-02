from fastapi import FastAPI, Query
from typing import Annotated
from typing import List, Union
from enum import Enum
from pydantic import BaseModel
from Utils import ModelName, get_model_impl, get_fakedb_itens, Item


print("=====================================================")
print("Initializing FastAPI Application")
print("=====================================================")
app = FastAPI()


#
# API
#

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return get_model_impl(model_name)


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return get_fakedb_itens(skip=skip, limit=limit)


@app.post("/items/")
async def create_item(item: Item):
    """
    {
        "name": "Foo",
        "description": "An optional description",
        "price": 45.2,
        "tax": 3.5
    }
    """
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.get("/items2/")
async def read_items(q: str):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items3/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items

