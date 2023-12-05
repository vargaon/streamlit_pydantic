from typing import Any
from streamlit_extras.stylable_container import stylable_container


def key_to_label(key: str) -> str:
    return " ".join([p.capitalize() for p in key.split("_")])


def label_to_key(label: str) -> str:
    return "_".join([p.lower() for p in label.split(" ")])


def nested_container(key: str) -> Any:
    return stylable_container(
        key=key,
        css_styles="""
                {
                    border: 1px solid #48494d;
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    )
