# 立方体の透視作図：計算・図版・点検資料

2026-10-02。当リポジトリによる独自の導出・合成入力・模擬検査。人の作図記録や、使いやすさ・学習効果の実証ではありません。

まず[手順書](../../docs/cube-construction-manual.md)、[記入済みの3例](worked-examples.md)、[空の作業表](blank-worksheet.md)を参照してください。研究上の判断は[総括と完了監査](../../research/topics/cube-construction-completion-summary.md)にまとめています。

## ファイルの役割

| ファイル | 内容 |
| --- | --- |
| [geometry.py](geometry.py) | 入力検査、逐次回転、独立した世界座標基準、視線作図、測点作図、誤差指標 |
| [make_cases.py](make_cases.py) / [cases.json](cases.json) | 基本24・境界12条件の生成と固定入力 |
| [test_geometry.py](test_geometry.py) | 13項目の自動検査。一般姿勢200例、退化・不正入力・省力化の条件も含む |
| [evaluate.py](evaluate.py) | 正確な方法、近似、工程別の仮想誤差を比較 |
| [reference-results.json](reference-results.json) | 正解の8頂点、用紙内外・拒否の判定 |
| [comparison-results.json](comparison-results.json) | 方法別の誤差、手数、補助図の倍率 |
| [sensitivity-results.json](sensitivity-results.json) | 操作の誤差ゼロと仮想誤差の全結果 |
| [evaluation-summary.json](evaluation-summary.json) | 有限34・拒否2、最大不一致、37,162回の模擬検査、精度別件数 |
| [supplement.py](supplement.py) / [supplement-results.json](supplement-results.json) | 任意角度100条件の丸めと5度刻みの比較 |
| [source_model_check.py](source_model_check.py) / [source-model-check.json](source-model-check.json) | 石川図4を指定画面への中心投影と比較した独自の数値例 |
| [source-inspection.json](source-inspection.json) | 原典の図・PDFの取得URLとハッシュ。外部画像本体は転載しない |
| [make_materials.py](make_materials.py) | 独自SVG、記入例、空の作業表の生成 |
| [write_results_docs.py](write_results_docs.py) | 比較結果と感度検査の本文・数表の生成 |
| [run_all.py](run_all.py) | 上記の計算・検査・生成とPNG変換を順に実行 |
| [verification.json](verification.json) | 最終点検の実行結果、成果物のハッシュ、図版確認範囲 |
| [probe.py](probe.py) / [probe-results.json](probe-results.json) | 初期調査時の1条件と603入力の有理数検算。履歴として保持 |

## 再生成

リポジトリのルートで実行します。数値計算はPython標準ライブラリのみを使用します。図のPNG化には `rsvg-convert` が必要です。別の場所にある場合は環境変数 `RSVG_CONVERT` で指定できます。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 assets/cube-projection-research/run_all.py
```

数値・生成文書・図版は上書きされます。数値の自動検査が通っても、新たに図を変更した場合の見た目の確認は別に必要です。自動検査だけなら次を実行します。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 assets/cube-projection-research/test_geometry.py
```

## 独自の図版

| 図 | SVG | 閲覧PNG |
| --- | --- | --- |
| 正面・一点 | [D1-2-1.svg](D1-2-1.svg) | [D1-2-1.png](D1-2-1.png) |
| 左右回転・二点 | [D2-2-1.svg](D2-2-1.svg) | [D2-2-1.png](D2-2-1.png) |
| 俯瞰・三点 | [D3-2-0.svg](D3-2-0.svg) | [D3-2-0.png](D3-2-0.png) |
| 二つの視線補助図 | [ray-charts.svg](ray-charts.svg) | [ray-charts.png](ray-charts.png) |
| 測点による一辺 | [measuring-point.svg](measuring-point.svg) | [measuring-point.png](measuring-point.png) |

画像の画面上の表示寸法は実寸を保証しません。人が描く際は作業表のmm値を使います。コンピューターは研究側の答え合わせに使い、提案手順の実行にプログラム・関数電卓・自動生成座標を必須としていません。
