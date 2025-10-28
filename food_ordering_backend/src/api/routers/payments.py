import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_current_user
from ..models import User, Order
from ..schemas import CreateCheckoutSessionRequest, CreateCheckoutSessionResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/create-checkout-session",
    response_model=CreateCheckoutSessionResponse,
    summary="Create a Stripe checkout session (stubbed)",
    description="Creates a mock checkout URL for payment. If STRIPE_* env vars are set, this can be wired later.",
)
async def create_checkout_session(
    payload: CreateCheckoutSessionRequest,
    session: AsyncSession = Depends(...),
    current_user: User = Depends(get_current_user),
):
    async for s in session.__class__(**session.__dict__):
        pass  # pragma: no cover

    # Validate order ownership and status
    result = await session.execute(select(Order).where(Order.id == payload.order_id, Order.user_id == current_user.id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Stubbed URL; in future integrate stripe and return redirect URL
    frontend_url = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    checkout_url = f"{frontend_url}/order-success?order_id={order.id}"

    # Optionally mark as paid directly in stub mode
    if os.getenv("PAYMENT_AUTO_COMPLETE", "true").lower() == "true":
        order.status = "paid"
        await session.commit()

    return CreateCheckoutSessionResponse(checkout_url=checkout_url)
