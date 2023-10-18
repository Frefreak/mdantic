from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Union, Literal, Dict, List


class SampleIntEnum(int, Enum):
    """
    Sample standard integer enum for testing enum-parsing capabilities
    """

    int_one = 1
    int_two = 2
    int_three = 3
    int_also_three = 3


class SampleStrEnum(str, Enum):
    """
    Sample standard string enum for testing enum-parsing capabilities
    """

    str_one = "one"
    str_two = "two"
    str_three = "three"
    str_also_three = "three"


class ContainedModel(BaseModel):
    """
    A BaseModel contained by the SampleModel
    """

    name: str = Field(..., description="A field internal to the Contained Model")


class SampleModel(BaseModel):
    """
    Sample model for testing BaseModel parsing capabilities
    """

    req_field: str = Field(..., description="Standard required string field")
    optional_field: Optional[str] = Field(None, description="Optional string field")
    alias_field: str = Field(
        ..., description="A field with an alias but no title", alias="alias_name"
    )
    title_field: str = Field(
        ..., description="A field with a title but no alias", title="title_name"
    )
    alias_title_field: str = Field(
        ...,
        description="A field with both a title and an alias",
        alias="alias_name",
        title="title_name",
    )
    example_field: str = Field(
        ...,
        description="A field that also has examples",
        examples=["example1", "example2", "example3"],
    )
    union_field: Union[str, int] = Field(
        ..., description="Field that can be an int or str"
    )
    dict_field: Dict[str, int] = Field(
        ..., description="A field that is a dict mapping str to int"
    )
    list_field: List[str] = Field(
        ..., description="A field which contains a list of strings"
    )
    int_enum_field: SampleIntEnum = Field(..., description="Integer Enum Field")
    str_enum_field: SampleStrEnum = Field(..., description="String Enum Field")
    either_enum_field: Union[SampleIntEnum, SampleStrEnum] = Field(
        ..., description="Union between two different enums"
    )
    literal_field: Literal["lit1", "lit2", "lit3"] = Field(
        ..., description="A literal string field"
    )
    default_factory_int: int = Field(
        ...,
        description="A field that uses a default factory (always 5)",
        default_factory=lambda: 5,
    )
    base_model_item: ContainedModel = Field(
        ..., description="A reference to a different base model"
    )
    base_model_dict: Dict[str, ContainedModel] = Field(
        ..., description="A field that maps str names to contained models"
    )

SAMPLE_OBJECT = SampleModel(
    req_field="req_field",
    alias_name="alias_field",
    example_field="example_field",
    union_field=5,
    dict_field={"1":1, "2":2},
    list_field=["a", "b", "c"],
    int_enum_field=SampleIntEnum.int_one,
    str_enum_field=SampleStrEnum.str_one,
    literal_field="lit1",
    base_model_item=ContainedModel(name="plain_contained"),
    base_model_dict={"contained_a": ContainedModel(name="dict_contained")},
    title_field="title_field",
    either_enum_field=SampleIntEnum.int_also_three
)