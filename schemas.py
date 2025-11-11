"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
    image: Optional[str] = Field(None, description="Primary image URL")
    images: Optional[List[str]] = Field(default_factory=list, description="Additional image URLs")
    colors: Optional[List[str]] = Field(default_factory=list, description="Available colors")
    sizes: Optional[List[str]] = Field(default_factory=list, description="Available sizes")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating 0-5")
    featured: bool = Field(False, description="Featured on homepage")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    title: str = Field(..., description="Snapshot of product title at purchase time")
    price: float = Field(..., ge=0, description="Unit price at purchase time")
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    color: Optional[str] = Field(None, description="Selected color")
    size: Optional[str] = Field(None, description="Selected size")
    image: Optional[str] = Field(None, description="Thumbnail image")

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order" (lowercase of class name)
    """
    items: List[OrderItem] = Field(..., description="List of items in the order")
    subtotal: float = Field(..., ge=0, description="Subtotal amount")
    shipping: float = Field(..., ge=0, description="Shipping cost")
    total: float = Field(..., ge=0, description="Total amount")
    customer_name: Optional[str] = Field(None, description="Customer full name")
    customer_email: Optional[str] = Field(None, description="Customer email")
    address: Optional[str] = Field(None, description="Shipping address")
