# DCC AI Status

DCC AI (`ai.shu-dcc.net`) の稼働状況を5分おきにチェックし、GitHub Pagesで公開するステータスページ。

- チェックはGitHub Actions(`*/5 * * * *`)がGitHub側のランナーで実行するため、監視対象のホストが落ちても監視自体は止まらない
- 結果は `data/history.json` に蓄積され、直近90日分を保持
- 表示は `index.html`(静的ページ、フレームワーク不使用)
