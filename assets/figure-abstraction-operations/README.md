# 単純化の操作を説明する独自図

作成：当リポジトリ、2026-10-02。原典図の転載・トレースではない。人体の実測・参加者データは含まない。説明本文は[操作別比較](../../research/comparisons/figure-abstraction-operations.md)。

| 図 | 意図・設計 |
| --- | --- |
| [量・軸・断面 PNG](mass-axis-section.png) / [SVG](mass-axis-section.svg) | 同じ箱に方向軸を加える操作と、別の円柱に断面を示す操作を分ける。赤い断面は裏側も表示 |
| [向き・接続 PNG](orientation-and-connection.png) / [SVG](orientation-and-connection.svg) | 同じ二箱に対して下側を35度回し、仮の対応点の接続を別段階で示す。帯は筋や皮膚ではない |

操作の背景は、[洞田](../../references/artists/toda-kobun-method.md)第3・7回、[Proko](../../references/videos/proko-robo-bean-and-obliques.md)のLandmarks・Motion・Twist、[Bridgman](../../references/books/bridgman-1920-constructive-anatomy.md)の量と接合。図中の座標軸・断面・帯・寸法・色・比較の順序は当リポジトリの設計で、著者の図や筆順の再現ではない。リクノ固有理論の定義を図解したものでもない。

[生成コード](generate.py)は共通の[幾何学関数](../construction-geometry/generate.py)を使う。カメラ方位30度・仰角18度の平行投影。円柱は48角柱近似。立体値はコードに固定し、人体比率の出典値として使わない。

リポジトリ直下から `python3 assets/figure-abstraction-operations/generate.py`。PNGは `node assets/figure-abstraction-operations/render.cjs`（Nodeとsharpが必要）。sharpを通常の探索先以外に置く場合、第1引数にモジュールの絶対パスを渡す。

2026-10-02、2枚のPNGを表示し、本文との対応、文字の欠け・重なり、面と軸、対応点と接続帯をAIが目視確認した。線の見やすさ・人体としての自然さ・人の理解度の評価はしていない。
