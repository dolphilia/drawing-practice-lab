# 新メソッド候補の図解別冊

総合報告書の第6章で挙げた M1〜M4 を、目的・具体的な操作・結果の読み方から説明し直した別冊。2026-10-03。

- [PDF](../../output/pdf/new-method-candidates-explained.pdf)：11ページ、説明図8点。
- [編集原稿](manuscript.md)：日常的な言葉による説明、作図、数値例、候補の使い分け。
- [図と生成コード](../../assets/new-method-candidates/README.md)：独自の説明図。実描画データではない。
- [機械点検](quality-checks.json)・[全ページの目視点検](visual-review.json)：対象PDFのハッシュと点検範囲。

既存の報告書と正式な実験仕様は変更していない。M3・M4の小手順は、未整備だった案を説明するために今回具体化した提案。学習効果、実施しやすさ、最適な練習量は未検証。新たな外部文献の調査は行わず、原稿末尾の保存資料へ根拠をたどれるようにした。

## 再生成

`../reml` のプログラミング本・コンパイラ本と同系統の Markdown → Pandoc HTML → 印刷CSS → Playwright Chromium で作る。PDFにはSVGを使い、MarkdownのプレビューにはPNGを使う。ネットワーク上の画像・フォントは読み込まない。

リポジトリのルートで実行する。

```sh
python3 assets/new-method-candidates/make_figures.py
python3 reports/new-method-candidates/build.py
/Users/dolphilia/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 reports/new-method-candidates/verify.py
```

必要なものは Pandoc、`rsvg-convert`、Playwright と既存の Chromium、日本語フォント、検査用の pypdf・pdfplumber。`DRAWING_NODE`、`REML_PLAYWRIGHT_PACKAGE`、`REML_CHROMIUM_EXECUTABLE` でローカル環境を指定できる。

中間HTMLと確認画像は `tmp/pdfs/new-method-candidates/` に置く。生成後、Popplerで全ページをPNGへ描画し、図中文字・改ページ・表・ページ番号を目視する。PDFを再生成した場合は、以前の目視記録が同じPDFに対するものかをハッシュで確認し、更新する。

PDF内の資料リンクは生成時のローカルファイルを指す。PDFを別の環境へ移しても本文と図は読めるが、リンク先の資料は別途必要。
