# App Store URL統一

確認日: 2026-10-10 (JST)

日本のApp Store公開ページから、サポートURL・プライバシーポリシーURL・マーケティングURLを確認しました。公開ページのserialized-server-dataに含まれるサポートURLも確認対象です。

## App Store Connectで更新するURL

以下の7アプリはサポート・プライバシーURLが現行URLと異なります。Apple側の設定は、このGitHubコミットでは変更していません。ローカライズされた各言語のURLも確認してください。

| アプリ | App ID | サポートURL | プライバシーポリシーURL | 紹介URL（設定する場合） |
|---|---|---|---|---|
| 余命予算 | 6767985543 | https://mailerdenight.github.io/yomei-yosan/support/ | https://mailerdenight.github.io/yomei-yosan/privacy/ | https://mailerdenight.github.io/yomei-yosan/ |
| 禁欲ログ：習慣記録 | 6798738455 | https://mailerdenight.github.io/kinyokulog/support/ | https://mailerdenight.github.io/kinyokulog/privacy/ | https://mailerdenight.github.io/kinyokulog/ |
| 婚活 - アポログ | 6770220914 | https://mailerdenight.github.io/konkatsu-apolog/support/ | https://mailerdenight.github.io/konkatsu-apolog/privacy/ | https://mailerdenight.github.io/konkatsu-apolog/ |
| バインミーログ | 6799560143 | https://mailerdenight.github.io/banhmi/support/ | https://mailerdenight.github.io/banhmi/privacy/ | https://mailerdenight.github.io/banhmi/ |
| 乗り物の音・のりものサウンド | 6782409549 | https://mailerdenight.github.io/norimono-sound/support/ | https://mailerdenight.github.io/norimono-sound/privacy/ | https://mailerdenight.github.io/norimono-sound/ |
| どうぶつの鳴き声・動物サウンド | 6799204438 | https://mailerdenight.github.io/doubutsu-sound/support/ | https://mailerdenight.github.io/doubutsu-sound/privacy/ | https://mailerdenight.github.io/doubutsu-sound/ |
| レトロドライブ | 6804456291 | https://mailerdenight.github.io/retrodrive/support/ | https://mailerdenight.github.io/retrodrive/privacy/ | https://mailerdenight.github.io/retrodrive/ |

## 旧URLの互換性

- 禁欲ログ: App Storeの旧 /kinyoku-log/ 配下は404だったため、紹介・サポート・プライバシーの3URLに /kinyokulog/ 配下への転送を追加。
- バインミーログ: App StoreのサポートURLは /banhmi/（紹介ページ）。紹介ページは保持し、上部メニューからサポートへ進める。Apple側では /banhmi/support/ へ変更する。privacy.html は現行プライバシーへ転送。
- 余命予算、婚活アポログ、のりものサウンド、どうぶつサウンド、レトロドライブ: 旧サポート・プライバシーURLから現行ページへの転送は維持。
- 禁欲ログ・のりものサウンドの旧マーケティングURLも、表の紹介URLへ統一する。

GitHub側の公開成功と、Apple側の登録URL更新は別々に確認する。7アプリの登録URL更新が終わるまで、本件を全体完了と記載しない。
