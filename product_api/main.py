from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool



# Dummy DB
product_list = [
    Product(id=1, name="iPhone 14", category="electronics", price=799.99, in_stock=True),
    Product(id=2, name="MacBook Air", category="electronics", price=999.99, in_stock=False),
    Product(id=3, name="Running Shoes", category="apparel", price=120.00, in_stock=True),
    Product(id=4, name="Water Bottle", category="home", price=10.00, in_stock=True),
]


@app.get("/products", response_model = List[Product])
def get_all_products():
    return product_list

@app.get("/products/search", response_model = List[Product])
def search_products(
    category: Optional[str] = None, 
    in_stock: Optional[bool] = None
):
    results = product_list
    if category:
        results = [p for p in results if p.category.lower() == category.lower() ]

    if in_stock is not None:
        resutls = [p for p in results if p.in_stock == in_stock]

    return results

@app.get("/products/{product_id}", response_model = Product)
def get_product(product_id:int):
    for product in product_list:
        if product.id == product_id:
            return product
    raise HTTPException(status_code = 404, detail = "product not found")

