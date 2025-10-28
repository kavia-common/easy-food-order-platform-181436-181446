from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_current_user
from ..models import User, Restaurant, MenuItem, Order, OrderItem
from ..schemas import CreateOrderRequest, OrderOut, OrderItemOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderOut, summary="Create an order from cart")
async def create_order(
    payload: CreateOrderRequest,
    session: AsyncSession = Depends(...),
    current_user: User = Depends(get_current_user),
):
    # Provide session dependency this way to ensure consistent DI chain
    async for s in session.__class__(**session.__dict__):
        pass  # pragma: no cover

    # validate restaurant
    result = await session.execute(select(Restaurant).where(Restaurant.id == payload.restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart cannot be empty")

    # Create Order
    order = Order(user_id=current_user.id, restaurant_id=restaurant.id, status="pending", total_cents=0)
    session.add(order)
    await session.flush()

    total_cents = 0
    for item in payload.items:
        mi_res = await session.execute(select(MenuItem).where(MenuItem.id == item.menu_item_id, MenuItem.restaurant_id == restaurant.id))
        menu_item = mi_res.scalar_one_or_none()
        if not menu_item:
            raise HTTPException(status_code=400, detail=f"Menu item {item.menu_item_id} invalid for restaurant {restaurant.id}")
        line_total = menu_item.price_cents * item.quantity
        total_cents += line_total
        oi = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            unit_price_cents=menu_item.price_cents,
        )
        session.add(oi)

    order.total_cents = total_cents
    await session.commit()
    await session.refresh(order)

    # Load items
    await session.refresh(order, attribute_names=["items"])
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        status=order.status,
        total_cents=order.total_cents,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                id=i.id,
                menu_item_id=i.menu_item_id,
                quantity=i.quantity,
                unit_price_cents=i.unit_price_cents,
            )
            for i in order.items
        ],
    )


@router.get("", response_model=list[OrderOut], summary="List current user's orders")
async def list_my_orders(session: AsyncSession = Depends(...), current_user: User = Depends(get_current_user)):
    async for s in session.__class__(**session.__dict__):
        pass  # pragma: no cover
    result = await session.execute(select(Order).where(Order.user_id == current_user.id).order_by(Order.id.desc()))
    orders = result.scalars().all()
    # Eager fetch items
    out: list[OrderOut] = []
    for o in orders:
        await session.refresh(o, attribute_names=["items"])
        out.append(
            OrderOut(
                id=o.id,
                user_id=o.user_id,
                restaurant_id=o.restaurant_id,
                status=o.status,
                total_cents=o.total_cents,
                created_at=o.created_at,
                items=[
                    OrderItemOut(
                        id=i.id,
                        menu_item_id=i.menu_item_id,
                        quantity=i.quantity,
                        unit_price_cents=i.unit_price_cents,
                    )
                    for i in o.items
                ],
            )
        )
    return out


@router.get("/{order_id}", response_model=OrderOut, summary="Get order by id")
async def get_order(order_id: int, session: AsyncSession = Depends(...), current_user: User = Depends(get_current_user)):
    async for s in session.__class__(**session.__dict__):
        pass  # pragma: no cover
    result = await session.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.refresh(order, attribute_names=["items"])
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        status=order.status,
        total_cents=order.total_cents,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                id=i.id,
                menu_item_id=i.menu_item_id,
                quantity=i.quantity,
                unit_price_cents=i.unit_price_cents,
            )
            for i in order.items
        ],
    )
