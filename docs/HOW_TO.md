############################################
IF YOU CLONED THE REPOSITORY SKIP TO STEP 10
############################################

1. Open command prompt

2. Navigate to /PySaar2024/

3. Execute `sphinx-quickstart docs --sep`

4. Change /PySaar2024/docs/source/conf.py to start with

import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix() + "/scripts")

and to include

extensions = [
	'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]

4. Navigate to /PySaar2024/docs/

5. Execute `sphinx-apidoc -o source/generated ../scripts/ -e -M -t source/_templates/apidoc` Add `-f` to overwrite previous versions.

6. Change /PySaar2024/docs/source/index.rst to include

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   generated

7. Add the following to *regions.rst* right below `:methods:`
   `:special-members: __init__`

8. Delete "docs/source/generated/modules.rst"

9. Change index.rst, symbols.rst

############################################

10. Execute `make.bat html`, when using windows try `.\make.bat html`, ignore single occurence of warning: `Inline strong start-string without end-string`

11. Open /PySaar2024/docs/build/html/index.html
