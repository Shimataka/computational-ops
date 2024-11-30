# Python開発環境

- 仮想環境に [uv]((https://github.com/astral-sh/uv)) を使用します。
- localでpython 3.12を使用します。
- その他のバージョンを使用する場合、
[reviewdog_python.yml](../../../.github/workflows/reviewdog_python.yml)
中のバージョン指定を変更する必要があります。
- 本開発環境で使用したツール一覧
    | カテゴリー | ツール |
    | :---: | :---: |
    | Package & Project manager | [uv](https://github.com/astral-sh/uv) |
    | Linter & Formatter | [ruff](https://github.com/astral-sh/ruff) |
    | Type Checker | [mypy](https://github.com/python/mypy) |
    | Test | [pytest](https://github.com/pytest-dev/pytest) |
    | Docs generator | [Sphinx](https://www.sphinx-doc.org/) |

## How to start

以下の手順に従ってください。

### 1. リポジトリ内のディレクトリ構成を作成

[.settings/templates/python/makeenv.sh](makeenv.sh) を実行してください。

```bash
.settings/templates/python/makeenv.sh
```

### 2. `uv` をインストール

公式 [uv - Getting Started](https://docs.astral.sh/uv/#getting-started)
に従ってインストールしてください。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

もしくはすでにpythonをインストールしている場合は `pip` からもインストールできます。

```bash
pip install uv
```

インストールできたら、以下のコマンドを実行してください。

```bash
uv init -p 3.12 # 仮想環境の作成 (python 3.12)
uv sync
. .venv/bin/activate # 仮想環境の有効化
```

### 3. `ruff` パッケージを追加

```bash
uv add ruff --dev
```

### 4. `mypy` パッケージを追加

```bash
uv add mypy --dev
```

### 5. `pytest` パッケージを追加

```bash
uv add pytest --dev
uv add pytest-cov --dev
```

### 6. `Sphinx` パッケージを追加

```bash
uv add sphinx --dev
uv add esbonio --dev
uv add myst-parser --dev
sphinx-quickstart docs
> ソースディレクトリとビルドディレクトリを分ける（y / n） [n]: y # <-- y にする
> プロジェクト名: <MYPROJECTNAME> # <-- プロジェクト名を入力
> 著者名（複数可）: <YOURNAME> # <-- 著者名を入力
> プロジェクトのリリース []: <VERSION> # <-- バージョンを入力
> プロジェクトの言語 [en]: <LANGUAGE> # <-- 言語を入力 (ja とか)
```

### 7. 追加したツールの設定ファイルを追記

[.settings/templates/python/finishenv.sh](finishenv.sh) を実行してください。

```bash
.settings/templates/python/finishenv.sh
```

## How to run

### 仮想環境の有効化

```bash
. .venv/bin/activate
```

### コードの実行

`uv` から実行できます。

```bash
uv run src/{example_new_repo}/main.py # main.pyを実行
```

### ドキュメントの生成

VSCodeのタスク `py-doc-gen` を実行してください。
`Sphinx` が実行され、`docs/build/html/index.html` が生成されます。

また `docs/source/*.rst` ファイルはVSCodeであれば、プレビュー表示が可能です。
右上の「プレビューを横に表示」ボタンを `Alt` と共に押してください。

- uvコマンドが見つからないエラーが出る場合

    [.vscode/tasks.json](../../../.vscode/tasks.json) 中に記述した `~/.cargo/bin/uv` が、
    `which uv` コマンドの出力と一致することを確認してください。

- sphinx-build が見つからないエラーが出る場合

    [.vscode/tasks.json](../../../.vscode/tasks.json) 中に記述した
    `"${workspaceFolder}/.venv/bin/sphinx-build"` が、
    `which sphinx-build` コマンドの出力と一致することを確認してください。

### コードチェックの実行

`mypy` はコードを書けば自動で実行されます。

`Ctrl+s` によって `ruff` `pytest` が実行されます。
`pytest` で算出したカバレッジは、[.pyコード中に色で表示されます](https://zenn.dev/tyoyo/articles/769df4b7eb9398)。

`pytest` が実行されない場合、VSCodeのタスク `py-code-check` を実行してください。
`pytest` に加え、 `ruff` と `mypy` も実行されます。
