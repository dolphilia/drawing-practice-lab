# drawing-practice-lab

イラストの練習方法に関する資料を集めて分析し、独自のお絵描きメソッドや練習方法を開発・確立するためのリポジトリです。

## はじめ方

まずは **資料メモ1件・ドリル1件・練習日誌1件** から始めます。全種類の文書をそろえる必要はありません。

1. [テンプレート一覧](templates/README.md)から必要な雛形をコピーし、保存先に合わせて名前・日付・リンクを直す
2. 資料を読む場合は、出典と該当箇所、試したいことを残す
3. ドリルを実行し、日誌に「何分・何をした・何が分かった・次に何をする」を残す
4. 効果を比較したくなったら、[評価・検証ガイド](docs/evaluation.md)に沿って実験を計画する

`skills/` は描画技能の分類です。AI エージェント用のスキルを置く場所ではありません。

## 調査資料を読む

- [資料収集・調査計画](docs/research-plan.md)：次に調べる問い、優先順位、検索・精読の手順と完了条件
- [調査計画の継続用プロンプト](docs/research-continuation-prompt.md)：現在の進捗から調査・保存・点検・引き継ぎまで進める指示
- [長期目標用プロンプト](docs/research-long-term-goal-prompt.md)：作業単位を繰り返し、調査計画全体の完了まで進める指示
- [資料一覧](references/README.md)：39件の出典を、主題・根拠の種類・確認範囲で分類
- [調査と分析](research/README.md)：学習科学、既存メソッド、隣接分野、キャラ絵の横断的な整理
- [何時間・何週間で評価できるか](research/learning-science/practice-dose-and-evaluation-timing.md)：研究の実施量と評価時期、探索用の日程案
- [描画の評価候補](research/learning-science/drawing-assessment-candidates.md)：採点法の比較と、実験前に測定の安定性を確かめる案
- [キャラ絵と洞田創のメソッド](research/topics/character-illustration-and-toda-method.md)：広文メソッド／トダ式アタリと検証候補

資料の信頼性は [評価・分類方針](docs/evidence-policy.md)に従って記録します。研究が直接示したこと、実践者の経験則、このリポジトリで試す仮説を分けています。

## ワークフロー

```text
references → research → methods → exercises → programs
                           ↑          │           │
                           │          └─────┬─────┘
                           │                ↓
                           └── experiments ← logs
```

1. **集める**：外部資料の出典・要点を `references/` に記録する
2. **分析する**：資料をまたいだ考察を `research/` にまとめる
3. **作る**：仮説としてのメソッドを `methods/drafts/` に書く
4. **具体化する**：実行可能なドリルを `exercises/` に置く
5. **続ける**：必要なら `programs/` で練習を組み合わせ、`logs/` に実施内容を残す
6. **試す**：比較したい仮説について `experiments/` に事前計画・結果・考察を記録する
7. **採用・見直しする**：条件と限界を確認したメソッドを `methods/stable/` に移し、反証が出たら再検証する

日誌からドリルを考えたり、既存の練習法を直接試したりしても構いません。`stable` は本リポジトリ内での採用判断であり、万人への効果を保証する意味ではありません。

## ディレクトリ構成

| ディレクトリ | 役割 |
| --- | --- |
| `docs/` | 運用ルール・評価ガイド・用語集 |
| `references/` | 外部資料の要約・メモ（資料の主張と自分の解釈を分ける） |
| `research/` | 複数資料をまたいだ分析・比較（自分の解釈） |
| `skills/` | 身につけるスキルの体系と地図 |
| `methods/` | 原理・適用条件・根拠（`drafts` / `stable` / `archived`） |
| `exercises/` | 実行できる練習ドリル（`skills/` と同じ分類） |
| `programs/` | ドリルを組み合わせたカリキュラム |
| `experiments/` | メソッドの検証計画・結果 |
| `logs/` | 日々の練習記録 |
| `templates/` | 各種ドキュメントのテンプレート |
| `assets/` | 追跡対象の共通素材。共有する比較画像は `assets/evidence/` |
| `images/` | ローカルの練習画像など（**Git 管理外**） |

## 運用ガイド

- [運用ルール](docs/conventions.md)：命名・状態・リンク・版管理
- [評価・検証ガイド](docs/evaluation.md)：比較条件・保持・転移・採用基準
- [資料の評価・分類方針](docs/evidence-policy.md)：根拠の種類・対象分野・確認範囲
- [テンプレート一覧](templates/README.md)：保存先と最小限の記入項目
- [スキルマップ](skills/skill-map.md) / [用語集](docs/glossary.md)
- [画像の保存方針](images/README.md)：ローカル画像と共有用素材
- [初期構成のレビュー](docs/structure-review.md)：改善理由と調査資料
