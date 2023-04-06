---
title: docstring2pdf の紹介
summary: mkdocs とそのプラグインを組み合わせて、ドキュメントをPDF化する仕組みを構築した
authors:
  - Ningensei848
date: 2023-04-03
---

# What is it ?

コードを書いてばかり、あるいはデータ分析してばかりで、
ドキュメントを書くという行為をサボっている組織は少なくない。

Python においては、その問題を解決しうる仕組みとして
 [`docstring`](https://peps.python.org/pep-0257/) がある。
「コードとは別にドキュメントを書く」からやがて億劫になるのであって、
それがソースコードとともに書くべきものとなれば、開発チームの意識は変わっていく――

`docstring2pdf` では、`docstring` からきれいで見やすい ＋ 検索もできる！
という静的ドキュメンテーションサイトの生成はもちろん、
その内容を PDF に出力して Google Drive にアップロードするところまでを実装している。
<!-- TODO: 既存プロジェクトへの移植も、いくつかの設定ファイルをコピペするだけでよい。 -->

ドキュメンテーションに悩むすべての組織に、ぜひとも導入を検討してもらいたい。

## Next

- [How it works ?](how-it-works.md)
- [How to introduce to existing project ?](how-to-install.md)
