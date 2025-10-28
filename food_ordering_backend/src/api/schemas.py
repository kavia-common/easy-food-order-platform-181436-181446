from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Auth
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# Restaurants and Menus
class RestaurantOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: Optional[str] = None
    price_cents: int

    class Config:
        from_attributes = True


# Orders
class CartItem(BaseModel):
    menu_item_id: int = Field(..., description="ID of menu item")
    quantity: int = Field(..., ge=1, description="Quantity of the item")


class CreateOrderRequest(BaseModel):
    restaurant_id: int = Field(..., description="ID of the restaurant")
    items: List[CartItem] = Field(..., description="Cart items for the order")


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price_cents: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: str
    total_cents: int
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


# Payments (stub)
class CreateCheckoutSessionRequest(BaseModel):
    order_id: int = Field(..., description="ID of the order to pay for")


class CreateCheckoutSessionResponse(BaseModel):
    checkout_url: str = Field(..., description="URL to redirect user to checkout page (stubbed)")
