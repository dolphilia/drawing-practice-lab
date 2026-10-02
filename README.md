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

[立方体の透視作図の研究計画](docs/cube-construction-research-plan.md)：第1〜6段階を完了。[手順書](docs/cube-construction-manual.md)（[改訂PDF・15頁](output/pdf/cube-construction-manual.pdf)）に指定道具による半辺・割算の方法と視線作図を整備し、[総括](research/topics/cube-construction-completion-summary.md)に原典図の照合、36条件、近似の採否、工程の誤差をまとめた。人の実作図・使いやすさ・時間・上達は未確認。

[総合報告書PDF：描く力を育てる練習の設計](output/pdf/drawing-practice-research-review.pdf)では、有望な練習法、新メソッド4候補、人による確認8項目と作業量、出典67件をまとめています。[編集原稿・再生成方法](reports/drawing-research-review/README.md)も保存しています。

- [資料収集・調査計画](docs/research-plan.md)：次に調べる問い、優先順位、検索・精読の手順と完了条件
- [人体の単純化と記憶描画の追加調査計画](docs/research-autonomous-followup-plan.md)：人の実描画・採点・資料提供を待たずに進める原典確認、図解比較、根拠整理、課題仕様の作成
- [根拠整理と教材素材の整備計画](docs/research-evidence-and-tools-plan.md)：6作業の順序・成果物・完了条件と実施状況。根拠台帳、操作別比較、幾何学素材、測定検査、原著精査、読書ガイド
- [疑問から読む描画研究ガイド](docs/drawing-research-reading-guide.md)：厚み・向き・接続・骨筋・記憶・別角度の6つの入口
- [根拠整理と教材素材の総括](research/topics/evidence-and-tools-completion-summary.md)：70主張の整理、操作比較図、12視点の合成素材、測定検査と限界
- [調査計画の継続用プロンプト](docs/research-continuation-prompt.md)：現在の進捗から調査・保存・点検・引き継ぎまで進める指示
- [長期目標用プロンプト](docs/research-long-term-goal-prompt.md)：作業単位を繰り返し、調査計画全体の完了まで進める指示
- [資料一覧](references/README.md)：72件の資料ノートを、主題・根拠の種類・確認範囲で分類
- [調査と分析](research/README.md)：学習科学、既存メソッド、隣接分野、キャラ絵の横断的な整理
- [何時間・何週間で評価できるか](research/learning-science/practice-dose-and-evaluation-timing.md)：研究の実施量と評価時期、探索用の日程案
- [描画の評価候補](research/learning-science/drawing-assessment-candidates.md)：採点法の比較と、実験前に測定の安定性を確かめる案
- [キャラ絵と洞田創のメソッド](research/topics/character-illustration-and-toda-method.md)：広文メソッド／トダ式アタリと検証候補
- [追加調査のわかりやすい総括](research/topics/rikuno-and-master-artists-summary.md)：リクノ、卓越した作家の学習歴、人体の単純化、古典から分かったこと
- [Kim Jung Gi・寺田克也・吉成曜の学習歴](research/topics/master-artists-learning-paths.md)：本人取材と発言の意味、未確認の伝聞との区別
- [人体の抽象化と古典的手法](research/comparisons/figure-abstraction-and-classical-methods.md)：洞田式、Proko、Hampton、Vilppu、Bridgman、記憶描画などの比較

調査・設計フェーズA〜D・Q1〜Q6は[完了監査](research/topics/2026-10-02_research-completion-audit.md)で照合済み。[箱比率の草案](methods/drafts/torso-ratio-quartering.md)、[ドリルv1](exercises/construction/torso-ratio-quartering.md)、[探索的実験計画](experiments/2026-10-02_torso-ratio-pilot.md)、[刺激・描画・採点道具](assets/torso-ratio-pilot/README.md)を準備した。実描画・保持・転移のデータは未取得で、効果は未実証。

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

追加計画の成果：[体幹と記憶描画の総括・点検](research/topics/torso-and-memory-research-summary.md) / [二方法の図解比較](research/comparisons/torso-construction-worked-comparison.md) / [3課題の仕様草案](methods/drafts/torso-observation-memory-task-spec.md)。公開資料での調査・図解・設計を完了し、本文未取得・実践未実施の範囲を分けて記録した。
