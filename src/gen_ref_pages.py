"""
このように、ファイル名がページタイトル（h1 要素）となり、
以降は各関数が見出し（h2 要素）、小見出し（h3 要素）と続く。

すべて `.py` から抽出して来たものである。
これを普段から利用すれば、いずれはドキュメント駆動でコードを書く習慣が身につくはず！
"""

from pathlib import Path

import mkdocs_gen_files

dirs = ["src"]
cwd = Path.cwd()

nav = mkdocs_gen_files.Nav()


def setEditPath(directory: Path) -> None:
    """Generate pages on-the-fly via `mkdocs-gen-files` plugin

    [recipes](https://mkdocstrings.github.io/recipes/) に書いてある通り、
    [`mkdocs-gen-files`](https://oprypin.github.io/mkdocs-gen-files/) と
    [`mkdocs-literate-nav`](https://oprypin.github.io/mkdocs-literate-nav/)
    を使用して自動的にページを生成する。
    この `setEditPath()` は、`mkdocs_gen_files.set_edit_path()`
    の wrapper である。
    引数としてディレクトリを与えると、その配下にある `.py` ファイルを再帰的に走査し、
    その全てから docstring を抽出してドキュメントを生成してくれる。

    Args:
        directory: An *pathlib.Path* instance.
            In the given directory, Generate documentation
            by recursively looking for `*.py` files.
            cf. https://docs.python.org/ja/3/library/pathlib.html#pathlib.Path
    Returns:
        None
    """

    for path in sorted(directory.rglob("*.py")):
        print(path)
        module_path = path.relative_to(cwd).with_suffix("")  # remove suffix
        doc_path = path.relative_to(cwd).with_suffix(".md")  # replace suffix
        full_doc_path = Path("reference", doc_path)

        parts = tuple(module_path.parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue

        nav[
            parts
        ] = doc_path.as_posix()  # Progressively build the navigation object.

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            fd.write(f"::: {ident}")

        # mkdocs_gen_files.set_edit_path(full_doc_path, path)
        mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)


for d in dirs:
    print(d)
    setEditPath(cwd / d)

sources = [
    f"{line.strip()}\n"
    for line in nav.build_literate_nav()
    if not line.startswith("*")
]

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(sources)
