from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

products: List[Product] = []

@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    for existing_product in products:
        if existing_product.id == product.id:
            raise HTTPException(status_code=400, detail="Product already exists")
    products.append(product)
    return product

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)