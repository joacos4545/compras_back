from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db import get_session
from app.models import Item, ItemCreate, ItemRead, ItemUpdate


router = APIRouter(prefix="/items", tags=["items"])
DbSession = Annotated[Session, Depends(get_session)]


def as_response(item: Item) -> ItemRead:
    total = None
    if item.unit_price is not None:
        total = (item.quantity * item.unit_price).quantize(Decimal("0.01"))
    return ItemRead(**item.model_dump(), total=total)


def find_item(session: Session, item_id: int) -> Item:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return item


@router.get("", response_model=list[ItemRead])
def list_items(session: DbSession) -> list[ItemRead]:
    items = session.exec(select(Item).order_by(Item.created_at, Item.id)).all()
    return [as_response(item) for item in items]


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, session: DbSession) -> ItemRead:
    item = Item.model_validate(payload)
    session.add(item)
    session.commit()
    session.refresh(item)
    return as_response(item)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, session: DbSession) -> ItemRead:
    item = find_item(session, item_id)
    item.sqlmodel_update(payload.model_dump(exclude_unset=True))
    session.add(item)
    session.commit()
    session.refresh(item)
    return as_response(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: DbSession) -> Response:
    item = find_item(session, item_id)
    session.delete(item)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


