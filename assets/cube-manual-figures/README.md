# 手順書の説明図

2026-10-02。当リポジトリで作成した説明図。外部作品の転載ではない。

[生成コード](make_figures.py)から、SVGと閲覧用PNGを10組作る。[改訂手順書](../../docs/cube-construction-manual.md)と[PDF](../../output/pdf/cube-construction-manual.pdf)で使用する。PDFにはベクターのSVGを入れる。

- workflow：入力から完成までの5工程。
- projection-plane：上から見た視点・画面・立体の点。
- angle-circle：半径80mmの円から30度の成分を読む。
- half-edges：中心からの3本の半辺と、頂点までの加算経路。
- rotation-update：元の値を残して二つの新成分を計算する。
- paper-point：紙の原点から右6.7mm、下60.0mmへ点を打つ。
- ray-p0：作例1のP0を二つの視線図で投影する。
- example-1〜3：既存の研究素材の余白を切り詰めた拡大表示。頂点の座標・接続・可視辺は変更していない。

説明図は模式図。paper-pointとray-p0は見やすさのため軸の表示倍率を変え、そのことを図中に明記した。実際の作図で補助図を縮める場合は全値を同率にする。作例3図は方眼10mm間隔で、閲覧時の表示寸法と実寸は別である。人の作図結果や実測精度を示す資料ではない。

再生成：`python3 assets/cube-manual-figures/make_figures.py`（rsvg-convertが必要）。作例の元SVGは `../cube-projection-research/` から読む。
