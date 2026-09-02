from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None