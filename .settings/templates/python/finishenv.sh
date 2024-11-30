#!/bin/bash

# To make environments
cd "$(dirname ${0})"

## ./tools_pyproject.toml >> ~/pyproject.toml
if [ -f ../../../pyproject.toml ]; then
    cat ./tools_pyproject.toml >> ../../../pyproject.toml
fi

## Edit docs/source/conf.py
if [ -f ../../../docs/source/conf.py ]; then
    sed -i -e "s/extensions = \[\]/extensions = \[\n    'sphinx.ext.autodoc',\n    'sphinx.ext.napoleon',\n    'myst_parser'\n\]/g" ../../../docs/source/conf.py
fi

## Edit .vscode/tasks.json
MYPROJECTNAME_JOINED=`sed -n -e '2s/"\([^"]*\)".*/\1/p' ../../../pyproject.toml`
MYPROJECTNAME_SPLIT=(${MYPROJECTNAME_JOINED//./ })
if [ -f ../../../.vscode/tasks.json ]; then
    sed -i -e "s/MYPROJECTNAME/${MYPROJECTNAME_SPLIT[2]}/g" ../../../.vscode/tasks.json
fi

## Avoid mypy error
touch ../../../src/__init__.py
