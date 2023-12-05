from typing import Any, Annotated, Literal
from pydantic import BaseModel, Field

PropertyType = Literal["string", "integer", "number", "array", "object", "boolean"]
PropertyFormat = Literal["color", "date", "time", "date-time", "password"]


class ItemType(BaseModel):
    type: PropertyType
    enum: list[Any] | None = None
    format: PropertyFormat | None = None


class Property(BaseModel):
    title: str
    description: str | None = None
    default: Any | None = None
    multipleOf: float | None = None
    maximum: int | None = None
    minimum: int | None = None
    exclusiveMaximum: int | None = None
    exclusiveMinimum: int | None = None
    minLength: int | None = None
    maxLength: int | None = None
    minItems: int | None = None
    maxItems: int | None = None
    examples: list[Any] | None = None
    type: PropertyType
    enum: list[int | float | str] | None = None
    items: ItemType | None = None
    format: PropertyFormat | None = None
    pattern: str | None = None
    readOnly: bool = False
    additionalProperties: ItemType | None = None


class NestedProperty(BaseModel):
    reference: Annotated[str, Field(alias="$ref")]


class Schema(BaseModel):
    title: str
    properties: dict[str, Property | NestedProperty]
    required: list[str]
    definitions: Annotated[
        dict[str, "Schema"] | None,
        Field(
            alias="$defs",
        ),
    ] = None


class InputError(BaseModel):
    msg: str
