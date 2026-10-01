---
title: "第3回計画調査：意図的練習の訂正・定義・選別"
status: ready
tags: [research-log, expertise, deliberate-practice]
related: [../../docs/research-plan.md, ../learning-science/deliberate-practice-definitions.md]
created: 2026-10-01
updated: 2026-10-01
---

# 第3回計画調査：意図的練習の訂正・定義・選別

## 開始前の計画

- 計画書：A4。Q2の必要時間の解釈と、Q3の練習の定義を点検。
- 起点：Macnamara 2014の訂正、Ericsson & Harwell 2019。
- 判断したいこと：何が訂正され、定義・選別・計算の違いが何を変えるか。
- 範囲：Web検索、出版社・大学公開版・PMC。日英、発行年による除外なし、件数上限なし。原著全件の再解析・二重選別は行わない。
- 終了条件：2件の確認または保留理由を残し、批判も調べて分析・計画・索引へ反映。

## 実際の検索

すべて2026-10-01。Web検索の関連度順の返却結果・抜粋を確認して主要候補へ進んだ。総ヒット数は取得しておらず、全件検索・選別ではない。

| ID | 実際の検索式 | 返却範囲での確認・制限 |
| --- | --- | --- |
| S01 | `"0956797618769891" correction` | 出版社の訂正と大学公開PDFを発見 |
| S02 | `"Ericsson" "Harwell" "2019" deliberate practice original definition` | 原著、批判的レビュー、関連応答と二次解説を選別 |
| S03 | `意図的練習 Macnamara Ericsson メタ分析 定義 訂正` | 日本語解説・関連研究候補。数値は原著・訂正へ戻って確認 |
| S04 | `"deliberate practice" "Harwell" correction replication 2021 2022 2023 2024 2025 2026` | 更新探索。年号は検索語であり厳密な発行年フィルタではない。後続候補は精読保留 |

直接閲覧：既存DOI・PMCから出版社本文へ移動。Macnamaraの出版社ページは要旨・書誌中心のため、S01のPurdue大学公開PDFでMethod等を確認。Ericsson 2019のPMCと関連応答のPMCは認証画面になり、2019はFrontiers本文で確認できた。ページ内検索で `Original Definition`、`attenuation`、`reanalysis`、`Inclusion criteria`、`88 studies` 等を探し、該当箇所の前後を読んだ。引用・被引用候補はS02/S04と原著の文献を入口に辿った。

## 候補と選別

| 候補 | 経路 | 判定・理由・次の確認 |
| --- | --- | --- |
| [Macnamara 2014と2018年訂正](../../references/articles/macnamara-2014-deliberate-practice.md) | 既存・S01 | 既存更新。原著の選別と訂正の主モデルを確認。訂正は別件加算しない |
| [Ericsson & Harwell 2019](../../references/articles/ericsson-2019-practice-definition.md) | 既存・S02 | 既存更新。定義・選別と補正の前提を本文確認 |
| [Hambrickほか2020](../../references/articles/hambrick-2020-deliberate-practice-critique.md) | S02/S04 | 新規採用。再分析への批判と感度分析。独立した介入研究とは数えない |
| [定義の不変性を主張するEricssonの関連応答](https://pmc.ncbi.nlm.nih.gov/articles/PMC8049893/) | S02/S04 | 検索抜粋のみ・保留。別のMacnamara & Hambrick論評への応答で、新規採用したHambrickほか2020への直接の返答と混同しない。出版社・著者版から本文を確認する |
| [Macnamara & Maitraの音楽研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC6731745/) | S04 | 追試候補・保留。検索抜粋のみ。方法変更・対象・結果・批判を確認してから独立データとして扱う |
| [個別化を扱う後続研究](https://doi.org/10.1007/s12144-021-02326-x) | S04 | 更新候補・保留。検索抜粋のみ。題名の主張を結論に採用せず、課題と実証部分を精読する |
| [2021年の熟達研究特集への導入](https://www.journalofexpertise.org/articles/volume4_issue2/JoE_4_2_Harris_Eccles_Intro.pdf) | S04 | 更新探索の入口として保留。特集の各論文は未取得 |
| 日本語ブログ、教師向け解説、Agents Wiki、Wikipedia、Reddit等 | S02〜S04 | 今回の根拠から除外。一次資料の所在探索以外に使用せず、各サイト全体の信頼性判定はしない |
| 同一論文のPMC・出版社・大学PDF | 各経路 | 重複統合。独立した支持研究として加算しない |

主要候補の表で、全検索結果の網羅表ではない。反証探索は `correction`、`replication` と発見した批判・応答を追う範囲。`null` 等の追加検索、学術索引の全被引用追跡は未実施。

## 精読と抽出

| 資料 | 確認箇所 | 残る未確認事項 |
| --- | --- | --- |
| Macnamara | 大学PDFの原著pp.1608–1612（Introduction、Method、Results冒頭）、出版社の訂正本文・Table 1 | 付録・公開データ、全原著の重複と採否の検証 |
| Ericsson & Harwell | 出版社HTMLのOriginal Definition、選別3基準、Reanalysis、Attenuation | S1/S2、図版、全原著を用いた再分類 |
| Hambrickほか | PMC本文の2019年再分析への批判、信頼性の記述とTable 3の統合区分 | 歴史的な定義の全引用照合、表2の全件検証 |

数値は主モデルか部分集約か、補正前か後かを区別した。特にHambrickの統合区分とdeliberateのみの数値は別の分母として点検。原著データの再計算は行っていない。研究で観測した相関と、当リポジトリで実施した練習結果を混同しない。

## 主張ごとの判断

- 訂正の内容は確認できた。数式訂正と採否への批判を分けて引用する。
- 定義と選別・測定の前提を揃えずに、集約された割合を比較しない。
- 描画への直接的な有効性や必要最小時間は判断できない。
- [横断分析](../learning-science/deliberate-practice-definitions.md)では、課題選択・修正情報・実施量・評価の対応を記録する案へつなげた。

## 終了記録

- 状態：A4の初回点検を一巡。段階A全体は未完了。A5・実験は未着手。
- 範囲変更：反論を一方だけの説明にしないため、批判的レビュー1件を追加。後続候補は精読せず保留先を残した。
- 作業時間：2026-10-01 22:24:51–22:32:22 JST、経過7分31秒（約7.5分）。検索・執筆・点検・外部応答待ちを含む。この時間記録の追記・最終報告は含めず、参加者の練習時間とは区別する。
- 成果：既存資料2件更新、新規1件追加で計39件。新規分析1件・本収集記録を含め分析と記録12件。学習原理・計画書・索引を更新。
- 結論を変え得る情報：採否の全件照合、信頼性の実測、目標に近い描画課題の比較研究、独立追試。
- 次の判断：追加調査。次回はA5の洞田創の講座の所在・本文・図版・手順の前提と例外を点検する。A4の保留は各候補の本文・補足資料が確認できたとき再開する。

## 保存後の点検

フロントマター60件を解析し、資料39件の索引収録・主要出典URLの重複と、内部リンク362件を確認した。エラーなし。`git diff --check` も通過。重要な数値は出典の集約区分・信頼性仮定と照合し、未確認の補足資料・追試は保留表示を維持した。既存の未コミット変更を保全し、コミットは行っていない。
