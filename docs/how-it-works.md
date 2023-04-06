---
title: docstring2pdf のしくみ
summary: どうやってサイト生成から PDF 出力までを実現しているか
authors:
  - Ningensei848
date: 2023-04-03
---

# How it works ?

大まかに分けると、以下の三段階で機能している：

1. [`mkdocstrings`](https://mkdocstrings.github.io/) でコード内の当該部分を抜き出す
2. [`MkDocs`](https://www.mkdocs.org/) で静的サイトを生成
3. [`mkdocs-with-pdf`](https://github.com/orzih/mkdocs-with-pdf) でサイトを PDF 化

### `mkdocstrings`

[Recipes](https://mkdocstrings.github.io/recipes/) にもある通り、
さらに他の _plugins_ と組み合わせることによって、 docstring から文書の自動生成を達成している。

- [`mkdocs-gen-files`](https://github.com/oprypin/mkdocs-gen-files)
- [`mkdocs-literate-nav`](https://github.com/oprypin/mkdocs-literate-nav)
- [`mkdocs-section-index`](https://github.com/oprypin/mkdocs-section-index)

これらの組み合わせにより、いちいち別のファイルを経由せずとも
対象の `*.py` ファイルから抜き出してページを生成できるようになっている。

### `MkDocs`

プロジェクトの根幹を成すのが静的サイトジェネレータの一つである *MkDocs* だ。
ただし、これはあくまでベースとしての利用にとどめており、実際にメインを飾っているのは
 [`Material for MkDocs`](https://squidfunk.github.io/mkdocs-material) である。

https://squidfunk.github.io/mkdocs-material

テーマがきれいであることはもとより、様々なカスタマイズができるし、開発も盛んである。
これのおかげで、いま読んでいるこのドキュメントも今風のいい感じの UX を提供できている。

### `mkdocs-with-pdf`

https://github.com/orzih/mkdocs-with-pdf

端的に言えば、「これしかなかった」から使っている。
これがデファクトというよりは、これ以外のものが見当たらなかった。
（あっても同様に開発が止まっているもの）

メンテされていない風に見えるのが非常に気になるところだが、
代替案が見つけられていない以上仕方がない。

## GitHub Actions and Google Drive

３つの機能の外側には、GitHub Actions によるビルド自動化と
 [`rclone`](https://rclone.org/drive) による Google Drive との同期も行われている。
リポジトリに変更があるたびにトリガーされ、
ブランチごとのドキュメントがドライブにアップロードされるという仕組みである。

### `rclone`

> クラウドストレージ上のファイル管理を行うオープンソースのコマンドライン型プログラムです。
> Amazon S3やGoogle Drive、Alibaba Cloud、Dropbox、Megaなど40以上の
> クラウドストレージサービスに対応しており、ファイルの転送、暗号化、圧縮、分割、バックアップ、
> 復元、同期、ミラーリング、マイグレーション、ストレージ管理といった様々な機能を具備しています。
>
> cf. https://www.sompocybersecurity.com/column/glossary/rclone

Go 製の OSS で、あらゆるクラウドストレージに対応している。
利用者が世界中にいることもあって、日々の開発はたいへん盛んに行われている。

ストレージごとの公式 API やライブラリを使う以外ではもっとも有名でデファクトなツールである。
基本的には単なる Wrapper CLI なので対象が増えるごとに大きくなりがちなところ、
golang で実装することにより手軽さも速度も実現しているようだ（素直にすごい）。

---

## Next

以上を踏まえて、具体的な導入方法についても説明する

→ [How to install](how-to-install.md)
