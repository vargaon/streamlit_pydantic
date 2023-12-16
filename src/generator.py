from typing import Any

from pydantic import BaseModel, ValidationError
import streamlit as st
import streamlit_nested_layout

from src.schemas import Schema, InputError, Property, NestedProperty
from src.utils import label_to_key, key_to_label, nested_container
from src.inputs import get_input


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

    schema = Schema(**model.model_json_schema(ref_template="{model}"))
    prop_keys = []

    form_key = label_to_key(schema.title)
    form_input_errors_key = f"{form_key}_input_errors"

    if isinstance(model, BaseModel):
        values = model.model_dump()
        model_class = model.__class__
    else:
        values = {}
        model_class = model

    if show_form_label:
        st.header(form_label if form_label is not None else schema.title)

    with nested_container(key=f"nested_form"):
        c1 = st.columns(1)
        with c1[0]:
            values = _generate_input(
                schema,
                label_to_key(schema.title),
                values,
                st.session_state.get(form_input_errors_key, {}),
                prop_keys,
            )

            if st.button(submit_btn_label):
                try:
                    res = model_class(**values)
                    st.session_state[form_input_errors_key] = {}
                    return res

                except ValidationError as errs:
                    errors_values = {}

                    for e in errs.errors():
                        for p in e["loc"][::-1]:
                            if p in prop_keys:
                                last_pos = p
                                break

                        temp = errors_values
                        for l in e["loc"]:
                            if l not in temp:
                                if l == last_pos:
                                    temp[l] = InputError(msg=e["msg"])
                                    break
                                else:
                                    temp[l] = {}

                            temp = temp[l]

                    st.session_state[form_input_errors_key] = errors_values
                    st.experimental_rerun()

            return None


def _generate_input(
    schema: Schema,
    key: str = "",
    values: dict | None = None,
    errors: dict[str, InputError] = {},
    prop_keys: list[str] = [],
) -> dict[str, Any]:
    if values is None:
        values = {}

    for prop_key, p in schema.properties.items():
        if isinstance(p, Property):
            prop_keys.append(prop_key)
            values[prop_key] = get_input(
                p, f"{key}_{prop_key}", values.get(prop_key), errors.get(prop_key)
            )
        elif isinstance(p, NestedProperty):
            nested_schema = schema.definitions[p.reference]
            nested_schema.definitions = schema.definitions

            st.text(key_to_label(prop_key))
            with nested_container(key=f"nested_form"):
                c = st.columns(1)
                with c[0]:
                    values[prop_key] = _generate_input(
                        nested_schema,
                        f"{key}_{prop_key}",
                        values.get(prop_key),
                        errors.get(prop_key, {}),
                        prop_keys,
                    )

    return values
