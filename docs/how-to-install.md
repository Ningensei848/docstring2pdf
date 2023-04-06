---
title: docstring2pdf の導入方法
summary: どうやって既存プロジェクトに導入するか
authors:
  - Ningensei848
date: 2023-04-06
---

# Installation

## Python libraries

まず、Python プロジェクトとしての依存関係はすべて [`Poetry`](https://python-poetry.org/)、
そして　[`pyproject.toml`](https://github.com/Ningensei848/docstring2pdf/blob/main/pyproject.toml) で管理されている。
既存プロジェクトに移植する際には、この設定ファイルをリポジトリのトップに置いてやるのがいいだろう。
その上で、次のコマンドを実行すれば必要なライブラリ群をインストールできる：

```shell title="install command"
poetry install --with docs # (1)!
```

1. リポジトリ内に .venv/ として仮想環境を作る場合には以下を先に実行すること<br />
`poetry config --local virtualenvs.in-project true`

## `MkDocs`

次に [MkDocs](https://www.mkdocs.org/) を利用したドキュメント生成全般の設定については、
[`mkdocs.yml`](https://github.com/Ningensei848/docstring2pdf/blob/main/mkdocs.yml) で管理している。
このファイルもまた `pyproject.toml` と同じ階層に置くようにする。
さらに、適宜必要なドキュメントを置くための `docs` というフォルダも作成する。

ここまでで、次のような構造になっているはずだ：

```shell title="tree"
.
├── .git       # from
├── .gitignore   # your
├── src            # projects
...
├── .venv      # ---> optional
├── docs
├── mkdocs.yml
├── poetry.lock
└── pyproject.toml
```

ここで、以下のコマンドを実行することで `mkdocs` の開発サーバが立ち上がる：

```shell title="Run development server"
$ poetry run mkdocs serve
INFO     -  Building documentation...
WARNING  -  without generate PDF(set environment variable ENABLE_PDF_EXPORT to 1 to enable)
INFO     -  Cleaning site directory
INFO     -  Documentation built in 0.86 seconds
INFO     -  [hh:mm:ss] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO     -  [hh:mm:ss] Serving on http://127.0.0.1:8000/docstring2pdf/
```

ブラウザで開くと、以下のような画面が見られたであろうか
（カスタマイズを施していない段階では、多少デザインが異なる部分はあるかもしれない）

<figure markdown>
  ![preview of `poetry run mkdocs serve`](../img/screenshot_mkdocs_serve.png)
  <figcaption>preview of `poetry run mkdocs serve`</figcaption>
</figure>

## Scripts

次に、`docstring` からドキュメントを生成するためのスクリプトを配置する。
具体的には、例えば `scripts` というフォルダを作成し、
その中に [`gen_ref_pages.py` というファイル](../reference/scripts/gen_ref_pages)を置けばいい。

そして、変数 `dirs` の値を自分の環境に合わせて変更すれば、
指定したフォルダ内の `*.py` ファイルを再帰的に走査し、
`reference/` 以下にページを生成してくれる。

```python title="gen_ref_pages.py"
from pathlib import Path

import mkdocs_gen_files

dirs = ["scripts"] # (1)!
cwd = Path.cwd()

nav = mkdocs_gen_files.Nav()
```

1. 例えば `src` などの **ドキュメント化したい対象のコードがあるディレクトリ名** を追記する。

## Stylesheets

最後に、スタイルの調整を行なう。
ここまでの設定では表示がズレていたり、細部のデザインが荒かったりするからだ。

具体的には、`mkdocs.yml` 内の `theme.extra_css` にファイルパスを指定する。
これだけで、指定したスタイルシートの内容が上から順番に読み込まれる。

```yaml title="mkdocs.yml"
theme:
  extra_css:
    - stylesheets/base.css
    - stylesheets/material.css
    - stylesheets/mkdocstrings.css
```

ファイルパスで指定するため、実はファイル実体をどこに置いても良い。
基本的には `docs` の直下に `stylesheets` などのディレクトリを置くべきだろうが、
各プロジェクトによって調整してもらいたい。

## Next

これで、PDF を得るまでの設定は一通り終えたことになる。

次は、いよいよ実際に出力する。
ついでに、Google Drive に同期させるところまで行なう。

→　[How to use](how-to-use.md)
