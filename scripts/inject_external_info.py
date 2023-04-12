"""
`mkdocs.yml` や _overrides_ では、外部情報をベタ書きする必要があり避けたい。

python でスクリプトを書き、以下の二つのアプローチで対応する。

1. `overrides/*.html` を生成する ( _*recommended*_ )
2. `mkdocs.yml` を上書きする

@see:
https://squidfunk.github.io/mkdocs-material/customization/#overriding-blocks
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv

# take environment variables from .env.
# cf. https://github.com/theskumar/python-dotenv
load_dotenv()

pattern_ga4 = re.compile(r"G-\w+")
pattern_show_source = re.compile(r"show_source:\s+(true|on|yes|1)")

MKDOCS_PATH = Path.cwd() / "mkdocs.yml"
BACKUP_PATH = Path.cwd() / "backup_mkdocs.yml"


def create_backup() -> None:
    """`mkdocs.yml` のバックアップファイルを作成する"""
    # read content of `mkdocs.yml`
    config = MKDOCS_PATH.read_text()
    # prepare backup (note: this file is deleted after `mkdocs export`)
    BACKUP_PATH.write_text(config)

    return


def prepare_google_ads() -> None:
    """Embed Google Ads in MkDocs (via `overrides`)

    MkDocs に Google Adsense の広告を埋め込むには、`overrides/main.html` を拡張して
    `head` 要素内に広告スクリプトを置いてやることになる。
    静的ファイルにベタ書きしたくないので、python スクリプトで生成する。
    """

    ads_id = os.environ.get("GOOGLE_ADS_ID", "ca-pub-XXXXXXXXXXXXXXXX")
    filepath = Path.cwd() / "overrides/main.html"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        '{% extends "base.html" %}\n',
        "{% block extrahead %}",
        "\t<script async"
        + " "  # whitespace * 1
        + 'src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
        + f'?client={ads_id}" crossorigin="anonymous"></script>',
        "{% endblock %}\n",
    ]

    filepath.write_text("\n".join(lines))

    return


def prepare_google_analytics() -> None:
    """Embed Google Analytics in MkDocs (via `mkdocs.yml`)

    MkDocs に Google Analytics を設置するには、`mkdocs.yml` に設定を加えてやればよい。
    Theme ごとに書き方の揺れはあるが、おおよそ `G-XXXXX` を書けば済む。

    しかし、実際にはそういう情報を 設定ファイルにベタ書きしたくない。
    よって、python スクリプトで当該部分を置換してやることにした。
    """

    ga4_id = os.environ.get("GOOGLE_ANALYTICS_ID", "G-XXXXXXXXXX")
    config = MKDOCS_PATH.read_text()

    # write new text with `G-XXXXXXXXXX` replaced by `$GOOGLE_ANALYTICS_ID`
    MKDOCS_PATH.write_text(pattern_ga4.sub(ga4_id, config))

    return


def prepare_template_sitemap() -> None:
    """Fix `sitemap.xml` with incorrect value `None`

    MkDocs ではデフォルトで `sitemap.xml` を出力する機能があるのだが、
    いろいろなプラグインを入れていく過程でなぜか不正なURLを持つようになってしまった。

    `<loc>None</loc>` となっている部分を排除すればいいので、
    Jinja2 template の該当部分を見て条件分岐を修正した。
    """
    filepath = Path.cwd() / "overrides/sitemap.xml"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "{%- for file in pages -%}",
        "\t{% if not file.page.is_link and not file.page.canonical_url is none"
        " and not file.page.abs_url is none %}",
        "\t<url>",
        "\t\t<loc>{% if file.page.canonical_url %}"
        "{{ file.page.canonical_url|e }}{% else %}{{ file.page.abs_url|e }}"
        "{% endif %}</loc>",
        "\t\t{% if file.page.update_date %}<lastmod>"
        "{{file.page.update_date}}</lastmod>{% endif %}",
        "\t\t<changefreq>monthly</changefreq>",
        "\t</url>",
        "\t{%- endif -%}" "{% endfor %}",
        "</urlset>",
    ]

    filepath.write_text("\n".join(lines))

    return


def disable_show_source() -> None:
    """Disable Handler Option (`show_source`) in MkDocs (via `mkdocs.yml`)

    Python Hanfler の option で、ソースコードの表示をオフにする。

    PDF として出力する際に、当該ソースコードが長大になると **うまく出力されなくなる**。
    これを防止するために、ソースコード無しで出力させる。
    （あるいは出力方法を変更すれば解決するかも……？）

    静的サイトとしてビルドする際は、ソースコードがあったほうがいいと思う。
    よって、python スクリプトで当該部分を切り替えられるようにした。
    """

    config = config = MKDOCS_PATH.read_text()
    MKDOCS_PATH.write_text(
        # Change flag `show_source` from _truthy_ to _falsy_
        pattern_show_source.sub("show_source: no", config)
    )

    return


if __name__ == "__main__":
    create_backup()

    prepare_google_ads()
    prepare_google_analytics()
    prepare_template_sitemap()

    # PDF として出力する際は、ソースコードの表示をオフにする
    if os.environ.get("ENABLE_PDF_EXPORT", False):
        disable_show_source()
