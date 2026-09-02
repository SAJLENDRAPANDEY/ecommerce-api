from pydantic import BaseModel,ConfigDict,Field


class ProductResponse(BaseModel):

    
    id: int
    name: str
    description: str
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)

class CreateProduct(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str = Field(
        min_length=5,
        max_length=500
    )

    price: float = Field(
        gt=0
    )

    stock: int = Field(
        ge=0
    )
    name: str
    description: str
    price: float
    stock: int


class ProductUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        min_length=5,
        max_length=500
    )

    price: float | None = Field(
        default=None,
        gt=0
    )

    stock: int | None = Field(
        default=None,
        ge=0
    )
    
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None