---
title: docstring2pdf の使い方
summary: どうやって PDF を出力し Google Drive 上に同期させるか
authors:
  - Ningensei848
date: 2023-04-06
---


# Usage

## How to Export

設定ファイル等が正しく記述されて `poetry run mkdocs serve` も滞りなく実行されていれば、
あとは別途コマンドを実行するだけで PDF への出力は可能となっている：

```shell title="export command"
ENABLE_PDF_EXPORT=1 poetry run mkdocs build
```

[`ENABLE_PDF_EXPORT`](https://github.com/orzih/mkdocs-with-pdf#-and-more) は、
PDF を出力したいときに付与する環境変数であり、`mkdocs.yml` には以下のように指定する：<br />
（※環境変数抜きで実行すると、PDF が出力されなくなる）

```yaml title="mkdocs.yml"
plugins:
  - with-pdf: # cf. https://github.com/orzih/mkdocs-with-pdf
        enabled_if_env: ENABLE_PDF_EXPORT  # (1)!
```

1. デフォルトでは空白（≒Falsy）な値となり、PDF が出力されない。
    `--watch` 等でリビルドを繰り返す際に、PDF への出力は非常に負担がかかるため、
    **必要な時以外は出力しないようにしておく機能** である。

こうして、`build` ディレクトリ直下に `document.pdf` が出力されていることが確認できれば完了だ。

## How to Upload

ドキュメントを PDF に出力して得られたまではいいが、
チーム開発でつかうのであれば共有ドライブに置きたい…という需要は少なくないと思う
（事実、私の手伝っているチームでもそういう課題があった）。
また、共有ドライブに置いたとしても、各人が好き勝手してしまい「一体どのファイルが最新なのか？」
というバージョン管理の問題も発生してしまっている状況もあった。

つまり、以下の３つが要件である：

1. 共有ドライブにファイルを置く
2. 最新版であることがわかるようにする
3. 人の手を介入させない

これを満たすには、GitHub Actions で Google Drive にアップロードするしかないと考えて、
次のような実装を行った。

### `rclone` をつかう

[`rclone`](https://rclone.org/)とは、Go 製の OSS であり、
あらゆるクラウドストレージ上のファイル管理を行う CLI ツールである。

これを使えば、GUI での操作やインタラクティブな操作をせずに Google Drive 上の
任意のフォルダにファイルを置くことができる。

<!-- block Admonition -->
??? info "以降の内容は、主にチーム向けのものです"
    もし、個人向けに `rclone` を使いたい場合、サービスアカウントではなく
    あなた自身の `client_id` を使用するといいでしょう。

    cf. https://rclone.org/drive/#making-your-own-client-id <br />
    cf. [rclone 用に独自の Google Drive クライアント ID を作成する。](https://gyo.tc/https://www.wave440.com/wave_log/client_id.html)
<!-- end Admonition -->

#### GCP から認証情報を得る

<!-- block Admonition -->
!!! quote "Google Drive 向けの `rclone` では、 サービスアカウントからの利用をサポートしている"
    - https://rclone.org/drive/#service-account-support
<!-- end Admonition -->

以下の手続きを踏むことでサービスアカウントの認証情報（JSONファイル）が入手できる：

1. [公式ドキュメント](ttps://cloud.google.com/iam/docs/service-accounts-create)
    を読んでサービスアカウントを作成する
2. ↑ その際に、「ロール」は空白のままでよい
3. 別の[公式ドキュメント](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority)
    を読んでドメイン全体の権限をサービスアカウントに委任する
4. 「アカウントの詳細」からキーの項目に移動し、鍵を追加 >> 新しい鍵を作成　と進む
5. JSON ファイルがダウンロードされるので大切に保管する

##### 公式ドキュメント：

- [サービス アカウントを作成する | IAM のドキュメント | Google Cloud](https://cloud.google.com/iam/docs/service-accounts-create)
- [ドメイン全体の権限をサービス アカウントに委任する | サーバー間アプリケーションに OAuth 2.0 を使用する | Authorization | Google Developers](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority)

#### Google Drive 上で保存先を決める

次は、「どこにファイルを置くか」を決める。
必須となるのは、共有ドライブ（旧称・チームドライブ）の ID だ。
これは、ブラウザ上で共有ドライブを開いたときに表示される URL の一部を参照することで判別できる。

追加として、共有ドライブのどこかに位置するフォルダの ID もあるとよい。
`rclone` から操作しうる範囲を限定して使うようにしたほうが安全だからだ
（人はいつか必ずミスをするし、そのタイミングは決まっていつも
["身構えていないときに来る"](https://google.com/search?q=身構えている時には、死神は来ないものだ)）。

<!-- block Admonition -->
??? note "id の場所"
    1. ドライブを開く
    2. URL を見る
    3. `drive/folders/{foler_id}` から `foler_id` を抜き出す
        - 共有ドライブは `0`, その中のフォルダは `1` から始まるようだ
<!-- end Admoniton -->

#### GitHub Actions の設定

いよいよ †完成† が近づいてきた。
ここまでよく目を通してくれたと思う、深く感謝する。

最後は、リポジトリの Settings で Actions に用いるための環境変数を指定していく。

必要となるのは、以下の５つである：

1. `GCP_SERVICE_ACCOUNT` ... サービスアカウントのメールアドレス
2. `SERVICE_ACCOUNT_CREDENTIAL` ... サービスアカウントの認証情報の JSON 文字列
3. `TEAM_DRIVE_ID` ... 共有ドライブの ID
4. `ROOT_FOLDER_ID` (optional) ... 共有ドライブ内にある任意のフォルダの ID
5. `GOOGLE_DRIVE_DIR` (optional) ... 自動的に作成されるフォルダ名


`ROOT_FOLDER_ID` では、基点となるフォルダを指定したが、
`GOOGLE_DRIVE_DIR` はブランチごとに作成されるドキュメント群の親ディレクトリとして作成される。
デフォルトでは、`env.FILENAME` と同じものが使用されるが、使い分けたい場合は直接変更すること。

---

これらの変数を、Action 実行時の秘密情報として登録する。

> Settings >> Secrets and Variables >> Actions >> \[New Repository Secret\]

変数名と値を入力したら "Add Secret" すればよい。

こうして、GitHub Actions 実行の準備が全て整った。
あとは、自分の環境に [`.github/workflows/actions.yml`](https://github.com/Ningensei848/docstring2pdf/blob/main/.github/workflows/actions.yml)を作り、内容をコピペしてリポジトリにプッシュするだけである。

```shell title="copy and paste"
# コピペも面倒な皆さんのために、次のようなコマンドをご用意しました〜

mkdir -p .github/workflows && \
curl https://raw.githubusercontent.com/Ningensei848/docstring2pdf/main/.github/workflows/actions.yml > .github/workflows/actions.yml

# then, `git commit` and `git push`
```

### Results

無事、リポジトリにプッシュされて GitHub Actions が回ったとしよう。
最終的に、Google Drive 上に PDF ドキュメントがアップロードされる。

このドキュメントは、<u>GitHub Actions が正常に実行完了するたびに更新される</u>。
すなわち、**新たにコミットをプッシュするたびに自動的に最新のドキュメントが生成され、
PDF ファイルを共有ドライブ上に同期させる** ――

!!! quote
    1. 共有ドライブにファイルを置く
    2. 最新版であることがわかるようにする
    3. 人の手を介入させない

当初の三要件は、無事に全てクリアできたのではないだろうか。

---

本リポジトリの最終成果物も、当然ながら同期されている。
以下のリンクから参照してみてほしい：

- [`docstring2pdf` で生成された PDF ドキュメント on Google Drive](https://drive.google.com/file/d/1ZKmctj0j7pJnoBCdoCsAN1MghouQFTlT)
