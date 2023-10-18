from mdantic import analyze

base_model_name = "mdantic.SampleModel"

structs = analyze(base_model_name)

assert structs is not None
assert len(structs) > 0

print(structs)