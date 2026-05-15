Package Reference — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](#)
    *   [`minify()`](#python_minifier.minify)
    *   [`RemoveAnnotationsOptions`](#python_minifier.RemoveAnnotationsOptions)
    *   [`awslambda()`](#python_minifier.awslambda)
    *   [`unparse()`](#python_minifier.unparse)
    *   [`UnstableMinification`](#python_minifier.UnstableMinification)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   Package Reference
*   [View page source](https://dflook.github.io/python-minifier/_sources/api_usage.rst.txt)

* * *

# Package Reference[](#module-python_minifier "Link to this heading")

This package transforms python source code strings or ast.Module Nodes into a ‘minified’ representation of the same source code.

 python\_minifier.minify(_source_, _filename\=None_, _remove\_annotations\=RemoveAnnotationsOptions(remove\_variable\_annotations=True, remove\_return\_annotations=True, remove\_argument\_annotations=True, remove\_class\_attribute\_annotations=False)_, _remove\_pass\=True_, _remove\_literal\_statements\=False_, _combine\_imports\=True_, _hoist\_literals\=True_, _rename\_locals\=True_, _preserve\_locals\=None_, _rename\_globals\=False_, _preserve\_globals\=None_, _remove\_object\_base\=True_, _convert\_posargs\_to\_args\=True_, _preserve\_shebang\=True_, _remove\_asserts\=False_, _remove\_debug\=False_, _remove\_explicit\_return\_none\=True_, _remove\_builtin\_exception\_brackets\=True_, _constant\_folding\=True_)[](#python_minifier.minify "Link to this definition")

Minify a python module

The module is transformed according the the arguments. If all transformation arguments are False, no transformations are made to the AST, the returned string will parse into exactly the same module.

Using the default arguments only transformations that are always or almost always safe are enabled.

 Parameters:

*   **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")) – The python module source code
    
*   **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")) – The original source filename if known
    
*   **remove\_annotations** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)") _or_ [_RemoveAnnotationsOptions_](#python_minifier.RemoveAnnotationsOptions "python_minifier.RemoveAnnotationsOptions")) – Configures the removal of type annotations. True removes all annotations, False removes none. RemoveAnnotationsOptions can be used to configure the removal of specific annotations.
    
*   **remove\_pass** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If Pass statements should be removed where possible
    
*   **remove\_literal\_statements** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If statements consisting of a single literal should be removed, including docstrings
    
*   **combine\_imports** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Combine adjacent import statements where possible
    
*   **hoist\_literals** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If str and byte literals may be hoisted to the module level where possible.
    
*   **rename\_locals** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If local names may be shortened
    
*   **preserve\_locals** ([_list_](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.13)")_\[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")_\]_) – Locals names to leave unchanged when rename\_locals is True
    
*   **rename\_globals** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If global names may be shortened
    
*   **preserve\_globals** ([_list_](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.13)")_\[_[_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")_\]_) – Global names to leave unchanged when rename\_globals is True
    
*   **remove\_object\_base** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If object as a base class may be removed
    
*   **convert\_posargs\_to\_args** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If positional-only arguments will be converted to normal arguments
    
*   **preserve\_shebang** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Keep any shebang interpreter directive from the source in the minified output
    
*   **remove\_asserts** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If assert statements should be removed
    
*   **remove\_debug** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If conditional statements that test ‘\_\_debug\_\_ is True’ should be removed
    
*   **remove\_explicit\_return\_none** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If explicit return None statements should be replaced with a bare return
    
*   **remove\_builtin\_exception\_brackets** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If brackets should be removed when raising exceptions with no arguments
    
*   **constant\_folding** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – If literal expressions should be evaluated
    

 Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")

  _class_ python\_minifier.RemoveAnnotationsOptions(_remove\_variable\_annotations\=True_, _remove\_return\_annotations\=True_, _remove\_argument\_annotations\=True_, _remove\_class\_attribute\_annotations\=False_)[](#python_minifier.RemoveAnnotationsOptions "Link to this definition")

Options for the RemoveAnnotations transform

This can be passed to the minify function as the remove\_annotations argument

 Parameters:

*   **remove\_variable\_annotations** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Remove variable annotations
    
*   **remove\_return\_annotations** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Remove return annotations
    
*   **remove\_argument\_annotations** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Remove argument annotations
    
*   **remove\_class\_attribute\_annotations** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")) – Remove class attribute annotations
    

  python\_minifier.awslambda(_source_, _filename\=None_, _entrypoint\=None_)[](#python_minifier.awslambda "Link to this definition")

Minify a python module for use as an AWS Lambda function

This returns a string suitable for embedding in a cloudformation template. When minifying, all transformations are enabled.

 Parameters:

*   **source** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")) – The python module source code
    
*   **filename** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")) – The original source filename if known
    
*   **entrypoint** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") _or_ _NoneType_) – The lambda entrypoint function
    

 Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")

  python\_minifier.unparse(_module_)[](#python_minifier.unparse "Link to this definition")

Turn a module AST into python code

This returns an exact representation of the given module, such that it can be parsed back into the same AST.

 Parameters:

**module** – The module to turn into python code

 Type:

module: [`ast.Module`](https://docs.python.org/3/library/ast.html#ast.Module "(in Python v3.13)")

 Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")

  _class_ python\_minifier.UnstableMinification(_exception_, _source_, _minified_)[](#python_minifier.UnstableMinification "Link to this definition")

Raised when a minified module differs from the original module in an unexpected way.

This is raised when the minifier generates source code that doesn’t parse back into the original module (after known transformations). This should never occur and is a bug.

 [Previous](https://dflook.github.io/python-minifier/command_usage.html "Command Usage")[Next](https://dflook.github.io/python-minifier/transforms/index.html "Minification Options") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Command Usage — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](#)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   Command Usage
*   [View page source](https://dflook.github.io/python-minifier/_sources/command_usage.rst.txt)

* * *

# Command Usage[](#command-usage "Link to this heading")

The pyminify command is installed with this package. It can be used to minify python files, and outputs the result to stdout.

usage: pyminify [-h] [--output OUTPUT | --in-place] [--no-combine-imports]
                [--no-remove-pass] [--remove-literal-statements]
                [--no-hoist-literals] [--no-rename-locals]
                [--preserve-locals LOCAL_NAMES] [--rename-globals]
                [--preserve-globals GLOBAL_NAMES] [--no-remove-object-base]
                [--no-convert-posargs-to-args] [--no-preserve-shebang]
                [--remove-asserts] [--remove-debug]
                [--no-remove-explicit-return-none]
                [--no-remove-builtin-exception-brackets]
                [--no-constant-folding] [--no-remove-annotations]
                [--no-remove-variable-annotations]
                [--no-remove-return-annotations]
                [--no-remove-argument-annotations]
                [--remove-class-attribute-annotations] [--version]
                path [path ...]

Minify Python source code

positional arguments:
  path                  The source file or directory to minify. Use "-" to
                        read from stdin. Directories are recursively searched
                        for ".py" files to minify. May be used multiple times

options:
  -h, --help            show this help message and exit
  --output, -o OUTPUT   Path to write minified output. Can only be used when
                        the source is a single module. Outputs to stdout by
                        default
  --in-place, -i        Overwrite existing files. Required when there is more
                        than one source module
  --version, -v         show program's version number and exit

minification options:
  Options that affect how the source is minified

  --no-combine-imports  Disable combining adjacent import statements
  --no-remove-pass      Disable removing Pass statements
  --remove-literal-statements
                        Enable removing statements that are just a literal
                        (including docstrings)
  --no-hoist-literals   Disable replacing string and bytes literals with
                        variables
  --no-rename-locals    Disable shortening of local names
  --preserve-locals LOCAL_NAMES
                        Comma separated list of local names that will not be
                        shortened
  --rename-globals      Enable shortening of global names
  --preserve-globals GLOBAL_NAMES
                        Comma separated list of global names that will not be
                        shortened
  --no-remove-object-base
                        Disable removing object from base class list
  --no-convert-posargs-to-args
                        Disable converting positional only arguments to normal
                        arguments
  --no-preserve-shebang
                        Disable preserving any shebang line from the source
  --remove-asserts      Enable removing assert statements
  --remove-debug        Enable removing conditional statements that test
                        __debug__ is True
  --no-remove-explicit-return-none
                        Disable replacing explicit return None with a bare
                        return
  --no-remove-builtin-exception-brackets
                        Disable removing brackets when raising builtin
                        exceptions with no arguments
  --no-constant-folding
                        Disable evaluating literal expressions

remove annotations options:
  Options that affect how annotations are removed

  --no-remove-annotations
                        Disable removing all annotations
  --no-remove-variable-annotations
                        Disable removing variable annotations
  --no-remove-return-annotations
                        Disable removing function return annotations
  --no-remove-argument-annotations
                        Disable removing function argument annotations
  --remove-class-attribute-annotations
                        Enable removing class attribute annotations

examples:
  # Minifying stdin to stdout
  pyminify -

  # Minifying a file to stdout
  pyminify example.py

  # Minifying a file and writing to a different file
  pyminify example.py --output example.min.py

  # Minifying a file in place
  pyminify example.py --in-place

  # Minifying all *.py files in a directory
  pyminify src/ --in-place

  # Minifying multiple paths in place
  pyminify file1.py file2.py src/ --in-place

 [Previous](https://dflook.github.io/python-minifier/installation.html "Installation")[Next](https://dflook.github.io/python-minifier/api_usage.html "Package Reference") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Installation — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](#)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   Installation
*   [View page source](https://dflook.github.io/python-minifier/_sources/installation.rst.txt)

* * *

# Installation[](#installation "Link to this heading")

To install python-minifier use pip:

$ pip install python-minifier

Note that python-minifier depends on the python interpreter for parsing source code, and outputs source code compatible with the version of the interpreter it is run with.

This means that if you minify code written for Python 3.6 using python-minifier running with Python 3.12, the minified code may only run with Python 3.12.

python-minifier runs with and can minify code written for Python 2.7 and Python 3.3 to 3.13.

 [Previous](https://dflook.github.io/python-minifier/index.html "Welcome to Python-Minifier’s documentation!")[Next](https://dflook.github.io/python-minifier/command_usage.html "Command Usage") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Combine Imports — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Combine Imports
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/combine_imports.rst.txt)

* * *

# Combine Imports[](#combine-imports "Link to this heading")

This transform combines adjacent import statements into a single statement. The order of the imports will not be changed. This transform is always safe to use and enabled by default.

Disable this source transformation by passing the `combine_imports=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-combine-imports` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

import requests
import collections
from typing import Dict
from typing import List, Optional
import sys
import os

### Output[](#output "Link to this heading")

import requests,collections
from typing import Dict,List,Optional
import sys,os

 [Previous](https://dflook.github.io/python-minifier/transforms/index.html "Minification Options")[Next](https://dflook.github.io/python-minifier/transforms/remove_pass.html "Remove Pass") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Constant Folding — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Constant Folding
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/constant_folding.rst.txt)

* * *

# Constant Folding[](#constant-folding "Link to this heading")

This transform evaluates constant expressions with literal operands when minifying and replaces the expression with the resulting value, if the value is shorter than the expression.

There are some limitations, notably the division and power operators are not evaluated.

This will be most effective with numeric literals.

This transform is always safe and enabled by default. Disable by passing the `constant_folding=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-constant-folding` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

SECONDS_IN_A_DAY = 60 * 60 * 24
SECONDS_IN_A_WEEK = SECONDS_IN_A_DAY * 7

### Output[](#output "Link to this heading")

SECONDS_IN_A_DAY=86400
SECONDS_IN_A_WEEK=SECONDS_IN_A_DAY*7

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html "Remove Builtin Exception Brackets")[Next](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html "Remove Literal Statements") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Convert Positional-Only Arguments to Arguments — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Convert Positional-Only Arguments to Arguments
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/convert_posargs_to_args.rst.txt)

* * *

# Convert Positional-Only Arguments to Arguments[](#convert-positional-only-arguments-to-arguments "Link to this heading")

This transform converts positional-only arguments into normal arguments by removing the ‘/’ separator in the argument list.

This transform is almost always safe to use and enabled by default.

Disable this source transformation by passing the `convert_posargs_to_args=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-convert-posargs-to-args` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

def name(p1, p2, /, p_or_kw, *, kw): pass
def name(p1, p2=None, /, p_or_kw=None, *, kw): pass
def name(p1, p2=None, /, *, kw): pass
def name(p1, p2=None, /): pass
def name(p1, p2, /, p_or_kw): pass
def name(p1, p2, /): pass

### Output[](#output "Link to this heading")

def name(p1,p2,p_or_kw,*,kw):pass
def name(p1,p2=None,p_or_kw=None,*,kw):pass
def name(p1,p2=None,*,kw):pass
def name(p1,p2=None):pass
def name(p1,p2,p_or_kw):pass
def name(p1,p2):pass

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_object_base.html "Remove Object Base")[Next](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html "Preserve Shebang") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Hoist Literals — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Hoist Literals
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/hoist_literals.rst.txt)

* * *

# Hoist Literals[](#hoist-literals "Link to this heading")

This transform replaces string and bytes literals with references to variables. It may also introduce new names for some builtin constants (True, False, None). This will only be done if multiple literals can be replaced with a single variable referenced in multiple locations (and the resulting code is smaller).

If the rename\_globals transform is disabled, the newly introduced global names have an underscore prefix.

This transform is always safe to use and enabled by default. Disable this source transformation by passing the `hoist_literals=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-hoist-literals` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

def validate(arn, props):
    if 'ValidationMethod' in props and props['ValidationMethod'] == 'DNS':

        all_records_created = False
        while not all_records_created:
            all_records_created = True

            certificate = acm.describe_certificate(CertificateArn=arn)['Certificate']

            if certificate['Status'] != 'PENDING_VALIDATION':
                return

            for v in certificate['DomainValidationOptions']:

                if 'ValidationStatus' not in v or 'ResourceRecord' not in v:
                    all_records_created = False
                    continue

                records = []
                if v['ValidationStatus'] == 'PENDING_VALIDATION':
                    records.append({
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': v['ResourceRecord']['Name'],
                            'Type': v['ResourceRecord']['Type'],
                            'TTL': 60,
                            'ResourceRecords': [{
                                'Value': v['ResourceRecord']['Value']
                            }]
                        }
                    })

                if records:
                    response = boto3.client('route53').change_resource_record_sets(
                        HostedZoneId=get_zone_for(v['DomainName'], props),
                        ChangeBatch={
                            'Comment': 'Domain validation for %s' % arn,
                            'Changes': records
                        }
                    )

### Output[](#output "Link to this heading")

def validate(arn,props):
	H='Value';G='Type';F='Name';E='ValidationStatus';D='PENDING_VALIDATION';C=False;B='ValidationMethod';A='ResourceRecord'
	if B in props and props[B]=='DNS':
		all_records_created=C
		while not all_records_created:
			all_records_created=True;certificate=acm.describe_certificate(CertificateArn=arn)['Certificate']
			if certificate['Status']!=D:return
			for v in certificate['DomainValidationOptions']:
				if E not in v or A not in v:all_records_created=C;continue
				records=[]
				if v[E]==D:records.append({'Action':'UPSERT','ResourceRecordSet':{F:v[A][F],G:v[A][G],'TTL':60,'ResourceRecords':[{H:v[A][H]}]}})
				if records:response=boto3.client('route53').change_resource_record_sets(HostedZoneId=get_zone_for(v['DomainName'],props),ChangeBatch={'Comment':'Domain validation for %s'%arn,'Changes':records})

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_pass.html "Remove Pass")[Next](https://dflook.github.io/python-minifier/transforms/remove_annotations.html "Remove Annotations") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Minification Options — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](#)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   Minification Options
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/index.rst.txt)

* * *

# Minification Options[](#minification-options "Link to this heading")

These transforms can be optionally enabled when minifying. Some are enabled by default as they are always or almost always safe.

They can be enabled or disabled through the minify function, or passing options to the pyminify command.

Enabled by default

*   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
*   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
*   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
*   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
*   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
*   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
*   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
*   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
*   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
*   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
*   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)

Disabled by default

*   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
*   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
*   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
*   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

 [Previous](https://dflook.github.io/python-minifier/api_usage.html "Package Reference")[Next](https://dflook.github.io/python-minifier/transforms/combine_imports.html "Combine Imports") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Preserve Shebang — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Preserve Shebang
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/preserve_shebang.rst.txt)

* * *

# Preserve Shebang[](#preserve-shebang "Link to this heading")

The shebang line indicates what interpreter should be used by the operating system when loading a python file as an executable. It does not have any meaning to python itself, but may be needed if python files should be directly executable.

When this option is enabled, any shebang line is preserved in the minified output. The option is enabled by default.

Disable this option by passing `preserve_shebang=False` to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-preserve-shebang` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

#!/usr/bin/python

import sys
print(sys.executable)

### Output[](#output "Link to this heading")

#!/usr/bin/python
import sys
print(sys.executable)

 [Previous](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html "Convert Positional-Only Arguments to Arguments")[Next](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html "Remove Explicit Return None") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Annotations — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](#)
        *   [Options](#options)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Annotations
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_annotations.rst.txt)

* * *

# Remove Annotations[](#remove-annotations "Link to this heading")

This transform removes annotations. Although the annotations have no meaning to the python language, they are made available at runtime. Some python library features require annotations to be kept.

Annotations can be removed from:

> *   Function arguments
>     
> *   Function return
>     
> *   Variables
>     
> *   Class attributes

By default annotations are removed from variables, function arguments and function return, but not from class attributes.

This transform is generally safe to use with the default options. If you know the module requires the annotations to be kept, disable this transform. Class attribute annotations can often be used by other modules, so it is recommended to keep them unless you know they are not used.

When removing class attribute annotations is enabled, annotations are kept for classes that are derived from:

> *   dataclasses.dataclass
>     
> *   typing.NamedTuple
>     
> *   typing.TypedDict

If a variable annotation without assignment is used the annotation is changed to a literal zero instead of being removed.

## Options[](#options "Link to this heading")

These arguments can be used with the pyminify command:

`--no-remove-variable-annotations` disables removing variable annotations

`--no-remove-return-annotations` disables removing function return annotations

`--no-remove-argument-annotations` disables removing function argument annotations

`--remove-class-attribute-annotations` enables removing class attribute annotations

`--no-remove-annotations` disables removing all annotations, this transform will not do anything.

When using the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function you can use the `remove_annotations` argument to control this transform. You can pass a boolean `True` to remove all annotations or a boolean `False` to keep all annotations. You can also pass a [`python_minifier.RemoveAnnotationsOptions`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.RemoveAnnotationsOptions "python_minifier.RemoveAnnotationsOptions") instance to specify which annotations to remove.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

class A:
    b: int
    c: int=2
    def a(self, val: str) -> None:
        b: int
        c: int=2

### Output[](#output "Link to this heading")

class A:
	b:0;c=2
	def a(self,val):b:0;c=2

 [Previous](https://dflook.github.io/python-minifier/transforms/hoist_literals.html "Hoist Literals")[Next](https://dflook.github.io/python-minifier/transforms/rename_locals.html "Rename Locals") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Asserts — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Asserts
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_asserts.rst.txt)

* * *

# Remove Asserts[](#remove-asserts "Link to this heading")

This transform removes assert statements.

Assert statements are evaluated by Python when it is not started with the -O option. This transform is only safe to use if the minified output will by run with the -O option, or you are certain that the assert statements are not needed.

If a statement is required, the assert statement will be replaced by a zero expression statement.

The transform is disabled by default. Enable it by passing the `remove_asserts=True` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--remove-asserts` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

word = 'hello'
assert word is 'goodbye'
print(word)

### Output[](#output "Link to this heading")

word='hello'
print(word)

 [Previous](https://dflook.github.io/python-minifier/transforms/rename_globals.html "Rename Globals")[Next](https://dflook.github.io/python-minifier/transforms/remove_debug.html "Remove Debug") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Builtin Exception Brackets — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Builtin Exception Brackets
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_builtin_exception_brackets.rst.txt)

* * *

# Remove Builtin Exception Brackets[](#remove-builtin-exception-brackets "Link to this heading")

This transform removes parentheses when raising builtin exceptions with no arguments.

The raise statement automatically instantiates exceptions with no arguments, so the parentheses are unnecessary. This transform does nothing on Python 2.

If the exception is not a builtin exception, or has arguments, the parentheses are not removed.

This transform is enabled by default. Disable by passing the `remove_builtin_exception_brackets=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-remove-builtin-exception-brackets` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

class MyBaseClass:
    def override_me(self):
        raise NotImplementedError()

### Output[](#output "Link to this heading")

class MyBaseClass:
	def override_me(self):raise NotImplementedError

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html "Remove Explicit Return None")[Next](https://dflook.github.io/python-minifier/transforms/constant_folding.html "Constant Folding") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Debug — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Debug
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_debug.rst.txt)

* * *

# Remove Debug[](#remove-debug "Link to this heading")

This transform removes `if` statements that test `__debug__` is `True`.

The builtin `__debug__` constant is True if Python is not started with the `-O` option. This transform is only safe to use if the minified output will by run with the `-O` option, or you are certain that any `if` statement that tests `__debug__` can be removed.

The condition is not evaluated. The statement is only removed if the condition exactly matches one of the forms in the example below.

If a statement is required, the `if` statement will be replaced by a zero expression statement.

The transform is disabled by default. Enable it by passing the `remove_debug=True` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--remove-debug` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

value = 10

# Truthy
if __debug__:
    value += 1

if __debug__ is True:
    value += 1

if __debug__ is not False:
    value += 1

if __debug__ == True:
    value += 1

# Falsy
if not __debug__:
    value += 1

if __debug__ is False:
    value += 1

if __debug__ is not True:
    value += 1

if __debug__ == False:
    value += 1

print(value)

### Output[](#output "Link to this heading")

value=10
if not __debug__:value+=1
if __debug__ is False:value+=1
if __debug__ is not True:value+=1
if __debug__==False:value+=1
print(value)

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_asserts.html "Remove Asserts")

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Explicit Return None — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Explicit Return None
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_explicit_return_none.rst.txt)

* * *

# Remove Explicit Return None[](#remove-explicit-return-none "Link to this heading")

This transforms any `return None` statement into a `return` statement, as return statement with no value is equivalent to `return None`. Also removes any `return None` or `return` statements that are the last statement in a function.

The transform is always safe to use and enabled by default. Disable by passing the `remove_explicit_return_none=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-remove-explicit-remove-none` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

def important(a):
    if a > 3:
        return a
    if a < 2:
        return None
    a.adjust(1)
    return None

### Output[](#output "Link to this heading")

def important(a):
	if a>3:return a
	if a<2:return
	a.adjust(1)

 [Previous](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html "Preserve Shebang")[Next](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html "Remove Builtin Exception Brackets") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Literal Statements — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Literal Statements
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_literal_statements.rst.txt)

* * *

# Remove Literal Statements[](#remove-literal-statements "Link to this heading")

This transform removes statements that consist entirely of a literal value. This includes docstrings. If a statement is required, it is replaced by a literal zero expression statement.

This transform will strip docstrings from the source. If the module uses the `__doc__` name the module docstring will be retained.

This transform is disabled by default. Enable by passing the `remove_literal_statements=True` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--remove-literal-statements` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

"""This is my module docstring"""

'This is another string that has no runtime effect'
b'Bytes literal'
0
1000

def test():
    'Function docstring'

### Output[](#output "Link to this heading")

def test():0

 [Previous](https://dflook.github.io/python-minifier/transforms/constant_folding.html "Constant Folding")[Next](https://dflook.github.io/python-minifier/transforms/rename_globals.html "Rename Globals") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Object Base — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Object Base
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_object_base.rst.txt)

* * *

# Remove Object Base[](#remove-object-base "Link to this heading")

In Python 3 all classes implicitly inherit from `object`. This transform removes `object` from the base class list of all classes. This transform does nothing on Python 2.

This transform is always safe to use and enabled by default.

Disable this source transformation by passing the `remove_object_base=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-remove-object-base` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

class MyClass(object):
    pass

### Output[](#output "Link to this heading")

class MyClass:pass

 [Previous](https://dflook.github.io/python-minifier/transforms/rename_locals.html "Rename Locals")[Next](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html "Convert Positional-Only Arguments to Arguments") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Remove Pass — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Remove Pass
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/remove_pass.rst.txt)

* * *

# Remove Pass[](#remove-pass "Link to this heading")

This transform removes pass statements. If a statement is required, it is replaced by a literal zero expression statement.

This transform is always safe to use and enabled by default.

Disable this source transformation by passing the `remove_pass=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function, or passing `--no-remove-pass` to the pyminify command.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

pass
def test():
    pass
    pass
pass

### Output[](#output "Link to this heading")

def test():0

 [Previous](https://dflook.github.io/python-minifier/transforms/combine_imports.html "Combine Imports")[Next](https://dflook.github.io/python-minifier/transforms/hoist_literals.html "Hoist Literals") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Rename Globals — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](https://dflook.github.io/python-minifier/transforms/rename_locals.html)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Rename Globals
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/rename_globals.rst.txt)

* * *

# Rename Globals[](#rename-globals "Link to this heading")

This transform shortens names in the module scope. This includes introducing short names for builtins.

This could break any program that imports the minified module. For this reason the transform is disabled by default.

When enabled, all global names may be renamed if it is space efficient. This includes:

> *   Global variables
>     
> *   Global import aliases
>     
> *   Global function names
>     
> *   Global class names
>     
> *   Builtin names may be bound to a new name in the module scope

Renaming is prevented by:

> *   If `eval()`, `exec()`, `locals()`, `globals()`, `vars()` are used, renaming is disabled
>     
> *   If `from <module> import *` is used in the module, renaming is disabled
>     
> *   If a name is included as a literal string in `__all__`, renaming of that name is disabled
>     
> *   Any name listed in the `preserve_globals` argument

Enable this source transformation by passing the `rename_globals=True` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function. The `preserve_globals` argument is a list of names to disable renaming for.

When using the pyminify command enable this transformation with `--rename-globals`. The `--preserve_globals` option may be a comma separated list of names to prevent renaming.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

import collections

my_counter = collections.Counter([True, True, True, False, False])

print('Contents:')
print(list(my_counter))

### Output[](#output "Link to this heading")

A=print
import collections as B
C=B.Counter([True,True,True,False,False])
A('Contents:')
A(list(C))

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html "Remove Literal Statements")[Next](https://dflook.github.io/python-minifier/transforms/remove_asserts.html "Remove Asserts") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).Rename Locals — Python Minifier 2.11.3 documentation

 [Python Minifier](https://dflook.github.io/python-minifier/index.html)

    

Contents:

*   [Installation](https://dflook.github.io/python-minifier/installation.html)
*   [Command Usage](https://dflook.github.io/python-minifier/command_usage.html)
*   [Package Reference](https://dflook.github.io/python-minifier/api_usage.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
    *   [Combine Imports](https://dflook.github.io/python-minifier/transforms/combine_imports.html)
    *   [Remove Pass](https://dflook.github.io/python-minifier/transforms/remove_pass.html)
    *   [Hoist Literals](https://dflook.github.io/python-minifier/transforms/hoist_literals.html)
    *   [Remove Annotations](https://dflook.github.io/python-minifier/transforms/remove_annotations.html)
    *   [Rename Locals](#)
        *   [Example](#example)
            *   [Input](#input)
            *   [Output](#output)
    *   [Remove Object Base](https://dflook.github.io/python-minifier/transforms/remove_object_base.html)
    *   [Convert Positional-Only Arguments to Arguments](https://dflook.github.io/python-minifier/transforms/convert_posargs_to_args.html)
    *   [Preserve Shebang](https://dflook.github.io/python-minifier/transforms/preserve_shebang.html)
    *   [Remove Explicit Return None](https://dflook.github.io/python-minifier/transforms/remove_explicit_return_none.html)
    *   [Remove Builtin Exception Brackets](https://dflook.github.io/python-minifier/transforms/remove_builtin_exception_brackets.html)
    *   [Constant Folding](https://dflook.github.io/python-minifier/transforms/constant_folding.html)
    *   [Remove Literal Statements](https://dflook.github.io/python-minifier/transforms/remove_literal_statements.html)
    *   [Rename Globals](https://dflook.github.io/python-minifier/transforms/rename_globals.html)
    *   [Remove Asserts](https://dflook.github.io/python-minifier/transforms/remove_asserts.html)
    *   [Remove Debug](https://dflook.github.io/python-minifier/transforms/remove_debug.html)

[Python Minifier](https://dflook.github.io/python-minifier/index.html)

*   [](https://dflook.github.io/python-minifier/index.html)
*   [Minification Options](https://dflook.github.io/python-minifier/transforms/index.html)
*   Rename Locals
*   [View page source](https://dflook.github.io/python-minifier/_sources/transforms/rename_locals.rst.txt)

* * *

# Rename Locals[](#rename-locals "Link to this heading")

This transform shortens any non-global names.

This transform is almost always safe to use and enabled by default.

When enabled all non-global names may be renamed if it is space efficient and safe to do so. This includes:

> *   Local variables
>     
> *   Functions in function scope
>     
> *   Classes in function scope
>     
> *   Local imports
>     
> *   Comprehension target names
>     
> *   Function arguments that are not typically referenced by the caller (self, cls, args, kwargs)
>     
> *   Positional only function arguments
>     
> *   Possible keyword function arguments may be bound with a new name in the function body, without changing the function signature
>     
> *   Exception handler target names

This will not change:

> *   Global names
>     
> *   Names in class scope
>     
> *   Lambda function arguments (except args/kwargs and positional only args)

New names are assigned according to the smallest minified result. To conserve the pool of available shortest names they are reused in sibling namespaces and shadowed in child namespaces.

Disable this source transformation by passing the `rename_locals=False` argument to the [`python_minifier.minify()`](https://dflook.github.io/python-minifier/api_usage.html#python_minifier.minify "python_minifier.minify") function. The `preserve_locals` argument is a list of names to disable renaming for.

When using the pyminify command disable this transformation with `--no-rename-locals`. The `--preserve_locals` option may be a comma separated list of names to prevent renaming.

Use of some python builtins (`vars()`, `exec()`, `locals()`, `globals()`, `eval()`) in the minified module will disable this transform, as it usually indicates usage of names that this transform can’t recognise.

## Example[](#example "Link to this heading")

### Input[](#input "Link to this heading")

def rename_locals_example(module, another_argument=False, third_argument=None):

    if third_argument is None:
        third_argument = []

    third_argument.extend(module)

    for thing in module.things:
        if another_argument is False or thing.name in third_argument:
            thing.my_method()

### Output[](#output "Link to this heading")

def rename_locals_example(module,another_argument=False,third_argument=None):
	B=module;A=third_argument
	if A is None:A=[]
	A.extend(B)
	for C in B.things:
		if another_argument is False or C.name in A:C.my_method()

 [Previous](https://dflook.github.io/python-minifier/transforms/remove_annotations.html "Remove Annotations")[Next](https://dflook.github.io/python-minifier/transforms/remove_object_base.html "Remove Object Base") 

* * *

© Copyright 2024, Daniel Flook.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).