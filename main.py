import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Order

app = FastAPI(title="Clothing Store API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Clothing Store Backend running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                response["collections"] = db.list_collection_names()[:10]
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Seed some demo products if collection empty
@app.post("/seed")
def seed_products():
    try:
        count = db["product"].count_documents({}) if db else 0
        if count > 0:
            return {"status": "ok", "message": "Products already seeded"}
        demo_products = [
            Product(title="AeroFlex Tee", description="Breathable performance tee", price=29.99, category="Tops", in_stock=True, image="https://images.unsplash.com/photo-1520975682031-5fdb9186b8a0?q=80&w=1200&auto=format&fit=crop", colors=["Black","White","Navy"], sizes=["S","M","L","XL"], rating=4.6, featured=True),
            Product(title="Contour Jeans", description="Slim-fit stretch denim", price=59.0, category="Bottoms", in_stock=True, image="https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1200&auto=format&fit=crop", colors=["Indigo","Black"], sizes=["28","30","32","34"], rating=4.4, featured=True),
            Product(title="Nimbus Hoodie", description="Cloud-soft fleece hoodie", price=49.5, category="Outerwear", in_stock=True, image="https://images.unsplash.com/photo-1542060748-10c28b62716e?q=80&w=1200&auto=format&fit=crop", colors=["Gray","Forest","Sand"], sizes=["S","M","L","XL"], rating=4.7, featured=False),
            Product(title="Stride Sneakers", description="Lightweight everyday sneakers", price=79.0, category="Footwear", in_stock=True, image="https://images.unsplash.com/photo-1520256862855-398228c41684?q=80&w=1200&auto=format&fit=crop", colors=["White","Gray"], sizes=["7","8","9","10","11"], rating=4.5, featured=False),
        ]
        for p in demo_products:
            create_document("product", p)
        return {"status": "ok", "inserted": len(demo_products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ProductQuery(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

@app.get("/products")
def list_products(q: Optional[str] = None, category: Optional[str] = None, featured: Optional[bool] = None):
    try:
        filter_dict = {}
        if category:
            filter_dict["category"] = category
        if featured is not None:
            filter_dict["featured"] = featured
        products = get_documents("product", filter_dict)
        # simple text search client-side compatible
        if q:
            q_lower = q.lower()
            products = [p for p in products if q_lower in p.get("title","" ).lower() or q_lower in (p.get("description","" ).lower())]
        # convert ObjectId to str
        for p in products:
            if "_id" in p:
                p["id"] = str(p.pop("_id"))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AddToCartItem(BaseModel):
    product_id: str
    quantity: int = 1
    color: Optional[str] = None
    size: Optional[str] = None

@app.post("/orders")
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"status": "ok", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
