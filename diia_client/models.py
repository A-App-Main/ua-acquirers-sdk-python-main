import re

from pydantic import BaseModel as PydanticBaseModel


ua_suffix_regex = re.compile("_ua$")
en_suffix_regex = re.compile("_en$")


def to_camel(string: str) -> str:
    # hack for suffixes *_ua -> *UA, *_en -> *EN
    string = re.sub(ua_suffix_regex, "_u_a", string)
    string = re.sub(en_suffix_regex, "_e_n", string)

    return "".join(
        word if idx == 0 else word.capitalize()
        for idx, word in enumerate(string.split("_"))
    )


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True
