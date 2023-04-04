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
    mkdocs_path = Path.cwd() / "mkdocs.yml"

    # read content of `mkdocs.yml`
    config = mkdocs_path.read_text()
    # prepare backup (note: this file is deleted after `mkdocs export`)
    mkdocs_path.with_stem("backup_mkdocs").write_text(config)
    # write new text with `G-XXXXXXXXXX` replaced by `$GOOGLE_ANALYTICS_ID`
    mkdocs_path.write_text(pattern_ga4.sub(ga4_id, config))

    return


if __name__ == "__main__":
    prepare_google_ads()
    prepare_google_analytics()
