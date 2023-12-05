from typing import Annotated, Literal
from datetime import date
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color
import streamlit as st
from src import generate_form

GenderType = Literal["Male", "Female", "Something else"]


class Address(BaseModel):
    street: str
    city: str


class Person(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    gender: GenderType
    date_of_birth: date
    email: Annotated[str, Field(pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")]
    address: Address
    hobbies: Annotated[list[str], Field(min_length=1)]
    favorite_color: Color


st.header("Complex Form")
st.code(
    """
        GenderType = Literal["Male", "Female", "Something else"]


        class Address(BaseModel):
            street: str
            city: str


        class Person(BaseModel):
            first_name: Annotated[str, Field(min_length=1, max_length=100)]
            last_name: Annotated[str, Field(min_length=1, max_length=100)]
            gender: GenderType
            date_of_birth: date
            email: Annotated[
                str, 
                Field(pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            ]
            address: Address
            hobbies: Annotated[list[str], Field(min_length=1)]
            favorite_color: Color
        """,
    language="python",
)

if (person_body := generate_form(Person, show_form_label=False)) is not None:
    st.json(person_body.model_dump())
