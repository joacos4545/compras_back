from datetime import datetime, timezone
from decimal import Decimal

from pydantic import field_validator, model_validator
from sqlalchemy import CheckConstraint, Column, DateTime, func
from sqlmodel import Field, SQLModel


class ItemFields(SQLModel):
    name: str = Field(min_length=1, max_length=120)
    quantity: Decimal = Field(default=Decimal("1"), gt=0, max_digits=12, decimal_places=3)
    unit: str | None = Field(default=None, max_length=20)
    note: str | None = Field(default=None, max_length=500)
    unit_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    is_purchased: bool = False

    @field_validator("name")
    @classmethod
    def nonempty_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        return value


class Item(ItemFields, table=True):
    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_positive"),
        CheckConstraint("unit_price >= 0", name="unit_price_nonnegative"),
        CheckConstraint("length(trim(name)) > 0", name="name_nonempty"),
    )

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
    )


class ItemCreate(ItemFields):
    pass


class ItemUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    quantity: Decimal | None = Field(
        default=None, gt=0, max_digits=12, decimal_places=3
    )
    unit: str | None = Field(default=None, max_length=20)
    note: str | None = Field(default=None, max_length=500)
    unit_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    is_purchased: bool | None = None

    @field_validator("name")
    @classmethod
    def nonempty_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        return value

    @model_validator(mode="after")
    def required_fields_cannot_be_null(self) -> "ItemUpdate":
        for field in ("name", "quantity", "is_purchased"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} no puede ser null")
        return self


class ItemRead(ItemFields):
    id: int
    created_at: datetime
    total: Decimal | None


