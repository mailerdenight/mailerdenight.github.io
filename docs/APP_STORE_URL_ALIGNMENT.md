# App Store URL統一

確認日: 2026-10-10 (JST)

日本のApp Store公開ページから、サポートURL・プライバシーポリシーURL・マーケティングURLを確認しました。公開ページのserialized-server-dataに含まれるサポートURLも確認対象です。

## App Store Connectで更新するURL

以下の7アプリはサポート・プライバシーURLが現行URLと異なります。Apple側の公開済みURLと、次期バージョン下書きに保存したURLは区別して確認してください。ローカライズされた各言語のURLも確認してください。

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

## App Store Connectでの保存結果（2026-10-10 JST）

公開済みバージョンのサポートURL・マーケティングURLは編集不可でした。App Privacy画面にも「プライバシーポリシーを変更するには新しいアプリバージョンを作成」と表示されたため、以下の次期バージョン下書きを作成しました。

| アプリ | 下書きバージョン | 保存した言語数 | 状態 |
|---|---|---:|---|
| 禁欲ログ | 1.2 | 8 | Prepare for Submission |
| 余命予算 | 1.2 | 1 | Prepare for Submission |
| 婚活アポログ | 1.3 | 1 | Prepare for Submission |
| バインミーログ | 1.4 | 9 | Prepare for Submission |
| のりものサウンド | 2.4.2 | 9 | Prepare for Submission |
| どうぶつサウンド | 1.4.2 | 9 | Prepare for Submission |
| レトロドライブ | 1.0.2 | 2 | Prepare for Submission |

計39言語について、サポートURL・マーケティングURL（紹介ページ）・プライバシーポリシーURLを表の正規URLへ保存しました。各アプリの下書きを開き直し、サポート・マーケティングURLの保存値を確認しました。プライバシーURLは保存後の表示を確認し、余命予算は開き直して保存値を確認しました。説明文・課金・データ収集の設定は変更していません。

ビルド未登録、審査未提出、ストア公開未完了です。各下書きバージョンに対応するビルドの登録と審査・リリースが必要です。公開ストアの再取得では6アプリが旧URLのままであることを確認し、婚活アポログは429のため再取得できませんでした。GitHubの旧URL転送は維持してください。未公開のかえる・ことりサウンドは操作していません。
