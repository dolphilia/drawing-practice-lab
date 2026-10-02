# 描く力を育てる練習の設計

2026年10月2日時点の調査を、人が通読できる形にまとめた総合報告書です。

[完成PDF（A4・29ページ）](../../output/pdf/drawing-practice-research-review.pdf)には、有望な練習の原則、新メソッド候補4案、人による確認8項目、既存の試行計画の作業量、出典67件を収録しています。実践者の経験、研究結果、このリポジトリの仮説、自動検査、人に対する効果の確認を区別しました。メソッドの効果は未実証です。

## 読む順序

- まず第1章で結論をつかみ、第2章で有望な練習の考え方を読む。
- 新メソッドの具体像は第6章、人が行う確認と予定作業量は第8章を読む。
- 根拠と限界は第3〜5章、自動検査の意味は第7章、開発の順序は第9章で確認する。
- 第10章の用語・資料案内と巻末の出典から、元の資料へ戻る。

8項目は人数や独立した実験数ではありません。作業量を数えたのは既存の箱比率計画だけで、固定時間310分・描画67枚に加え、評価採点54画像回と記録等の時間が必要です。開始日・追加作業時間は未定で、最終の再採点まで最短で約40日となる予定です。推奨される最低練習量を示す数値ではありません。

## 保存したファイル

| ファイル | 用途 |
| --- | --- |
| [manuscript.md](manuscript.md) | 編集する本文。出典は資料ノートのスラッグで指定 |
| [print.css](print.css) | 明朝体の本文、ゴシック体の見出し、表・図・改ページ |
| [build.py](build.py) | 出典一覧・目次を生成し、Pandocと印刷処理を起動 |
| [print-pdf.mjs](print-pdf.mjs) | Playwright ChromiumによるPDF生成とブラウザ上の検査 |
| [page-map.py](page-map.py) | PDFのリンク先から実際のページ番号を取得 |
| [verify.py](verify.py) | PDF内の文字・ページ・リンク・項目数等を点検 |
| [sources.json](sources.json) | 作成時の資料ノート67件のメタデータ。本文で引用したノートは38件 |
| [browser-checks.json](browser-checks.json) | 画像、表の横あふれ、リンク先、目次ページの検査記録 |
| [quality-checks.json](quality-checks.json) | PDFのハッシュと機械検査結果 |
| [visual-review.json](visual-review.json) | そのPDFを画像化して目視した結果 |

## PDFの作り方

ユーザー指定の `../reml` にあるプログラミング本・コンパイラ本の生成方式を参照しています。参照先は `books/README.md`、各書籍のREADME、`scripts/books/pdf.mjs`、`scripts/books/print-pdf.mjs`、`scripts/books/print.css` です。`../reml` 自体は変更していません。

共通する処理は **Markdown → Pandocの単独HTML → 印刷用CSS → Playwright Chromium → A4 PDF** です。明朝体とゴシック体、フォント・画像の読み込み待ち、表の幅の検査、ヘッダー・フッター、しおり・タグを用います。この報告書ではさらに、初回のPDFから目次のページ番号を取得し、再出力後に番号が変わっていないことを確認します。印刷時のHTTP/HTTPSアクセスは遮断し、図はローカルの独自作成素材を使います。

リポジトリのルートから、pypdfを利用できるPythonで次を実行します。

```bash
python3 reports/drawing-research-review/build.py
python3 reports/drawing-research-review/verify.py
```

必要なものは Pandoc、Python（pypdf・pdfplumber）、Node.js、Playwright、Chromium、日本語フォントです。今回の環境では既存のCodex同梱ランタイムとインストール済みPandoc・Chromiumを使用しました。新しいパッケージはインストールしていません。

この環境でのPythonは `/Users/dolphilia/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` です。`DRAWING_NODE`、`DRAWING_PYTHON`、`DRAWING_CHROMIUM_EXECUTABLE`、`PANDOC` で実行ファイルを指定できます。Playwrightの読み込み先は `print-pdf.mjs` でCodex同梱場所を指定しているため、別の環境ではその箇所も調整してください。フォントが変わると改ページも変わるので、再生成後の目視点検が必要です。

再生成の出典範囲は `sources.json` に記録した67件に固定します。その後の立方体研究等で増えた資料ノートを、過去の報告書へ自動的に追加しません。報告書の範囲を改訂する場合は、本文・出典リスト・検査条件を一緒に改訂してください。

中間HTMLは `tmp/pdfs/drawing-research-review/` に生成されます。完成PDFは `output/pdf/drawing-practice-research-review.pdf` に出力されます。再生成時は同名のファイルを置き換えます。

## 点検と限界

全29ページをPNG化して目視し、改ページ・表の幅・文字の欠け・図・出典欄を確認しました。本文・図・出典の代表ページは拡大して確認しています。最終修正は16〜17ページだけで、他27ページの画像が前回の点検時と同一であることも照合しました。目次の実ページ、画像3点、内部リンク64件、外部リンク67件、A4サイズ、出典番号、本文中の候補4案・確認8項目を機械検査しました。外部リンク数はPDF内のリンクの存在を表し、すべての公開先の現在の応答を保証するものではありません。

機械検査の再実行でPDFのハッシュが変わっていれば、以前の目視点検は引き継ぎません。PDFを再びPNG化し、全ページを確認して `visual-review.json` を更新してください。PDFの見た目の点検は、学習者による読みやすさの調査・実描画・効果の検証とは異なります。

本文は既存の資料ノートと調査文書の再整理です。今回新たに系統的レビューを実施したものではありません。フィードバックのメタ分析は公開元本文を再確認しました。一方、空間訓練と描画研究の一部は今回の取得時に本文が得られず、既存の確認記録の範囲を引き継いでいます。各資料の確認範囲を巻末に明記し、未取得部分や著者の主張を独自に補っていません。
