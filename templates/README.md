# テンプレートの使い方

必要なものだけコピーします。全項目を一度に埋める必要はありません。空欄を残す場合、未確認・未実施・対象外のどれかが分かるように書きます。

| 雛形 | 保存先 | 最初に埋める項目 |
| --- | --- | --- |
| [reference.md](reference.md) | `references/{books,videos,articles,artists}/` | 出典、確認範囲、要点、該当箇所 |
| [collection.md](collection.md) | `research/topics/YYYY-MM-DD_collection-<theme>.md` | 問い、検索計画、実行した検索、候補の採否・保留理由 |
| [research.md](research.md) | `research/{topics,comparisons,learning-science}/` | 問い、資料、自分の仮説 |
| [skill.md](skill.md) | `skills/{fundamentals,figure,composition,rendering}/` | 定義、観察できる到達基準 |
| [method.md](method.md) | `methods/drafts/` | 課題、対象、原理の仮説、根拠 |
| [exercise.md](exercise.md) | `exercises/{fundamentals,figure,composition,rendering}/` | 目的、時間、手順、振り返り方 |
| [program.md](program.md) | `programs/` | 目標、頻度、ドリル、見直し時期 |
| [experiment.md](experiment.md) | `experiments/YYYY-MM-DD_name.md` | 開始前に仮説・条件・評価・判定基準 |
| [log.md](log.md) | `logs/YYYY/YYYY-MM-DD.md` | 時間、実施内容、気づき、次回 |

1. コピー先のフォルダを選び、内容が分かる名前を付ける。
2. タイトル、日付、必要なフロントマターを記入する。状態は [運用ルール](../docs/conventions.md)に従う。
3. パスは**コピー先ファイルから**の相対パスに直す。該当する文書ができたら本文にもリンクを付ける。
4. `null`、`[]`、空欄は未記入。結果がない段階で成功例として埋めない。

日誌の「任意」項目は使わなければ削除できます。実験の事前計画は開始時点で保存し、変更時には元の計画と変更理由を残してください。
