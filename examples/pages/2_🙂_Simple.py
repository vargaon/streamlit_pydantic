from typing import Annotated
from pydantic import BaseModel, SecretStr, Field
import streamlit as st
from src import generate_form


class Login(BaseModel):
    username: Annotated[str, Field(min_length=3)]
    password: Annotated[SecretStr, Field(min_length=6)]


st.header("Simple Form")
st.code(
    """
        class Login(BaseModel):
            username: Annotated[str, Field(min_length=3)]
            password: Annotated[SecretStr, Field(min_length=6)]
        """,
    language="python",
)

if (login_body := generate_form(Login, show_form_label=False)) is not None:
    st.json(login_body.model_dump())
