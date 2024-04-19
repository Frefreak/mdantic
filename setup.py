from setuptools import setup

setup(
    name="markdown-mdantic",
    version="2.1.1",
    author="Xiangyu Zhu",
    author_email="frefreak.zxy@gmail.com",
    description="Python-Markdown extension for rendering pydantic BaseModel as table",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/frefreak/mdantic",
    packages=["mdantic"],
    install_requires=["markdown >= 3.0", "tabulate", "pydantic >= 2.0"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup :: HTML",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
