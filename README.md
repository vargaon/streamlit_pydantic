# Pydantic Streamlit Generator

## Usage

1) Define data model using [Pydantic](https://docs.pydantic.dev/latest/)
2) Generate [Streamlit](https://streamlit.io) form


![Simple example image](/imgs/simple_example.png "Simple Example")

```python
def generate_form(
    model: BaseModel | type[BaseModel],
    form_label: str | None = None,
    submit_btn_label: str = "Submit",
    show_form_label: bool = True,
) -> BaseModel | None:
    """Generates a form according to the Pydantic model, if the form is submitted it returns an instance of the model.

    :param model: Pydantic model or its instances
    :type model: BaseModel | type[BaseModel]
    :param form_label: Form label, defaults to None
    :type form_label: str | None, optional
    :param submit_btn_label: Submit button label, defaults to "Submit"
    :type submit_btn_label: str, optional
    :param show_form_label: If True, show form label, defaults to True
    :type show_form_label: bool, optional
    :return: Pydantic model instance
    :rtype: BaseModel | None
    """

```

## Supported Types

- ### Bool
- ### Int
    - **le**: sets the minimum
    - **lt**: sets the exclusive minimum
    - **ge**: sets the maximum
    - **gt**: sets the exclusive maximum
    - **multiple_of**: sets step
- ### Float
    - **le**: sets the minimum
    - **lt**: sets the exclusive minimum
    - **ge**: sets the maximum
    - **gt**: sets the exclusive maximum
- ### Str
    - **max_length**: sets maximum number of characters
- ### SecretStr
    - **max_length**: sets maximum number of characters
- ### Date
- ### Time
- ### Datetime
- ### List
    - **max_length**: sets maximum number of list elements
- ### Dict
    - **max_length**: sets maximum number of key-value pairs
- ### Color

## List

Supports the following element types:
- Int
- Float
- Str
- Date
- Time
- Datetime
- Color

Generates an interface for adding and removing elements

![List input](/imgs/list_input.png "List Input")

## Dict

Supports the following value types:
- Int
- Float
- Str
- Date
- Time
- Datetime
- Color

Generates an interface for adding and removing key-value pairs

![Dict input](/imgs/dict_input.png "Dict Input")

## Nesting

The generator supports nested types. If a model has a parameter defined with a nested type, the generator generates a subarea in the form that matches that type.

![Nested type](/imgs/nested_type.png "Nested Type")

## Input Validation

After the form is submitted, it tries to create an instance of the inserted model. If a ValidationError occurs error messages are applied to specific inputs and displayed. 

## Run Example App

Run following commands to install dependencies and run streamlit app:
```bash
$ make install && make run
```

Example app is [here](http://localhost:8501)

### Requirements
- python == 3.11
- poetry == 1.7.0
