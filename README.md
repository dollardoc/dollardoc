# DollarDoc

Dollardoc is a unique documentation method that uses Markdown and a pseudo object-oriented model to simplify documentation in complex environments. By utilizing dollar-plugins, dollardoc provides a feature-rich documentation method, while still being lightweight and straightforward.

## Getting Started

### Installation

To begin using dollardoc, first install Python 3.9 or above: [https://www.python.org/downloads/](https://www.python.org/downloads/).

Then you can install dollardoc with pip in a terminal

``` bash
$ pip install dollardoc
```

After that you will need two files, one python file, which starts a build. And one configuration file, which tells dollardoc about the documentation environment.

`build.py`

``` python
from dollar.builder.dollarbuilder import DollarBuilder


def main():
    DollarBuilder.build()


if __name__ == '__main__':
    main()

```

`dollarconfig.yaml`

``` yaml
docs_path: docs
target_path: output
plugin_path: plugin
file_passthrough:
  - .md
  - .txt
```

Now you just need to create two folders in your project, `docs/` and `plugin/` and you are ready to start writing dollar-style documentation.

#### Quicker Alternative

You can also use the [dollar-project-boilerplate](https://github.com/dollardoc/dollardoc-project-boilerplate) project, which will provide you with a quick start.

### Folder Structure

This is the recommended folder structure to simply organize your dollardoc project.

``` text
dollardoc_test_project
├── docs
│   └── ... Dollardoc and Markdown files
├── plugin
│   ├── block
│   │   └── ... Block plugin python files
│   ├── extension
│   │   └── ... Extension plugin python files
│   └── function
│       └── ... Function plugin python files
├── build.py
└── dollarconfig.yaml
```

### Creating Your First Documentation File

Dollar-files end with `.mdd` to differentiate them from normal markdown files. All dollar-files start with a header-section. The syntax of the header-section is in yaml and contains variables that can be used by this document and other documents. Although other documents' use of these variables is limited to their respective content-section, the header can only refer to variables in it's own context and other dollar-files (by refering to their id).

The content part is plain markdown, with the addition of dollar-references, dollar-functions and dollar-blocks.

#### Example Input

``` markdown
---
id: id-is-required
type: page

title: Some Title
description: Some description of the page

some-variable: Example text in $this.id
some-list:
  - First item
  - $another-page-id
---

# $this.title

$this.description

Variable some-variable from this has the value: $this.some-variable

Variable title from another-page-id has the value: $another-page-id.title

You can also create simple inline links to another object like $another-page-id by just writing a reference to the id.

## Dollar Function Example

$$List($this.some-list)

## Dollar Block Example

Currently there are no standard library dollar blocks to show as an example, this is *under construction*.

```

#### Example Output

``` markdown

# Some Title

Some description of the page

Variable some-variable from this has the value: Example text in id-is-required

Variable title from another-page-id has the value: Another Page Title

You can also create simple inline links to another object like [Another Page Title](./another-page-id.md) by just writing a reference to the id.

## Dollar Function Example

* First item
* [Another Page Title](./another-page-id.md)

## Dollar Block Example

Currently there are no standard library dollar blocks to show as an example, this is *under construction*.

```

### Building the Documentation

``` bash
$ python build.py
```

Unless there is an exception, all your generated markdown files will show up in the `output/` folder.

## Dollar Syntax Specification Document

[dollar-syntax-specification-v0_1_0.pdf](https://github.com/dollardoc/dollar-syntax-specification/releases/download/v0.1.0/dollar-syntax-specification-v0_1_0.pdf)

## Outputs Supported

This project only supports plain markdown files. Other alternatives has been considered, like docusaurus style markdown output, but nothing has been decided at this moment.

## Future of the Project

* **Syntax specification**
  * An outline of the syntax specification is currently in progress.

* **Support for tags**
  * Add the ability to create indirect links between different pages using tags. This simplifies the process of linking related documentation pages without requiring the creation of entire new pages.
