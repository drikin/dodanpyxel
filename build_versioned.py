#!/usr/bin/env python3
"""
LAST DESCENT: バージョン管理ビルドスクリプト
コミットごとにビルド番号を更新し、dist以下にバージョン付きのビルドを生成します
"""

import os
import sys
import subprocess
import shutil
import time
import glob
import datetime
import json

# ビルド設定
TEMP_DIR = "temp_app"
BUILD_DIR = "dist"
VERSION_FILE = "version.json"
PROJECT_NAME = "last_descent"

def ensure_directory(directory):
    """指定されたディレクトリが存在しない場合は作成する"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def clean_directory(directory):
    """指定されたディレクトリを空にする"""
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(directory)

def get_version_info():
    """バージョン情報を取得する"""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, 'r') as f:
                version_info = json.load(f)
                return version_info
        except:
            print(f"警告: バージョンファイルの読み込みに失敗しました")
    
    # デフォルトのバージョン情報
    return {
        "major": 1,
        "minor": 0,
        "patch": 0,
        "build": 0,
        "last_build_date": ""
    }

def save_version_info(version_info):
    """バージョン情報を保存する"""
    with open(VERSION_FILE, 'w') as f:
        json.dump(version_info, f, indent=2)

def increment_build_number():
    """ビルド番号を更新する"""
    version_info = get_version_info()
    
    # ビルド番号をインクリメント
    version_info["build"] += 1
    
    # 最終ビルド日時を更新
    version_info["last_build_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存
    save_version_info(version_info)
    
    return version_info

def get_version_string(version_info):
    """バージョン文字列を取得する"""
    return f"{version_info['major']}.{version_info['minor']}.{version_info['patch']}.{version_info['build']}"

def build_pyxapp():
    """PyxelゲームをPyxelアプリファイル(.pyxapp)にパッケージ化"""
    print("Pyxelゲームをパッケージ化しています...")
    
    # バージョン情報を更新
    version_info = increment_build_number()
    version_string = get_version_string(version_info)
    
    print(f"ビルドバージョン: {version_string}")
    
    # 古いpyxappファイルがあれば削除
    pyxapp_files = glob.glob("*.pyxapp")
    for old_file in pyxapp_files:
        print(f"古いpyxappファイルを削除: {old_file}")
        os.remove(old_file)
    
    # main.pyがカレントディレクトリにあるか確認
    if not os.path.exists("main.py"):
        print("警告: main.pyが見つかりません。直接実行モードに切り替えます。")
        return "direct"
    
    # 必要なディレクトリを準備
    clean_directory(TEMP_DIR)  # クリーンスタート
    ensure_directory(os.path.join(TEMP_DIR, "assets"))
    
    # メインPythonファイルをTEMP_DIRにコピー
    essential_files = ["main.py", "game.py", "player.py", "enemy.py", "bullet.py", 
                      "explosion.py", "background.py", "powerup.py", "boss.py", 
                      "constants.py", "highscores.py"]
                      
    print("重要なファイルをコピーします:")
    for file in essential_files:
        if os.path.exists(file):
            dst = os.path.join(TEMP_DIR, file)
            print(f"  コピー中: {file} -> {dst}")
            shutil.copy(file, dst)
        else:
            print(f"  警告: {file}が見つかりません")
    
    # version.pyを生成してTEMP_DIRにコピー
    with open("version.py", "w") as f:
        f.write(f"""# 自動生成されたバージョン情報
VERSION = "{version_string}"
BUILD_DATE = "{version_info['last_build_date']}"
""")
    print(f"  生成: version.py")
    shutil.copy("version.py", os.path.join(TEMP_DIR, "version.py"))
    
    # main.pyにバージョン情報を追加
    main_py_path = os.path.join(TEMP_DIR, "main.py")
    with open(main_py_path, "r") as f:
        main_content = f.read()
    
    # バージョンインポートがまだ無い場合は追加
    if "import version" not in main_content:
        # importの後に追加
        import_pos = main_content.find("import")
        if import_pos >= 0:
            next_line_pos = main_content.find("\n", import_pos) + 1
            main_content = main_content[:next_line_pos] + "import version\n" + main_content[next_line_pos:]
        
        # タイトルにバージョン表示を追加
        title_line = 'TITLE = "LAST DESCENT: THE FINAL HOPE"'
        if title_line in main_content:
            new_title_line = f'TITLE = "LAST DESCENT: THE FINAL HOPE v{version_string}"'
            main_content = main_content.replace(title_line, new_title_line)
    
    # 更新したmain.pyを書き戻す
    with open(main_py_path, "w") as f:
        f.write(main_content)
    
    # assetsディレクトリ内のファイルをコピー
    if os.path.exists("assets"):
        print("assetsディレクトリが見つかりました")
        for asset_file in os.listdir("assets"):
            if asset_file.endswith(".py"):
                src = os.path.join("assets", asset_file)
                dst = os.path.join(TEMP_DIR, "assets", asset_file)
                ensure_directory(os.path.dirname(dst))
                print(f"  コピー中: {src} -> {dst}")
                shutil.copy(src, dst)
    else:
        print("警告: assetsディレクトリが見つかりません")
    
    # high_scores.jsonをコピー（存在する場合）
    if os.path.exists("high_scores.json"):
        print("high_scores.jsonをコピーします")
        shutil.copy("high_scores.json", TEMP_DIR)
    
    # コピーできているか確認
    print(f"\n{TEMP_DIR}ディレクトリの内容:")
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            print(f"  {os.path.join(root, file)}")
    
    # まずはPyxelのバージョンを確認
    print("\nPyxelのコマンドを確認:")
    try:
        help_check = subprocess.run(
            [sys.executable, "-m", "pyxel"], 
            capture_output=True, 
            text=True
        )
        print(f"{help_check.stdout}")
    except Exception as e:
        print(f"Pyxelコマンド確認エラー: {e}")
    
    # パッケージ化を実行
    print("\nパッケージ化コマンドを実行:")
    try:
        # 現在のディレクトリを一時的に変更
        current_dir = os.getcwd()
        os.chdir(TEMP_DIR)
        
        # パッケージ化を実行
        package_cmd = [sys.executable, "-m", "pyxel", "package", ".", "main.py"]
        print(f"実行コマンド（{os.getcwd()}から）: {' '.join(package_cmd)}")
        
        result = subprocess.run(
            package_cmd,
            check=False
        )
        
        # 元のディレクトリに戻る
        os.chdir(current_dir)
        
        print(f"パッケージ化コマンド終了コード: {result.returncode}")
        
        # 生成されたpyxappファイルを確認
        temp_pyxapp_files = glob.glob(os.path.join(TEMP_DIR, "*.pyxapp"))
        if temp_pyxapp_files:
            # バージョン付きのファイル名を生成
            # バージョン文字列のドットをアンダースコアに置換（URL互換性のため）
            version_display = version_string.replace(".", "_")
            versioned_filename = f"{PROJECT_NAME}_v{version_display}.pyxapp"
            target_pyxapp = versioned_filename
            
            # distディレクトリにコピー
            ensure_directory(BUILD_DIR)
            dist_path = os.path.join(BUILD_DIR, target_pyxapp)
            shutil.copy(temp_pyxapp_files[0], dist_path)
            print(f"生成されたpyxappファイルをdistにコピー: {temp_pyxapp_files[0]} -> {dist_path}")
            
            # 通常の場所にもコピー
            shutil.copy(temp_pyxapp_files[0], "temp_app.pyxapp")
            
            print(f"パッケージ化成功: {dist_path}")
            return dist_path
        else:
            print("エラー: パッケージファイルが生成されませんでした")
            return None
            
    except Exception as e:
        print(f"パッケージ化例外エラー: {e}")
        return None

def run_pyxapp(pyxapp_file):
    """Pyxelアプリを実行する"""
    if not pyxapp_file:
        print("警告: 実行するPyxelアプリファイルがありません")
        return None
        
    # ソフトウェアレンダリング用の環境変数を設定
    env = os.environ.copy()
    env["LIBGL_ALWAYS_SOFTWARE"] = "1"
    env["GALLIUM_DRIVER"] = "llvmpipe"
    env["MESA_GL_VERSION_OVERRIDE"] = "3.3"
    env["MESA_GLSL_VERSION_OVERRIDE"] = "330"
    
    print(f"Pyxelアプリ temp_app.pyxapp を実行しています...")
    
    try:
        # Pyxelのplayコマンドで実行
        cmd = [sys.executable, "-m", "pyxel", "play", "temp_app.pyxapp"]
        print(f"実行コマンド: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        print(f"Pyxelアプリを実行中 (PID: {process.pid})")
        return process
            
    except Exception as e:
        print(f"実行エラー: {e}")
        return None

def list_builds():
    """distディレクトリのビルド一覧を表示"""
    ensure_directory(BUILD_DIR)
    builds = glob.glob(os.path.join(BUILD_DIR, f"{PROJECT_NAME}_v*.pyxapp"))
    
    if not builds:
        print("ビルドが見つかりません")
        return
    
    # ビルドバージョンをパースして数値化する関数
    def get_version_number(build_path):
        try:
            # ファイル名からバージョン部分を抽出 (例: last_descent_v1_0_0_12.pyxapp または last_descent_v1.0.0.12.pyxapp)
            filename = os.path.basename(build_path)
            version_str = filename.split('_v')[1].split('.pyxapp')[0]  # 1_0_0_12 または 1.0.0.12 部分を取得
            
            # アンダースコアをドットに置換してから分割（両方の形式に対応）
            version_str = version_str.replace("_", ".")
            
            # バージョン番号をドットで分割して数値配列に変換
            version_parts = [int(x) for x in version_str.split('.')]
            
            # 比較のために一つの数値に変換（Major*1000000 + Minor*10000 + Patch*100 + Build）
            version_num = 0
            for i, part in enumerate(version_parts):
                version_num += part * (10 ** (6 - i * 2))
            return version_num
        except:
            return 0  # パースできない場合は0を返す
    
    # バージョン番号でソートして最新を取得
    sorted_builds = sorted(builds, key=get_version_number)
    newest_build = sorted_builds[-1]
    
    # 最新ビルドの情報表示
    filename = os.path.basename(newest_build)
    filesize = os.path.getsize(newest_build) / 1024  # KBに変換
    mod_time = os.path.getmtime(newest_build)
    mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n最新のビルド:")
    print(f"  {filename} ({filesize:.1f} KB) - 作成日時: {mod_time_str}")
    
    # 古いビルドを削除（最新ビルドは除く）
    for build in builds:
        if build != newest_build:
            try:
                os.remove(build)
                print(f"古いビルドを削除しました: {os.path.basename(build)}")
            except Exception as e:
                print(f"ビルド削除エラー: {e}")

def cleanup_temp_files():
    """一時ファイルを削除する"""
    # 一時ディレクトリを削除
    if os.path.exists(TEMP_DIR):
        print(f"\n一時ディレクトリを削除: {TEMP_DIR}")
        shutil.rmtree(TEMP_DIR)
    
    # 一時的なversion.pyを削除
    if os.path.exists("version.py"):
        print(f"一時ファイルを削除: version.py")
        os.remove("version.py")

def main():
    """メイン実行関数"""
    print("===== LAST DESCENT: バージョン管理ビルドスクリプト =====")
    
    # コマンドライン引数をチェック
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_builds()
        return
    
    # ビルドディレクトリを作成
    ensure_directory(BUILD_DIR)
    
    # Pyxelアプリをビルド
    pyxapp_file = build_pyxapp()
    if not pyxapp_file:
        print("ビルドに失敗しました")
        cleanup_temp_files()
        sys.exit(1)
    
    # 利用可能なビルドを表示
    list_builds()
    
    # Pyxelアプリを実行
    process = run_pyxapp(pyxapp_file)
    if not process:
        print("Pyxelアプリの実行に失敗しました")
        cleanup_temp_files()
        sys.exit(1)
    
    # プロセスが終了するまで待機
    try:
        process.wait()
    except KeyboardInterrupt:
        print("ユーザーによる中断を検出しました。終了します...")
        process.terminate()
    
    print("Pyxelアプリの実行が終了しました")
    
    # 最後に一時ファイルを削除
    cleanup_temp_files()

if __name__ == "__main__":
    main()