from typing import Any, Annotated, Literal, Callable

from pydantic import BaseModel, Field
import streamlit as st
import streamlit_nested_layout

PropertyType = Literal["string", "integer", "number", "array"]


class ArrayItemType(BaseModel):
    type: PropertyType
    enum: list[Any] | None = None


class Property(BaseModel):
    title: str
    description: str | None = None
    default: Any | None = None
    maximum: int | None = None
    minimum: int | None = None
    exclusiveMaximum: int | None = None
    exclusiveMinimum: int | None = None
    type: PropertyType
    enum: list[int | float | str] | None = None
    items: ArrayItemType | None = None


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


def generate_inputs(model: BaseModel) -> dict[str, Any]:
    schema = Schema(**model.model_json_schema(ref_template="{model}"))

    with st.expander("", expanded=True):
        values = _gen(schema, model.model_dump())

        if st.button("submit"):
            st.json(values)


def _gen(schema: Schema, values: dict | None = None) -> dict[str, Any]:
    if values is None:
        values = {}

    for prop_key, p in schema.properties.items():
        if isinstance(p, Property):
            values[prop_key] = _get_input(p, values.get(prop_key))
        elif isinstance(p, NestedProperty):
            with st.expander(label=p.reference, expanded=True):
                nested_schema = schema.definitions[p.reference]
                nested_schema.definitions = schema.definitions
                values[prop_key] = _gen(nested_schema, values.get(prop_key))

    return values


def _get_input(p: Property, value: Any | None = None) -> Any:
    if p.enum is not None:
        return _enum_input(p, value)
    else:
        match p.type:
            case "integer":
                return _integer_input(p, value)
            case "string":
                return _string_input(p, value)
            case "number":
                return _number_input(p, value)
            case "array":
                return _array_input(p, value)


def _integer_input(p: Property, value: int | None = None) -> int:
    value = int(value) if value is not None else p.default

    return st.number_input(label=p.title, help=p.description, step=1, value=value)


def _number_input(p: Property, value: float | None = None) -> float:
    value = float(value) if value is not None else p.default

    return st.number_input(label=p.title, help=p.description, value=value)


def _string_input(p: Property, value: str | None = None) -> str:
    value = str(value) if value is not None else p.default

    return st.text_input(label=p.title, value=value, help=p.description)


def _enum_input(p: Property, value: Any | None = None) -> Any:
    value = value if value is not None else p.default

    if value is not None:
        default_index = p.enum.index(value)
    else:
        default_index = 0

    return st.selectbox(label=p.title, options=p.enum, index=default_index, help=p.description)


def _integer_item_input(key: str, value: int | None = None) -> Any:
    value = int(value) if value is not None else None

    return st.number_input(label="", key=key, value=value, step=1, label_visibility="collapsed")


def _number_item_input(key: str, value: float | None = None) -> Any:
    value = float(value) if value is not None else None

    return st.number_input(label="", key=key, value=value, label_visibility="collapsed")


def _string_item_input(key: str, value: str | None = None) -> Any:
    value = str(value) if value is not None else None

    return st.text_input(label="", key=key, value=value, label_visibility="collapsed")


def _get_enum_item_input(options: list[Any]) -> Callable:
    def _inner(key: str, value: Any | None = None) -> Any:
        if value is not None:
            default_index = options.index(value)
        else:
            default_index = 0

        return st.selectbox(
            label="", key=key, options=options, index=default_index, label_visibility="collapsed"
        )

    return _inner


def _array_input(p: Property, values: list[Any] | None = None) -> list[Any]:
    st.text(p.title)
    key = f"array_{p.title}"

    initialize = False

    if key not in st.session_state:
        st.session_state[key] = {}
        initialize = True

    elements = st.session_state[key]

    if p.items.enum is not None:
        input_fnc = _get_enum_item_input(p.items.enum)
    else:
        match p.items.type:
            case "integer":
                input_fnc = _integer_item_input
            case "number":
                input_fnc = _number_item_input
            case "string":
                input_fnc = _string_item_input

    def _add_item_input(value: Any | None = None) -> Callable:
        index = max(elements.keys()) + 1 if len(elements) > 0 else 0

        def _inner() -> Any:
            c1, c2 = st.columns((9, 1))
            with c1:
                res = input_fnc(f"{key}_{index}", value)
            with c2:
                if st.button("X", use_container_width=True, key=f"rmbtn_{key}_{index}"):
                    del elements[index]
                    st.experimental_rerun()

            return res

        elements[index] = _inner

    if initialize and values is not None:
        for v in values:
            _add_item_input(v)

    arr = [i() for i in elements.values()]

    if st.button("\+ Item", key=f"{p.title}_btn"):
        _add_item_input()
        st.experimental_rerun()

    return arr
