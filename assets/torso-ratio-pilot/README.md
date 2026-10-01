---
title: "上下箱比率の試行素材 v1"
status: ready
tags: [construction, evaluation]
related: []
created: 2026-10-02
updated: 2026-10-02
---

# 上下箱比率の試行素材 v1

## 開くもの

[描画画面](draw.html)を通常のブラウザで直接開く。参照図を選ぶ→試行ID入力→4分開始→PNG保存→保存を確認して全消去、の順。採点時だけ[6点採点画面](score.html)を開き、PNG読込→6点クリックまたは欠測理由→CSV保存。[探索計画](../../experiments/2026-10-02_torso-ratio-pilot.md)が条件・日程・判定の正本。

保存はブラウザのダウンロード先へ行う。開始前の線・丸による装置確認でPNG/CSVが保存できることを確かめ、ブラウザ名・版・表示配置をログに記す。外部通信・自動保存なし。ファイルを閉じると未保存描画は消える。

## 刺激と記録

[stimuli.json](stimuli.json)が座標・寸法の正本。SVGは全て当リポジトリの自作線図（800×600px）で原教材の図版の複製ではない。全12図は上下比0.75。標準と練習2図は同じ上高さで幅を変える。近い転移9図は各3図の大きさをそろえ、pre/post/retentionで位置を変える。単なる配置変化の近い転移であり、立体・人体・比率変更の転移ではない。

| 役割 | 素材 |
| --- | --- |
| 標準 | [standard.svg](standard.svg) |
| 練習 | [幅広](practice-wide.svg)、[幅狭](practice-narrow.svg) |
| 近い転移pre | [1](near-pre-1.svg)、[2](near-pre-2.svg)、[3](near-pre-3.svg) |
| 近い転移post | [1](near-post-1.svg)、[2](near-post-2.svg)、[3](near-post-3.svg) |
| 近い転移7日 | [1](near-retention-1.svg)、[2](near-retention-2.svg)、[3](near-retention-3.svg) |
| 算式 | [measurement.js](measurement.js)（自動端点検出なし） |
| 入力雛形 | [実施ログ](session-log.csv)、[匿名対応キー](blind-key.csv)、[集計](summary.csv) |

ローカル限定の実描画PNGはGit管理外の`images/experiments/torso-ratio-pilot/`へ。共有が必要になった実画像のみ画像方針に従い別途扱う。ここには自作刺激と空の雛形だけを置く。

## 匿名化

[blind.py](blind.py)をPython 3で実行：`python3 assets/torso-ratio-pilot/blind.py 入力PNGフォルダ 新しい出力フォルダ`。同じ画像セットで採点回ごとに新しい出力先を使う。コピーをランダム順の`image-NNN.png`へ変え、対応キーを出力先の外側に保存する。既存出力へ上書きしない。キーを閉じ、順番に採点する。2回分をキーで元画像へ対応させ差を取る。自己採点では記憶を消せず、完全盲検とは呼ばない。

## 点検の範囲

[合成入力の検証コード](verify.cjs)を`node assets/torso-ratio-pilot/verify.cjs`で実行できる。素材の座標・算式・入力状態は合成値で点検した。これは人の作画、採点一致、妥当性、学習効果の検証ではない。道具の入力・保存動作の確認は[最終監査](../../research/topics/2026-10-02_research-completion-audit.md)へ記録する。
