# 箱から面頭部を作る説明用模型

2026-10-05。[調査](../../research/topics/head-construction-and-free-models.md)と[手順草案](../../methods/drafts/box-to-planar-head.md)の図解用に独自生成した模型。

- [OBJ模型](schematic-planar-head.obj)：148頂点、134多角形面。頭部と左右の耳はそれぞれ閉じた別体で、耳は頭に接続して溶接されていない。3D印刷用の一体メッシュではない。
- [生成コード](make_model.py)：Python標準ライブラリのみ。
- [4段階の座標データ](model-data.json)：箱、頭蓋・顎、眼窩・鼻、口・耳の形を同じ頂点対応で収録。

```bash
python3 assets/head-construction/make_model.py
```

コードは辺の隣接面数、頂点番号、有限座標を点検する。これが確認するのは生成データの基本構造で、顔の解剖学的正確さや元模型への一致率ではない。多角形面の中には非共面の四角形があるため、インポート時の三角形分割で陰影が少し変わる場合がある。平滑化前の粗い形の練習用。

参考に選んだ模型：[Loomis Head - Planes (3D Print Ready)](https://sketchfab.com/3d-models/loomis-head-planes-3d-print-ready-fdd295e9075647a7a07f689147fac31b)、cgmonkey、配布表示CC BY 4.0。今回作成したファイルはそのメッシュを取得・改変したものではない。立体を箱・面・くさびで説明するための独自模式図で、比率は仮の出発値。元模型の寸法・全形状を再現した成果とは扱わない。
