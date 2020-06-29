import importlib
import re
from collections import namedtuple

import tabulate
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from pydantic import BaseModel


class MarkdownInclude(Extension):
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
        md.preprocessors.add(
            "include", IncludePreprocessor(md, self.getConfigs()), "_begin"
        )


def analyze(model):
    paths = model.split(".")
    module = ".".join(paths[:-1])
    attr = paths[-1]
    mod = importlib.import_module(module)
    if not hasattr(mod, attr):
        return None
    cls = getattr(mod, attr)

    structs = {}
    mk_struct(cls, structs)
    return structs


Field = namedtuple("Field", "key type required desc default")


def mk_struct(cls, structs):
    this_struct = []
    structs[cls.__name__] = this_struct
    for _, f in cls.__fields__.items():
        ty = f.type_.__name__ if hasattr(f.type_, '__name__') else str(f.type_)
        this_struct.append(
            Field(
                f.alias,
                ty,
                str(f.required),
                str(f.field_info.description),
                str(f.default),
            )
        )
        if hasattr(f.type_, '__mro__'):
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


class IncludePreprocessor(Preprocessor):
    """
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    """

    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.init_code = config["init_code"]
        if self.init_code:
            exec(self.init_code)

    def run(self, lines):
        for i, l in enumerate(lines):
            g = re.match("^\$pydantic: (.*)$", l)
            if g:
                cls_name = g.group(1)
                structs = analyze(cls_name)
                if structs is None:
                    print(
                        f"warning: mdantic pattern detected but failed to import module: {cls_name}"
                    )
                    continue
                tabs = fmt_tab(structs)
                table_str = ''
                for cls, tab in tabs.items():
                    table_str += '\n' + f'**{cls}**' + '\n\n' + str(tab) + '\n'
                lines = lines[:i] + [table_str] + lines[i+1:]

        return lines


def makeExtension(*args, **kwargs):
    return MarkdownInclude(kwargs)
