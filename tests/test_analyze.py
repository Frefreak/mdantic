from mdantic import analyze


def test_analyze():
    """Tests the analyze function using sample Base Models"""

    base_model_name = "mdantic.SampleModel"

    structs = analyze(base_model_name)

    assert structs is not None
    assert len(structs) > 0