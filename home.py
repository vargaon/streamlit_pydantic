import streamlit as st
from typing import Literal, Annotated

from pydantic import BaseModel, Field

from generator import generate_inputs

Types = Literal["this", "that", "them"]


class NestedNested(BaseModel):
    hobby: str


class Nested(BaseModel):
    street: str
    city: str
    nested_nested: "NestedNested"


class MyModel(BaseModel):
    name: Annotated[str, Field(description="Name of user")] = "test"
    age: int = 10
    address: Nested
    my_num: int = Field(le=10, ge=2)
    my_num1: int = Field(lt=9, gt=3)
    type_s: Types = "this"
    arr1: list[int]
    arr2: list[str] = ["hello", "world"]
    arr3: list[Types]


st.title("Hello world")

generate_inputs(
    MyModel(
        name="Name",
        age=24,
        address=Nested(
            street="Street1", city="City1", nested_nested=NestedNested(hobby="Sport"), arr1=[]
        ),
        my_num=3,
        my_num1=4,
        arr1=[1, 2],
        arr3=["that", "this"],
    )
)
