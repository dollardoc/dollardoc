from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dollardoc",
    version="0.2.0",
    description="Object oriented markdown documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="dollardoc",
    author_email="development@dollardoc.dev",
    url="https://github.com/dollardoc/dollardoc",
    packages=[
        "dollar",
        "dollar.builder",
        "dollar.cli",
        "dollar.file",
        "dollar.format",
        "dollar.format.header",
        "dollar.format.input",
        "dollar.format.output",
        "dollar.format.raw",
        "dollar.format.transformer",
        "dollar.helper",
        "dollar.plugin",
        "dollar.plugin.builtin",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Documentation",
        "Topic :: Education",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Editors :: Word Processors",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Utilities",
    ],
    keywords=[
        "documentation",
        "object-oriented",
        "objectoriented",
        "object oriented",
        "markdown",
        "processing",
        "organize",
        "version",
    ],
    install_requires=[
        "PyYAML"
    ],
    entry_points={
        "console_scripts": [
            "dollardoc=dollar.cli.cli:cli"
        ]
    },
)