---
title: docstring2pdf の紹介
summary: mkdocs とそのプラグインを組み合わせて、ドキュメントをPDF化する仕組みを構築した
authors:
  - Ningensei848
date: 2023-04-03
---

# What is it ?

<!-- Admonition -->
!!! tip "the answer is ..."
    **`docstring2pdf`** とは、コードとともにドキュメントを書くチームを支援し、
    <u>常にそのドキュメントを最新に保つためのプロジェクト</u>である。
<!-- end Admonition -->
---

いざ Python を使い始めたはいいが、
コードを書いてばかり / データ分析するだけしてそのまま放置してしまい、
ドキュメントを書くという行為をサボっている組織は少なくない。

Python においては、その問題を解決しうる仕組みとして
 [`docstring`](https://peps.python.org/pep-0257/) がある。
「<u>コードとは別にドキュメントを書かねばならない…</u>」からやがて億劫になるのであって、
それが**ソースコードとともに書くべきもの**となれば、開発チームの意識は変わっていく――

`docstring2pdf` では、`docstring` からきれいで見やすい ＋ 検索もできる！
という静的ドキュメンテーションサイトの生成はもちろん、
その内容を PDF に出力して Google Drive にアップロードするところまでを実装した。
既存プロジェクトへの移植も、いくつかの設定ファイルをコピペするだけでよい。

ドキュメンテーションに悩むすべての組織に、ぜひとも導入を検討してもらいたい。

## Next

- [How it works ?](how-it-works.md)
- [How to introduce to existing project ?](how-to-install.md)
