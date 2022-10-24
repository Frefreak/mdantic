import re
import inspect
import importlib
from enum import Enum
from collections import namedtuple

import tabulate
from pydantic import BaseModel
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class Mdantic(Extension):
    def __init__(self, configs=None):
        if configs is None:
            configs = {}
        self.config = {
            "init_code": ["", "python code to run when initializing"],
        }
        for key, value in configs.items():
            self.setConfig(key, value)
        super().__init__()

    def extendMarkdown(self, md):
        md.preprocessors.register(
            MdanticPreprocessor(md, self.getConfigs()), "mdantic", 100
        )


def analyze(model):
    paths = model.rsplit(".", 1)
    if len(paths) != 2:
        return None
    module = paths[0]
    attr = paths[1]
    try:
        mod = importlib.import_module(module)
    except ModuleNotFoundError:
        return None
    if not hasattr(mod, attr):
        return None
    cls = getattr(mod, attr)

    structs = {}
    mk_struct(cls, structs)
    return structs


Field = namedtuple("Field", "key type required desc default")


def get_related_enum(ty):
    visited = set()
    result = []
    get_related_enum_helper(ty, visited, result)
    return result


def get_enum_values(e):
    return [x.value for x in list(e)]


def get_related_enum_helper(ty, visited, result):
    visited.add(ty)
    if inspect.isclass(ty) and issubclass(ty, Enum) and ty not in result:
        result.append(ty)
    if hasattr(ty, "__args__"):
        for sub_ty in getattr(ty, "__args__"):
            if sub_ty not in visited:
                get_related_enum_helper(sub_ty, visited, result)


def mk_struct(cls, structs):
    this_struct = []
    structs[cls.__name__] = this_struct
    for _, f in cls.__fields__.items():
        ty = f.type_
        description = f.field_info.description or ""
        related_enums = get_related_enum(ty)
        if related_enums:
            for e in related_enums:
                description += f"\n{e.__name__}: {get_enum_values(e)}"
        default = str(f.default if f.default is not None else "")
        if hasattr(f, "_type_display"):
            ty = f._type_display()
        elif hasattr(ty, "__name__"):
            ty = ty.__name__
        else:
            ty = str(ty)
        this_struct.append(
            Field(
                f.alias,
                ty,
                str(f.required),
                description,
                default,
            )
        )
        if hasattr(f.type_, "__mro__"):
            if BaseModel in f.type_.__mro__:
                mk_struct(f.type_, structs)


def fmt_tab(structs):
    tabs = {}
    field_names = ["key", "type", "required", "description", "default"]
    for cls, struct in structs.items():
        tab = []
        for f in struct:
            tab.append(list(f))
        tabs[cls] = tabulate.tabulate(tab, headers=field_names, tablefmt="github")
    return tabs


class MdanticPreprocessor(Preprocessor):
    """
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    """

    def __init__(self, md, config):
        super(MdanticPreprocessor, self).__init__(md)
        self.init_code = config["init_code"]
        if self.init_code:
            exec(self.init_code)

    def run(self, lines):
        for i, l in enumerate(lines):
            g = re.match(r"^\$pydantic: (.*)$", l)
            if g:
                cls_name = g.group(1)
                structs = analyze(cls_name)
                if structs is None:
                    print(
                        f"warning: mdantic pattern detected but failed to process or import: {cls_name}"
                    )
                    continue
                tabs = fmt_tab(structs)
                table_str = ""
                for cls, tab in tabs.items():
                    table_str += "\n" + f"**{cls}**" + "\n\n" + str(tab) + "\n"
                lines = lines[:i] + [table_str] + lines[i + 1 :]

        return lines


def makeExtension(*_, **kwargs):
    return Mdantic(kwargs)
