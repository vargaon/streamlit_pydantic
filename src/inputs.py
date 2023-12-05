from typing import Any, Callable
from datetime import datetime, date, time, timedelta

from pydantic_extra_types.color import Color
import streamlit as st
import streamlit_nested_layout
from streamlit_extras.stylable_container import stylable_container

from src.schemas import InputError, Property


def get_input(
    p: Property, key: str = "", value: Any | None = None, e: InputError | None = None
) -> Any:
    if p.enum is not None:
        return _enum_input(p, key, value)

    match p.type:
        case "boolean":
            return _boolean_input(p, key, value, e)
        case "integer":
            return _integer_input(p, key, value, e)
        case "string":
            if p.format == "color":
                return _color_input(p, key, value, e)
            if p.format == "date":
                return _date_input(p, key, value, e)
            if p.format == "time":
                return _time_input(p, key, value, e)
            if p.format == "date-time":
                return _date_time_input(p, key, value, e)

            return _string_input(p, key, value, e)
        case "number":
            return _number_input(p, key, value, e)
        case "array":
            return _array_input(p, key, value, e)
        case "object":
            if p.additionalProperties is not None:
                return _dict_input(p, key, value, e)


def _boolean_input(
    p: Property, key: str = "", value: bool | None = None, e: InputError | None = None
) -> bool:
    value = value if value is not None else p.default

    res = st.checkbox(
        p.title,
        value=value if value is not None else False,
        help=p.description,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _integer_input(
    p: Property, key: str = "", value: int | None = None, e: InputError | None = None
) -> int:
    value = int(value) if value is not None else p.default

    min_value = None
    max_value = None

    if p.minimum is not None:
        min_value = p.minimum
    elif p.exclusiveMinimum is not None:
        min_value = p.exclusiveMinimum + 1

    if p.maximum is not None:
        max_value = p.maximum
    elif p.exclusiveMaximum is not None:
        max_value = p.exclusiveMaximum - 1

    input = st.number_input if min_value is None or max_value is None else st.slider

    if value is None:
        if min_value is not None:
            if p.multipleOf is not None:
                value = min_value + (int(p.multipleOf) - (min_value % int(p.multipleOf)))
            else:
                value = min_value
        else:
            value = 0

    if p.multipleOf is not None:
        if value != 0 and value % int(p.multipleOf) != 0:
            if min_value is not None:
                value = min_value + (int(p.multipleOf) - (min_value % int(p.multipleOf)))
            else:
                value = 0

    res = input(
        label=p.title,
        help=p.description,
        step=int(p.multipleOf) if p.multipleOf is not None else 1,
        value=value,
        min_value=min_value,
        max_value=max_value,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _number_input(
    p: Property, key: str = "", value: float | None = None, e: InputError | None = None
) -> float:
    value = float(value) if value is not None else p.default

    min_value = None
    max_value = None

    if p.minimum is not None:
        min_value = float(p.minimum)
    elif p.exclusiveMinimum is not None:
        min_value = float(p.exclusiveMinimum + 0.01)

    if p.maximum is not None:
        max_value = float(p.maximum)
    elif p.exclusiveMaximum is not None:
        max_value = float(p.exclusiveMaximum - 0.01)

    input = st.number_input if min_value is None or max_value is None else st.slider

    if value is None:
        if min_value is not None:
            value = min_value
        else:
            value = 0.00

    res = input(
        label=p.title,
        help=p.description,
        value=value,
        min_value=min_value,
        max_value=max_value,
        step=float(p.multipleOf) if p.multipleOf is not None else 0.01,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _string_input(
    p: Property, key: str = "", value: str | None = None, e: InputError | None = None
) -> str:
    value = str(value) if value is not None else p.default

    res = st.text_input(
        label=p.title,
        value=value,
        help=p.description,
        max_chars=p.maxLength,
        key=key,
        type="password" if p.format is not None and p.format == "password" else "default",
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _enum_input(
    p: Property, key: str = "", value: Any | None = None, e: InputError | None = None
) -> Any:
    value = value if value is not None else p.default

    if value is not None:
        default_index = p.enum.index(value)
    else:
        default_index = 0

    res = st.selectbox(
        label=p.title,
        options=p.enum,
        index=default_index,
        help=p.description,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _color_input(
    p: Property, key: str = "", value: Color | None = None, e: InputError | None = None
) -> Color:
    value = (
        value.as_hex()
        if value is not None
        else (p.default.as_hex() if p.default is not None else None)
    )

    res = Color(
        st.color_picker(
            label=p.title,
            value=value,
            help=p.description,
            key=key,
            disabled=p.readOnly,
        )
    )

    if e is not None:
        st.error(e.msg)

    return res


def _date_input(
    p: Property, key: str = "", value: date | None = None, e: InputError | None = None
) -> date:
    value = value if value is not None else p.default

    res = st.date_input(
        p.title,
        help=p.description,
        value=value,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _time_input(
    p: Property, key: str = "", value: time | None = None, e: InputError | None = None
) -> time:
    value = value if value is not None else p.default

    step = timedelta(minutes=1)

    res = st.time_input(
        p.title,
        help=p.description,
        value=value,
        step=step,
        key=key,
        disabled=p.readOnly,
    )

    if e is not None:
        st.error(e.msg)

    return res


def _date_time_input(
    p: Property, key: str = "", value: datetime | None = None, e: InputError | None = None
) -> datetime:
    value = value if value is not None else p.default

    date_value, time_value = None, None

    if value is not None:
        date_value = value.date()
        time_value = value.time()

    st.text(p.title)
    with stylable_container(
        key=f"datetime_con",
        css_styles="""
                {
                    border: 1px solid #48494d;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        c1, c2 = st.columns(2)

        with c1:
            date_value = st.date_input(
                p.title,
                value=date_value,
                key=f"{key}_date",
                label_visibility="collapsed",
                disabled=p.readOnly,
            )
        with c2:
            step = timedelta(minutes=1)
            time_value = st.time_input(
                p.title,
                value=time_value,
                step=step,
                key=f"{key}_time",
                label_visibility="collapsed",
                disabled=p.readOnly,
            )

    now = datetime.now()

    if date_value is None and time_value is None:
        res = None

    else:
        res = datetime.combine(
            date_value if date_value is not None else now.date(),
            time_value if time_value is not None else now.time(),
        )

    if e is not None:
        st.error(e.msg)

    return res


def _boolean_item_input(key: str, value: bool | None = None) -> bool:
    value = value if value is not None else False

    return st.checkbox("item", value=value, key=key, label_visibility=False)


def _integer_item_input(key: str, value: int | None = None) -> Any:
    value = int(value) if value is not None else None

    if value is None:
        value = 0

    return st.number_input(
        label="item",
        key=key,
        value=value,
        step=1,
        label_visibility="collapsed",
    )


def _number_item_input(key: str, value: float | None = None) -> Any:
    value = float(value) if value is not None else None

    return st.number_input(label="item", key=key, value=value, label_visibility="collapsed")


def _string_item_input(key: str, value: str | None = None) -> Any:
    value = str(value) if value is not None else None

    return st.text_input(label="item", key=key, value=value, label_visibility="collapsed")


def _color_item_input(key: str, value: Color | None = None) -> Any:
    value = value.as_hex() if value is not None else None

    return Color(st.color_picker(label="item", key=key, value=value, label_visibility="collapsed"))


def _get_enum_item_input(options: list[Any]) -> Callable:
    def _inner(key: str, value: Any | None = None) -> Any:
        if value is not None:
            default_index = options.index(value)
        else:
            default_index = 0

        return st.selectbox(
            label="enum_item",
            key=key,
            options=options,
            index=default_index,
            label_visibility="collapsed",
        )

    return _inner


def _date_item_input(key: str, value: date | None = None) -> date | None:
    value = value if value is not None else None

    return st.date_input("date_item", value=value, key=key, label_visibility="collapsed")


def _time_item_input(key: str, value: time | None = None) -> time | None:
    value = value if value is not None else None

    step = timedelta(minutes=1)

    return st.time_input(
        "time_item", value=value, step=step, key=key, label_visibility="collapsed"
    )


def _date_time_item_input(key: str, value: datetime | None = None) -> datetime | None:
    value = value if value is not None else None

    date_value, time_value = None, None

    if value is not None:
        date_value = value.date()
        time_value = value.time()

    with stylable_container(
        key=f"datetime_con",
        css_styles="""
                {
                    border: 1px solid #48494d;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        c1, c2 = st.columns(2)

        with c1:
            date_value = st.date_input(
                "date_item",
                value=date_value,
                key=f"{key}_date",
                label_visibility="collapsed",
            )
        with c2:
            step = timedelta(minutes=1)
            time_value = st.time_input(
                "time_input",
                value=time_value,
                step=step,
                key=f"{key}_time",
                label_visibility="collapsed",
            )

    now = datetime.now()

    if date_value is None and time_value is None:
        return None

    return datetime.combine(
        date_value if date_value is not None else now.date(),
        time_value if time_value is not None else now.time(),
    )


def _array_input(
    p: Property, key: str = "", values: list[Any] | None = None, e: InputError | None = None
) -> list[Any]:
    initialize = False

    if key not in st.session_state:
        st.session_state[key] = {}
        initialize = True

    elements = st.session_state[key]

    if p.items.enum is not None:
        input_fnc = _get_enum_item_input(p.items.enum)
    else:
        match p.items.type:
            case "boolean":
                input_fnc = _boolean_item_input
            case "integer":
                input_fnc = _integer_item_input
            case "number":
                input_fnc = _number_item_input
            case "string":
                if p.items.format == "color":
                    input_fnc = _color_item_input
                elif p.items.format == "date":
                    input_fnc = _date_item_input
                elif p.items.format == "time":
                    input_fnc = _time_item_input
                elif p.items.format == "date-time":
                    input_fnc = _date_time_item_input
                else:
                    input_fnc = _string_item_input

    def _add_item_input(value: Any | None = None) -> Callable:
        index = max(elements.keys()) + 1 if len(elements) > 0 else 0

        def _inner() -> Any:
            c1, c2 = st.columns((1, 9))
            with c2:
                res = input_fnc(f"{key}_{index}", value)
            with c1:
                if st.button(":heavy_minus_sign:", key=f"rmbtn_{key}_{index}"):
                    del elements[index]
                    st.experimental_rerun()

            return res

        elements[index] = _inner

    st.text(p.title)
    with stylable_container(
        key=f"array_con_{key}",
        css_styles="""
                {
                    border: 1px solid #48494d;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        if initialize and values is not None:
            for v in values:
                _add_item_input(v)

        arr = [i() for i in elements.values()]

        if p.maxItems is None or len(elements) < p.maxItems:
            if st.button(":heavy_plus_sign:", key=f"{p.title}_btn"):
                _add_item_input()
                st.experimental_rerun()

    res = [a for a in arr if a is not None]

    if e is not None:
        st.error(e.msg)

    return res


def _dict_input(
    p: Property, key: str = "", values: dict[str, Any] | None = None, e: InputError | None = None
) -> dict[str, Any]:
    initialize = False

    if key not in st.session_state:
        st.session_state[key] = {}
        initialize = True

    records = st.session_state[key]

    if p.additionalProperties.enum is not None:
        input_fnc = _get_enum_item_input(p.items.enum)
    else:
        match p.additionalProperties.type:
            case "boolean":
                input_fnc = _boolean_item_input
            case "integer":
                input_fnc = _integer_item_input
            case "number":
                input_fnc = _number_item_input
            case "string":
                if p.additionalProperties.format == "color":
                    input_fnc = _color_item_input
                elif p.additionalProperties.format == "date":
                    input_fnc = _date_item_input
                elif p.additionalProperties.format == "time":
                    input_fnc = _time_item_input
                elif p.additionalProperties.format == "date-time":
                    input_fnc = _date_time_item_input
                else:
                    input_fnc = _string_item_input

    def _add_item_input(value: Any | None = None) -> Callable:
        index = max(records.keys()) + 1 if len(records) > 0 else 0

        def _inner() -> Any:
            if value is not None:
                vk, vv = value
            else:
                vk, vv = None, None
            c1, c2 = st.columns((1, 9))
            with c2:
                c11, c22 = st.columns((2, 3))
                with c11:
                    item_key = st.text_input(
                        "item_key",
                        value=vk,
                        key=f"{key}_{index}_key",
                        label_visibility="collapsed",
                    )
                with c22:
                    item_value = input_fnc(f"{key}_{index}_value", vv)
            with c1:
                if st.button(":heavy_minus_sign:", key=f"rmbtn_{key}_{index}"):
                    del records[index]
                    st.experimental_rerun()

            return item_key, item_value

        records[index] = _inner

    st.text(p.title)
    with stylable_container(
        key=f"dict_con",
        css_styles="""
                {
                    border: 1px solid #48494d;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        if initialize and values is not None:
            for k, v in values.items():
                _add_item_input((k, v))

        res = dict([i() for i in records.values()])

        if p.maxItems is None or len(records) < p.maxItems:
            if st.button(":heavy_plus_sign:", key=f"{p.title}_btn"):
                _add_item_input()
                st.experimental_rerun()

    res = {k: v for k, v in res.items() if v is not None}

    if e is not None:
        st.error(e.msg)

    return res
