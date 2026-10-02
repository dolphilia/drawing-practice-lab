# 立方体の透視作図・改訂手順書

2026-10-02改訂。[本文](../../docs/cube-construction-manual.md)を、[A4・15ページのPDF](../../output/pdf/cube-construction-manual.pdf)へ出力した。

数値・計算式・3作例の24頂点の値を保ち、座標の意味、半辺、回転の前後、点を紙へ写す操作を説明する図を追加した。掲載図は10点（新規説明図7点、既存作例の拡大表示3点）。補助図は模式図であること、図の表示倍率とmm値の違いを明記した。数値検査は人の使いやすさ・上達の実証ではない。

## 生成方法

ユーザー指定の `../reml/scripts/books/pdf.mjs` と `print-pdf.mjs` を参照し、**Markdown → Pandoc HTML → 印刷用CSS → Playwright Chromium → PDF** の方式を使用した。`../reml` は変更していない。本文は明朝、見出しはゴシック。画像はSVGで読み込み、フォントと画像の読み込み完了後に印刷する。ヘッダー、ページ番号、しおり、タグ付きPDFを出力する。印刷中のHTTP/HTTPSリクエストは遮断する。

リポジトリのルートで実行する。

```bash
python3 assets/cube-manual-figures/make_figures.py
python3 reports/cube-construction-manual/build.py
PYTHONDONTWRITEBYTECODE=1 python3 reports/cube-construction-manual/verify.py
```

必要なもの：Pandoc、rsvg-convert、Node.js、Playwright、Chromium、日本語フォント、Python（検査にはpypdf・pdfplumber）。既存の環境を使い、追加インストールはしていない。`PANDOC`、`DRAWING_NODE`、`REML_PLAYWRIGHT_PACKAGE`、`REML_CHROMIUM_EXECUTABLE`で実行先を指定できる。この環境の検査用Pythonは `/Users/dolphilia/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`。

Chromiumは通常の実行制限下では起動できなかったため、ローカル文書を印刷する実行権限で生成した。原稿・画像の外部送信は行っていない。

## 点検記録

- [browser-checks.json](browser-checks.json)：画像10点の読み込み、横あふれと内部リンクの欠落なし。
- [quality-checks.json](quality-checks.json)：A4・15頁、24頂点の数値照合、ページ外文字・文字置換・ほぼ空白の頁なし、本文と図のハッシュ。
- [visual-review.json](visual-review.json)：最終PDFのハッシュ、全頁の表示確認。最終修正した6頁を再確認し、他9頁は前回画像と同一であることを照合した。

PDF解析器は一部フォントのFontBBox取得について警告を出したが、文字抽出と検査は完了した。文字境界の自動検査だけに依存せず、Popplerで画像化した全頁の表示も確認した。

再生成した場合はPDFのハッシュと図のレイアウトが変わり得る。過去の目視確認を引き継がず、再度画像化して点検する。中間ファイルは `tmp/pdfs/cube-construction-manual/` に生成され、検査用画像は納品前に削除する。本文末のローカル資料リンクは、このリポジトリのファイルがある環境で利用する。
