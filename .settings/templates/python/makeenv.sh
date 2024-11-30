#!/bin/bash

# To make environments
cd "$(dirname ${0})"

## Copy ./reviewdog_python.yml to ~/.github/workflows/reviewdog_python.yml
cp ./reviewdog_python.yml ../../../.github/workflows/reviewdog_python.yml

## Copy ./extensions.json to ~/.vscode/extensions.json
cp ./extensions.json ../../../.vscode/extensions.json

## Copy ./settings.json to ~/.vscode/settings.json
cp ./settings.json ../../../.vscode/settings.json

## Copy ./tasks.json to ~/.vscode/tasks.json
cp ./tasks.json ../../../.vscode/tasks.json

## Makedir for sphinx
mkdir -p ../../../docs/

## Makedir for pytest
mkdir -p ../../../tests/
touch ../../../tests/__init__.py

## Copy .gitignore to ~/
cp ./.gitignore ../../../.gitignore

## git config (core.hooksPath -> .settings/templates/git/hooks)
git config --local core.hooksPath .settings/templates/git/hooks
