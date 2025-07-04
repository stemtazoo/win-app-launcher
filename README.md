# アプリランチャー (Flet版)

## 概要

このアプリは、**PythonとFletで作成されたWindows用のアプリランチャー**です。
自分のPCにあるよく使うアプリケーションやバッチファイルをリスト化し、**ワンクリックで起動・管理**できます。
追加や削除はGUIで直感的に行え、デザインもタイル風でモダンです。

---

## 主な特徴

* アプリ登録・削除はGUIで簡単操作
* ワンクリックでアプリケーションを起動
* アプリ一覧はタイル（カード）形式でモダン表示
* アプリ情報（名前とパス）はローカル`apps.json`に保存され、**次回起動時も自動復元**
* パス指定はテキスト入力 or \[参照]ボタンからファイルダイアログ選択が可能
* Windows・Mac・Linux（Flet対応環境）で動作

---

## インストール方法

### ⏩ もっとカンタン！

**Windowsなら `start.bat` をダブルクリックするだけで仮想環境構築・ライブラリ導入・ランチャーアプリ起動まで自動で行えます。**

---

1. **リポジトリをクローン**

   ```bash
   git clone https://github.com/yourname/win-app-launcher.git
   cd win-app-launcher
   ```

2. **仮想環境を作成・有効化（推奨）**

   Windows:

   ```bat
   python -m venv .venv
   call .venv\Scripts\activate
   ```

   Mac/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **依存パッケージのインストール**

   ```bash
   pip install -r requirements.txt
   ```

4. **アプリの起動**

   ```bash
   python src/main.py
   ```

   ※`start.bat`（Windows用バッチ）からも起動可能

---

## 使い方

### アプリの追加

* 「アプリ追加」タブで「アプリ名」と「アプリパス」を入力

  * パスは「参照」ボタンからファイル選択も可能
* 「追加」ボタンでリストに登録

### アプリの起動

* 「アプリ起動」タブのタイルから目的のアプリの▶ボタンをクリック

### アプリの削除

* タイルの🗑（ゴミ箱）アイコンをクリック

---

## データ保存について

* 登録したアプリ情報は `apps.json` に保存されます
* このファイルは `.gitignore` によりGit管理されません（ユーザーごとに個別管理されます）

---

## 開発・カスタマイズ

* `src/main.py` にすべての処理・UIがまとまっています
* デザインや機能追加もFletの知識で容易に拡張可能

---

## ライセンス

このプロジェクトはMITライセンスで公開されています。詳細は [LICENSE](./LICENSE) をご覧ください。

---

## 作者

* [stemtazoo](https://github.com/stemtazoo/win-app-launcher)
* ご意見・バグ報告は[issues](https://github.com/yourname/win-app-launcher/issues)まで！
