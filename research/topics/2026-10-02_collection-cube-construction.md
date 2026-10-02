---
title: "立方体の透視作図に関する初期収集記録"
status: ready
tags: [perspective, construction, source-audit]
related: [cube-construction-feasibility.md, ../../docs/cube-construction-research-plan.md]
created: 2026-10-02
updated: 2026-10-02
---

# 立方体の透視作図に関する初期収集記録

## 調査の目的

ユーザー指定の道具で立方体をさまざまな視点から作図するため、基準法・簡略化・近似の候補を選び、継続可能な計画を作る。網羅的な文献レビューや手法の確立を、この初回だけで完了したとは扱わない。

## 実施した検索

2026-10-02、Web検索で次の6式を使用した。

1. `site.gutenberg.org perspective Storey measuring points distance cube`
2. `site.math.utah.edu perspective cube three point drawing`
3. `site.nptel.ac.in perspective projection visual rays method cube`
4. `site.edu perspective drawing inaccessible vanishing point measuring point cube`
5. `site.ac.jp 透視図 測点法 立方体 三点透視 図学`
6. `site.nptel.ac.in "Perspective Projections" "Vanishing" cube`

検索結果から原典を開き、関連する本文に絞って確認した。検索抽出と原典本文を混同しない。

## 採用した資料ノート

| 資料 | 採用理由 | 残る確認 |
| --- | --- | --- |
| [Storey](../../references/books/storey-1910-perspective-measuring-points.md) | 測点と紙外の距離点 | 図の精査、同条件での再作図 |
| [Ruskin](../../references/books/ruskin-elements-perspective-point-construction.md) | 点から線へ作る構成 | 収録版の刊年、図と任意姿勢への対応 |
| [Treibergs](../../references/articles/treibergs-perspective-geometry.md) | 数式・幾何・測点を結ぶ大学教材 | 画像式・全図・コードは未精査 |
| [Illinois大学教材](../../references/articles/illinois-recipe-for-cube.md) | 三点透視の立方体に直接関係 | 図、当該ページの著者署名、全手順の再現 |
| [石川](../../references/articles/ishikawa-2015-cube-perspective.md) | 同じ問題を扱う日本語の論考 | 図と投影モデルの照合 |

計5ノートを追加した。同じサイトの別URL、同じ資料の別表示を独立の証拠として数えない。資料ノート総数は67件から72件。今回追加の内訳は方法論1件、実践教材4件であり、学習効果の研究を5件追加した意味ではない。

## 取得保留と見送り

- [NPTEL Lecture 40のVisual Ray Method](https://archive.nptel.ac.in/content/storage2/courses/112103019/module4/lec40/3.html)は検索抽出で平面図・立面図等から視線を扱う説明が得られたが、原典を開くと認証画面へ転送された。隣接する `/2.html` も試した。ログイン・認証回避は行わず、本文確認済みの基準資料には採用しなかった。正規公開の本文が得られる場合に再開する。
- 石川PDFは本文抽出には成功したが、ページ画像0・1・4の取得がキャッシュエラーで失敗した。本文中の手順と図の説明は読めるが、図版の確認済みとはしない。第3段階で原典の画像を取得できた場合に再開する。
- Illinois教材の親ディレクトリ取得は失敗した。子ページ本文は取得できた。著者名をURLの文字列から推定して埋めなかった。
- 検索に現れた掲示板・一般まとめは、技術的な結論の根拠として採用しなかった。
- 岡山県立大学、武蔵野美術大学、金沢美術工芸大学の関連PDFは候補として検索結果に現れたが、今回は本文を開いていない。第3段階で未解決の作図操作に必要なら読む。取得・精読済み一覧には含めない。

## 今回実施した検算

[probe.py](../../assets/cube-projection-research/probe.py)で、有理数の回転を使う1例の8頂点と12辺を検査した。さらに近似縮尺の誤差関係を3範囲×201入力＝603入力で確認した。[結果JSON](../../assets/cube-projection-research/probe-results.json)を保存。

確認したのは式の整合と限定的な実装である。任意角度の人力設定、消失点・測点の図解、工程の読み取り誤差、実作図は未実施。これらを今後の段階へ残した。

## 今回の成果と次の入口

[初期調査](cube-construction-feasibility.md)と[研究計画書](../../docs/cube-construction-research-plan.md)を作成した。次回は共通の入力仕様、基本24条件・境界12条件、独立に照合できる基準投影を準備する。既存の人体・記憶描画の完了監査やPDF報告書は、当時の資料範囲の記録として保持した。
