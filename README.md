# mailerdenight アプリサイト

アプリ紹介・サポート・プライバシーポリシーの正規管理元です。

## ページの構成

- 総合案内: https://mailerdenight.github.io/
- アプリ紹介: /<slug>/
- サポート: /<slug>/support/
- プライバシー: /<slug>/privacy/

総合案内は20アプリ。Sound EffectsとPico Buttonsは同じアプリとして掲載します。
既存ページの政策本文は移行時に維持しています。
App Storeリンクは既存資料で具体的なURLを確認できたアプリにのみ掲載しています。

## 正規URL一覧

| アプリ | URL |
| --- | --- |
| ジム歩走ログ | https://mailerdenight.github.io/gym-walk-log/ |
| 親子の返済ノート | https://mailerdenight.github.io/parent-child-repayment/ |
| 余命予算 | https://mailerdenight.github.io/yomei-yosan/ |
| 禁欲ログ | https://mailerdenight.github.io/kinyokulog/ |
| 婚活アポログ | https://mailerdenight.github.io/konkatsu-apolog/ |
| 麻辣湯ログ | https://mailerdenight.github.io/malatang/ |
| バインミーログ | https://mailerdenight.github.io/banhmi/ |
| ビリヤニログ | https://mailerdenight.github.io/biryani-log/ |
| 焼肉手帳 | https://mailerdenight.github.io/yakiniku-techo/ |
| むしサウンド | https://mailerdenight.github.io/mushi-sound/ |
| かえるサウンド | https://mailerdenight.github.io/kaeru-sound/ |
| せみサウンド | https://mailerdenight.github.io/semi-sound/ |
| ことりサウンド | https://mailerdenight.github.io/kotori-sound/ |
| のりものサウンド | https://mailerdenight.github.io/norimono-sound/ |
| どうぶつサウンド | https://mailerdenight.github.io/doubutsu-sound/ |
| 鳥・ねずみ除けサウンド | https://mailerdenight.github.io/bird-deterrent-sounds/ |
| Sound Effects（Pico Buttons） | https://mailerdenight.github.io/sound-effects/ |
| どうぶつポン！ | https://mailerdenight.github.io/animal-pop/ |
| 自動車免許クイズ 2026 | https://mailerdenight.github.io/driving-quiz/ |
| RetroDrive | https://mailerdenight.github.io/retrodrive/ |

## 旧URL

旧ディレクトリには新URLへの転送ページを残しています。
ページ専用リポジトリ側も同じ転送に切り替え、本文の二重管理を止めます。
アプリのコードを含むリポジトリは削除対象にしません。
App Store Connectや配信済みアプリ内のURLはこのリポジトリの変更だけでは更新されません。

最終整理日: 2026-10-09 (JST)

## 言語切替の本文検査

GitHub Actions の `Page locale coverage` が、PR・mainへのpush・手動実行で検査します。
Python 3.12の標準ライブラリのみで動作し、追加パッケージは不要です。

```sh
python -m unittest discover -s tests -v
python scripts/check_page_locales.py
```

上記の正規URL一覧からアプリを読み取り、紹介・サポート・プライバシーの3ページを検査します。
アプリ追加時は一覧への追記で検査対象も増えます。旧URLの転送ページは対象外です。
言語選択肢、`support-page-config`の言語、`data-page-locale`の本文の対応を調べ、
空本文・ブロック欠落・設定不一致・ページ欠落をファイル名と言語付きで報告します。
コメント、空タグ、空白、script/style/template、非表示の子要素は本文と数えません。
言語ブロック自体の初期`hidden`は、切替時に解除されるため空本文判定から除外します。
ジム歩走ログのFAQ・ポリシーなど、共通JavaScriptで生成する本文も設定値で検査します。
言語切替を実装していない単一言語ページも対象ファイルとして読み取りますが、翻訳を要求しません。

既知の欠落は `scripts/page-locales-baseline.json` にファイル・言語・問題種別・理由を限定して記録します。
2026-10-12、コミット `eac65a4955cb68c7c5e4b39fb157aa3139b63dd5` で確認した既知の欠落は、
親子の返済ノートの `support/index.html` の英語本文が空である1件です。
翻訳修正は別作業とし、この検査の追加では本文を変更しません。
`KNOWN`は表示して通常のCIを通し、新規問題の`NEW`で失敗します。
修正済みの項目は`RESOLVED`として表示し、独立した翻訳PRを妨げずにベースライン削除を促します。
既知の問題も含めて失敗させるには `python scripts/check_page_locales.py --strict` を実行します。
ベースラインの一括再生成は行わず、追加する場合は欠落の理由をレビューしてください。

これは現在の共通JavaScriptの本文生成方式に合わせた静的検査です。
外部CSSによる非表示、ブラウザー実行時のJavaScriptエラー、翻訳の意味や品質は判定しません。
本文生成方式を変更する際は検査処理と回帰テストも更新してください。
