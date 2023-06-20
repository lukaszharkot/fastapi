from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MenuCreateSchema(BaseModel):
    nazwa: str
    cena: int

    class Config:
        schema_extra = {
            "example": {
                "nazwa": "Spaghetti Carbonara",
                "cena": 32,
            }
        }
    
class OrderCreateSchema(BaseModel):
    dishes: list

    class Config:
        schema_extra = {
            "example": {
                "dishes": [1, 2, 3],
            }
        }

class Dish(BaseModel):
    id: int
    nazwa: str
    cena: int

class Order(BaseModel):
    id: int
    dishes: list

menus = {}
orders = {}

@app.get("/menus")
async def get_menus():
    return menus

@app.get("/orders")
async def get_orders():
    return orders

@app.post("/menus")
async def create_menu(menu: MenuCreateSchema):
    id = len(menus) + 1
    new_dish = Dish(**menu.dict(), id=id)
    menus[id] = new_dish
    return new_dish

@app.post("/orders")
async def create_order(order: OrderCreateSchema):
    id = len(orders) + 1
    order_dishes = []
    for dish_id in order.dishes:
        if dish_id in menus:
            dish = menus[dish_id]
            order_dishes.append(dish)
    new_order = Order(id=id, dishes=order_dishes)
    orders[id] = new_order
    return new_order
