# 既知の立体による構築課題素材 v1

2026-10-02、当リポジトリで設計した合成幾何学。人体の標準比率や人の描画結果ではない。[計画W3・W4](../../docs/research-evidence-and-tools-plan.md)と[課題仕様草案](../../methods/drafts/torso-observation-memory-task-spec.md)に対応する。正解とは、このモデルをこのカメラで投影した座標である。

## 使い分け

- A：参照あり。[二箱T1](prompts/two-boxes-T1-A.md)・[箱と円柱T1](prompts/box-cylinder-T1-A.md)。表示されたIDと点を対応付ける。
- B：同じ視点を記憶から再生。[観察画面](prompts/two-boxes-T1-B-observe.md)と[再生指示](prompts/two-boxes-T1-B-recall.md)を分離した。再生が終わった後、同じ観察画面へ戻って照合する。
- C：未提示視点へ構築。[二箱E1](prompts/two-boxes-E1-C.md)・[箱と円柱E1](prompts/box-cylinder-E1-C.md)。出題にはモデル・カメラ条件だけを含め、完成図・解答座標を含めない。

A・Bは各モデルT1〜T3の計6組。CはE1〜E3の計6問。[prompts](prompts/)と[answers](answers/)は別ディレクトリである。フォルダ分離はアクセス制御ではない。出題中は解答フォルダや一覧画像を開かない運用が必要で、閲覧を強制遮断するアプリは作っていない。このREADMEは実施者向けの仕様書で、Cの画面へ完成図を埋め込んでいない。

BはID付きの図を覚える条件。純粋な形の記憶や自由描画の評価とは異なる。時間・反復回数・学習の合格点は設定していない。視点数3+3は素材の制作範囲であり、推奨練習量ではない。

## モデルと視点

[models.json](models.json)に2モデルの全寸法・中心・回転を保存。二箱は上下で寸法・位置・回転が異なる。箱と円柱は円柱底面と箱上面が接し、体積は貫通しない。円柱は半径0.38に内接する**24角柱**で、真円柱の解析輪郭ではない。モデルの正解はこのメッシュで定義する。

[views.json](views.json)が投影と分割の正本。各モデル共通で、T1=(25°,15°)、T2=(115°,25°)、T3=(225°,35°)、E1=(65°,20°)、E2=(155°,30°)、E3=(295°,25°)。括弧は方位角・仰角。全6カメラ条件に重複はない。画像は800×800 px、原点(400,410)、縮尺200 px/単位。

座標は右手系のx右・y上・z前。部品の局所座標をy軸まわりに角度θ回転すると、`x'=cosθ x + sinθ z, y'=y, z'=-sinθ x + cosθ z`。その後、中心位置を加える。

カメラ方位a、仰角eについて、画面右 `r=(cos a,0,-sin a)`、画面上 `u=(-sin e sin a, cos e,-sin e cos a)`、カメラへ向かう単位ベクトル `t=(cos e sin a,sin e,cos e cos a)`。世界点pを `X=400+200(p·r), Y=410-200(p·u), depth=p·t` へ写す。depthが大きい方が手前。角度はJSONでは度、計算ではラジアン。透視除算は行わない。

## ID・輪郭・可視性

箱は局所座標の下側y=-h/2で `0=(-w/2,-d/2),1=(+w/2,-d/2),2=(+w/2,+d/2),3=(-w/2,+d/2)`（組はx,z）。上側y=+h/2の同位置が4〜7。先頭文字は部品IDのL/U/B。

円柱近似は下側0〜23、上側24〜47。円周は局所x-z平面の `x=r cos(2πi/24), z=r sin(2πi/24)`。測定用目印は各層のi=0,6,12,18のみで、Cを付ける。輪郭の端はカメラに応じて変わるため、固定した測定点と一致しない場合がある。画像には可視目印だけをラベル表示し、全頂点・面・可視/不可視の目印と投影座標は各解答JSONに保存する。

可視性は点からカメラ方向への半直線と全メッシュの三角形の交差で判定。自身の表面の距離ゼロは除き、他面が手前にあれば不可視。画像は外向き面の判定と奥行き順描画を使う。今回の12配置では、別方式の画素位置での三角形深度比較で前後の一致を検査した。任意の追加モデルで正しい描画を保証する汎用3Dレンダラーではない。

対称形でもIDは材質点に固定する。ラベルの付け替えを同じ正解にしない。隠れた点は可視点の評価から明示的に外し、同一のID集合を入力する。真横等で軸が潰れる視点は今回含めていない。二次元で重なる点・ほぼゼロ長の軸は測れない条件として除外し、正しい描画の0誤差と混同しない。

## 再生成と点検

リポジトリ直下で、順に実行する。

```bash
python3 assets/construction-geometry/generate.py
python3 assets/construction-geometry/verify_geometry.py
python3 assets/construction-geometry/test_measure.py
node assets/construction-geometry/render.cjs
```

最初の3つはPython 3.8以降の標準ライブラリのみ。PNG変換はNodeとsharpが必要。今回使用したNodeは `/Users/dolphilia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`。同じランタイムの `dependencies/node/node_modules/sharp` をrender.cjsの第1引数へ渡した。依存を自動インストールする処理は含まない。

[manifest](manifest.json)が12素材の対応表。[geometry-checks](geometry-checks.json)は境界・ラベル・出題分離・投影基底・接触・前後の検査結果。[合成入力](synthetic-cases.json)、[測定コード](measure.py)、[検査コード](test_measure.py)、[測定結果](measurement-report.json)は人の記録とは別に保管した。指標の定義と限界は[測定の点検報告](../../research/learning-science/geometric-measurement-checks.md)。

2026-10-02、12枚の一覧PNGと個別画像をAIが表示確認した。初回に下端の余白不足を境界検査で検出し、縮尺と原点を修正してから再生成した。最終の検査数・再現性は[総括](../../research/topics/evidence-and-tools-completion-summary.md)に記録する。学習効果、人の採点との一致、人体への転移は未検証。

解答閲覧用の[12視点一覧](contact-sheet.png)は出題終了後に開く。写真からの人体の唯一の正解を示す資料ではない。

全成果の再生成監査は `python3 assets/construction-geometry/audit_artifacts.py --regenerate`。Nodeとsharpの場所を指定する場合は `--node` と `--sharp` を使う。引数なしでは文書・素材の存在等を点検し、再生成したとは記録しない。監査結果JSONは直近の実行で上書きされる。
