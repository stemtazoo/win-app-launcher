import flet as ft
import subprocess
import json
import os

APPS_FILE = "apps.json"

def load_apps():
    """
    アプリ一覧をJSONファイルから読み込む。
    ファイルがなければ空リストを返す。

    Returns:
        list[dict]: {'name': アプリ名, 'path': パス} のリスト
    """
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_apps(apps):
    """
    アプリ一覧をJSONファイルに保存する。

    Args:
        apps (list[dict]): {'name': アプリ名, 'path': パス} のリスト
    """
    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    """
    Fletアプリのメインエントリーポイント。
    UIのセットアップとイベントハンドラ定義を行う。

    Args:
        page (ft.Page): Fletのページオブジェクト
    """
    page.title = "アプリランチャー"
    page.window_width = 650
    page.window_height = 400

    # アプリリストとUI部品の初期化
    apps = load_apps()
    app_buttons = ft.Column()
    app_name = ft.TextField(label="アプリ名", width=200)
    app_path = ft.TextField(label="アプリパス", width=320)
    add_button = ft.ElevatedButton("追加")

    # ファイルピッカー（アプリパス選択用）
    file_picker = ft.FilePicker()

    def on_file_result(e: ft.FilePickerResultEvent):
        """
        ファイル選択ダイアログの選択結果をアプリパス欄に反映する。
        """
        if e.files:
            app_path.value = e.files[0].path
            page.update()

    file_picker.on_result = on_file_result
    page.overlay.append(file_picker)

    # [参照]ボタン
    file_select_button = ft.ElevatedButton("参照", on_click=lambda e: file_picker.pick_files(allow_multiple=False))

    def refresh_buttons():
        """
        アプリ起動タブのタイル一覧を再描画する。
        各アプリごとにカード（タイル）を生成してGridViewに並べる。
        """
        app_buttons.controls.clear()
        tiles = []
        for idx, app in enumerate(apps):
            tile = ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text(app['name'], size=18, weight="bold", color=ft.Colors.WHITE),
                        ft.Row([
                            ft.IconButton(
                                ft.Icons.PLAY_ARROW,
                                tooltip="起動",
                                icon_color=ft.Colors.GREEN_ACCENT_400,
                                on_click=lambda e, p=app['path']: launch_app(p)
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                tooltip="削除",
                                icon_color=ft.Colors.RED_ACCENT_200,
                                on_click=lambda e, i=idx: delete_app(i)
                            ),
                        ], alignment="center"),
                    ], spacing=8, alignment="center"),
                    width=160,
                    height=100,
                    padding=10,
                    alignment=ft.alignment.center,
                    border_radius=16,
                    bgcolor=ft.Colors.BLUE_GREY_800
                ),
                elevation=6,
            )
            tiles.append(tile)
        grid = ft.GridView(
            expand=True, runs_count=3, max_extent=180, child_aspect_ratio=1.4, spacing=12, run_spacing=12,
            controls=tiles
        )
        app_buttons.controls.append(grid)
        page.update()

    def launch_app(path):
        """
        指定したパスのアプリケーションを起動する。
        起動失敗時はダイアログでエラーを表示。

        Args:
            path (str): 実行ファイルまたはバッチファイルのパス
        """
        try:
            subprocess.Popen(path)
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"起動エラー: {ex}"))
            page.dialog.open = True
            page.update()

    def delete_app(index):
        """
        指定インデックスのアプリをリストから削除し、保存＆再描画。

        Args:
            index (int): appsリスト中の削除対象インデックス
        """
        del apps[index]
        save_apps(apps)
        refresh_buttons()

    def add_app(e):
        """
        入力欄のアプリ名・パスをappsリストに追加し、保存＆再描画。

        Args:
            e: Fletのイベント（未使用）
        """
        name = app_name.value.strip()
        path = app_path.value.strip()
        if name and path:
            apps.append({'name': name, 'path': path})
            save_apps(apps)
            app_name.value = ""
            app_path.value = ""
            refresh_buttons()

    add_button.on_click = add_app

        # テーマ選択ドロップダウン
    theme_options = [
        ft.dropdown.Option("system", "システム（自動）"),
        ft.dropdown.Option("light", "ライト"),
        ft.dropdown.Option("dark", "ダーク")
    ]
    theme_selector = ft.Dropdown(
        label="テーマ選択",
        value="system",
        options=theme_options,
        width=200
    )

    def on_theme_change(e):
        """
        設定タブのテーマ選択で、page.theme_modeを変更する。
        """
        if theme_selector.value == "light":
            page.theme_mode = ft.ThemeMode.LIGHT
        elif theme_selector.value == "dark":
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.SYSTEM
        page.update()

    theme_selector.on_change = on_theme_change

    # タブ切替UI（起動/追加/設定）
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="アプリ起動",
                content=app_buttons,
            ),
            ft.Tab(
                text="アプリ追加",
                content=ft.Row([app_name, app_path, file_select_button, add_button]),
            ),
            ft.Tab(
                text="設定",
                content=ft.Column([
                    ft.Container(
                        theme_selector,
                        padding=ft.padding.only(top=40)
                    )
                ]),
            ),
        ],
        expand=True,
    )

    page.add(tabs)
    refresh_buttons()


# Fletアプリの起動エントリポイント
ft.app(target=main)
