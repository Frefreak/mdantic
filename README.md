# Mdantic

This is an extension to [Python-Markdown](https://python-markdown.github.io/). It adds a new syntax so that you can reference a [pydantic](https://pydantic-docs.helpmanual.io/) `BaseModel` and translate its fields to a markdown table. (Get the name?) I originally make this to generate http api parameter tables with [mkdocs](https://www.mkdocs.org/), but you can use it for other stuffs if suitable.

The code itself is a direct modification to [markdown-include](https://github.com/cmacmackin/markdown-include) since they do similar things.

Notice: This project is still WIP and need more examples to adapt to most of the possible BaseModel models.

## Installation

Just use pip:

```
pip install markdown-mdantic
```

## Usage

### Config options
`init_code` will execute **any** python code in the environment when its `__init__` is called.
In this way you can do something like adding system path, django setup etc,
before run.

**Note**: Please note that the `init_code` thing is a huge security issue if
you run that with untrusted input. Use it with caution!

`columns` is a comma-separated list of table columns to use in each table.
The default is to use all columns `["key", "type", "required", "description", "default"]`.


### mkdocs

example:

```yaml
markdown_extensions:
    mdantic:
        init_code: |
            import os
            import django
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.default")
            django.setup()
    columns: [key, type, required, default]
```

Some time ago the extension name used here should be `markdown_mdantic`, but
after some point it seems there will only be one file after installation in
python's site-packages directory (mdantic.py) so now we should use the name
`mdantic`.

### reference the model

Each reference must be in one line, starts with `$pydantic: ` (notice the
single space after the colon), following the model import path which looks
lik `a.b.c.D` where `D` is the model class itself (which is subclass of `BaseModel`).

```markdown
**params**:

$pydantic: src.test.TestGetSchema

```

### customize output

The resulting table is rendered using [tabulate](https://pypi.org/project/tabulate/), in `github` style. The `columns` config option can be used to
restrict the columns to show. Styling cannot be changed at the moment. PR is welcomed.
