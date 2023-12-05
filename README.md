# Pydantic Streamlit Generator

## Usage

1) Define data model using [Pydantic](https://docs.pydantic.dev/latest/)
2) Generate [Streamlit](https://streamlit.io) form


```python
class Login(BaseModel):
    username: Annotated[str, Field(min_length=3)]
    password: Annotated[SecretStr, Field(min_length=6)]

login_body = generate_form(Login)
```

## Run Example App

Run following commands to install dependencies and run strealit app:
```bash
$ make install && make run
```

Example app is [here](http://localhost:8501)

### Requirements
- python == 3.11
- poetry == 1.7.0