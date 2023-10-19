from mdantic import analyze, Field


def test_analyze():
    """Tests the analyze function using sample Base Models"""

    base_model_name = "mdantic.SampleModel"

    structs = analyze(base_model_name)

    expected_structs = {
        "SampleModel": [
            Field(
                key="req_field", type="str", required="True", description="Standard required string field", default=None
            ),
            Field(
                key="optional_field",
                type="typing.Optional[str]",
                required="False",
                description="Optional string field",
                default="None",
            ),
            Field(
                key="alias_field",
                type="str",
                required="True",
                description="A field with an alias but no title",
                default=None,
            ),
            Field(
                key="title_name",
                type="str",
                required="True",
                description="A field with a title but no alias",
                default=None,
            ),
            Field(
                key="title_name",
                type="str",
                required="True",
                description="A field with both a title and an alias",
                default=None,
            ),
            Field(
                key="example_field",
                type="str",
                required="True",
                description="A field that also has examples",
                default=None,
            ),
            Field(
                key="union_field",
                type="typing.Union[str, int]",
                required="True",
                description="Field that can be an int or str",
                default=None,
            ),
            Field(
                key="dict_field",
                type="typing.Dict[str, int]",
                required="True",
                description="A field that is a dict mapping str to int",
                default=None,
            ),
            Field(
                key="list_field",
                type="typing.List[str]",
                required="True",
                description="A field which contains a list of strings",
                default=None,
            ),
            Field(
                key="int_enum_field",
                type="SampleIntEnum",
                required="True",
                description="Integer Enum Field</br>SampleIntEnum: [1, 2, 3]",
                default=None,
            ),
            Field(
                key="str_enum_field",
                type="SampleStrEnum",
                required="True",
                description="String Enum Field</br>SampleStrEnum: ['one', 'two', 'three']",
                default=None,
            ),
            Field(
                key="either_enum_field",
                type="typing.Union[mdantic.samples.SampleIntEnum, mdantic.samples.SampleStrEnum]",
                required="True",
                description="Union between two different enums</br>SampleIntEnum: [1, 2, 3]</br>SampleStrEnum: ['one', 'two', 'three']",
                default=None,
            ),
            Field(
                key="literal_field",
                type="typing.Literal['lit1', 'lit2', 'lit3']",
                required="True",
                description="A literal string field",
                default=None,
            ),
            Field(
                key="default_factory_int",
                type="int",
                required="False",
                description="A field that uses a default factory (always 5)",
                default="None",
            ),
            Field(
                key="base_model_item",
                type="ContainedModel",
                required="True",
                description="A reference to a different base model",
                default=None,
            ),
            Field(
                key="base_model_dict",
                type="typing.Dict[str, mdantic.samples.ContainedModel]",
                required="True",
                description="A field that maps str names to contained models",
                default=None,
            ),
        ],
        "ContainedModel": [
            Field(
                key="name",
                type="str",
                required="True",
                description="A field internal to the Contained Model",
                default=None,
            )
        ],
    }

    assert structs == expected_structs
