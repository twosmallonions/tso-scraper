from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScrapeRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class ScrapeResponse(_message.Message):
    __slots__ = ("author", "canonical_url", "category", "cook_time", "description", "image", "ingredients", "instructions", "instructions_list", "keywords", "language", "prep_time", "title", "total_time", "cuisine", "host", "ingredient_groups")
    class IngredientGroup(_message.Message):
        __slots__ = ("ingredients", "purpose")
        INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
        PURPOSE_FIELD_NUMBER: _ClassVar[int]
        ingredients: _containers.RepeatedScalarFieldContainer[str]
        purpose: str
        def __init__(self, ingredients: _Optional[_Iterable[str]] = ..., purpose: _Optional[str] = ...) -> None: ...
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_URL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    COOK_TIME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PREP_TIME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TIME_FIELD_NUMBER: _ClassVar[int]
    CUISINE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    INGREDIENT_GROUPS_FIELD_NUMBER: _ClassVar[int]
    author: str
    canonical_url: str
    category: str
    cook_time: int
    description: str
    image: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    instructions: str
    instructions_list: _containers.RepeatedScalarFieldContainer[str]
    keywords: _containers.RepeatedScalarFieldContainer[str]
    language: str
    prep_time: int
    title: str
    total_time: int
    cuisine: str
    host: str
    ingredient_groups: _containers.RepeatedCompositeFieldContainer[ScrapeResponse.IngredientGroup]
    def __init__(self, author: _Optional[str] = ..., canonical_url: _Optional[str] = ..., category: _Optional[str] = ..., cook_time: _Optional[int] = ..., description: _Optional[str] = ..., image: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., instructions: _Optional[str] = ..., instructions_list: _Optional[_Iterable[str]] = ..., keywords: _Optional[_Iterable[str]] = ..., language: _Optional[str] = ..., prep_time: _Optional[int] = ..., title: _Optional[str] = ..., total_time: _Optional[int] = ..., cuisine: _Optional[str] = ..., host: _Optional[str] = ..., ingredient_groups: _Optional[_Iterable[_Union[ScrapeResponse.IngredientGroup, _Mapping]]] = ...) -> None: ...
