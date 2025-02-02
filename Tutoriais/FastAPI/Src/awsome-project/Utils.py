from enum import Enum
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


def get_model_impl(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


def get_fakedb_itens(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


class Item(BaseModel):
    name: str = ""
    description: str = ""
    price: float = 0.0
    tax: float = 0.0



