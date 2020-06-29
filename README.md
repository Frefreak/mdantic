# Mdantic

This is an extension to [Python-Markdown](https://python-markdown.github.io/). It adds a new syntax so that you can reference a [pydantic](https://pydantic-docs.helpmanual.io/) `BaseModel` and translate its fields to a markdown table. (Get the name?) I originally make this to generate http api parameter tables with [mkdocs](https://www.mkdocs.org/), but you can use it for other stuffs if suitable.

The code itself is a direct modification to [markdown-include](https://github.com/cmacmackin/markdown-include) since they do similar things.

## Installation

Just use pip:

```
pip install markdown-mdantic
```

## Usage

Currently this module has only one config option: `init_code` which will execute **any** python code in the environment when its `__init__` is called. In this way you can do something like adding system path, django setup etc, before run.


### mkdocs

example:

```yaml
markdown_extensions:
    markdown_mdantic:
        init_code: |
            import os
            import django
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.default")
            django.setup()
```

### reference the model

Each reference must be in one line, starts with `$pydantic: ` (notice the single space after the colon), following the model import path which looks lik `a.b.c.D` where `D` is the model class itself (BaseModel).

```markdown
**params**:

$pydantic: src.test.TestGetSchema

```

### customize output

The resulting table is rendered using [tabulate](https://pypi.org/project/tabulate/), in `github` style. Currently there is no config option to change this and the table headers. PR is welcomed.
