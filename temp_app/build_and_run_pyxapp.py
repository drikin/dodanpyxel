import os
import sys
import subprocess
import shutil
import time
import glob

# ビルド設定
TEMP_DIR = "temp_app"
GAME_MODULE = "main.py"
APP_FILE = "game.pyxapp"

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

def build_pyxapp():
    """PyxelゲームをPyxelアプリファイル(.pyxapp)にパッケージ化"""
    print("Pyxelゲームをパッケージ化しています...")
    
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
    
    # その他のPythonファイルも念のためコピー
    python_files = glob.glob("*.py")
    for py_file in python_files:
        if py_file not in essential_files:
            dst = os.path.join(TEMP_DIR, py_file)
            if not os.path.exists(dst):  # 重複コピーを避ける
                print(f"  追加コピー: {py_file} -> {dst}")
                shutil.copy(py_file, dst)
    
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
    
    # 重要: TEMPディレクトリ内のmain.pyをスタートアップファイルとしてパッケージ化
    print("\nパッケージ化コマンドを実行:")
    try:
        # Pyxelのpackageコマンドの要件：
        # 1. 現在のディレクトリからの相対パスでAPP_DIRを指定
        # 2. APP_DIR内のファイルを指定（APP_DIRからの相対パス）
        
        # 現在のディレクトリを一時的に変更
        current_dir = os.getcwd()
        os.chdir(TEMP_DIR)
        
        # 現在のディレクトリ (temp_app) からの相対パスで実行
        package_cmd = [sys.executable, "-m", "pyxel", "package", ".", "main.py"]
        print(f"実行コマンド（{os.getcwd()}から）: {' '.join(package_cmd)}")
        
        result = subprocess.run(
            package_cmd,
            check=False  # エラーで中断しない
        )
        
        # 元のディレクトリに戻る
        os.chdir(current_dir)
        
        print(f"パッケージ化コマンド終了コード: {result.returncode}")
        
        # 成功した場合、temp_appディレクトリにpyxappファイルが生成されるので、
        # それをcurrentディレクトリにコピー
        temp_pyxapp_files = glob.glob(os.path.join(TEMP_DIR, "*.pyxapp"))
        if temp_pyxapp_files:
            target_pyxapp = os.path.basename(temp_pyxapp_files[0])
            shutil.copy(temp_pyxapp_files[0], target_pyxapp)
            print(f"生成されたpyxappファイルをコピー: {temp_pyxapp_files[0]} -> {target_pyxapp}")
        
        # 生成された.pyxappファイルを確認
        pyxapp_files = glob.glob("*.pyxapp")
        if pyxapp_files:
            print(f"パッケージ化成功: {pyxapp_files[0]}")
            return pyxapp_files[0]
        else:
            print("エラー: パッケージファイルが生成されませんでした")
            
            # プランB: 直接実行
            print("プランB: 直接main.pyを実行します")
            return "direct"
            
    except Exception as e:
        print(f"パッケージ化例外エラー: {e}")
        print("プランB: 直接main.pyを実行します")
        return "direct"

def run_pyxapp(pyxapp_file):
    """Pyxelアプリを実行する"""
    # ソフトウェアレンダリング用の環境変数を設定
    env = os.environ.copy()
    # Vulkanを使わず、ソフトウェアレンダリングを強制する設定
    env["LIBGL_ALWAYS_SOFTWARE"] = "1"    # Mesa/OpenGLをソフトウェアモードに
    env["GALLIUM_DRIVER"] = "llvmpipe"    # Galliumドライバーをソフトウェアに
    env["MESA_GL_VERSION_OVERRIDE"] = "3.3"  # OpenGL 3.3を使用
    env["MESA_GLSL_VERSION_OVERRIDE"] = "330"  # GLSL 330を使用
    
    if pyxapp_file == "direct":
        print("直接main.pyを実行します...")
        try:
            # 直接main.pyを実行
            cmd = [sys.executable, "main.py"]
            print(f"実行コマンド: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env  # 環境変数を指定
            )
            
            print(f"Python main.pyを実行中 (PID: {process.pid})")
            return process
                
        except Exception as e:
            print(f"直接実行エラー: {e}")
            return None
    else:
        print(f"Pyxelアプリ {pyxapp_file} を実行しています...")
        
        try:
            # Pyxelのplayコマンドで実行
            cmd = [sys.executable, "-m", "pyxel", "play", pyxapp_file]
            print(f"実行コマンド: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env  # 環境変数を指定
            )
            
            print(f"Pyxelアプリを実行中 (PID: {process.pid})")
            return process
                
        except Exception as e:
            print(f"実行エラー: {e}")
            return None

def main():
    """メイン実行関数"""
    # まずPyxelアプリにパッケージ化
    pyxapp_file = build_pyxapp()
    if not pyxapp_file:
        print("パッケージ化に失敗しました")
        sys.exit(1)
    
    # Pyxelアプリを実行
    process = run_pyxapp(pyxapp_file)
    if not process:
        print("Pyxelアプリの実行に失敗しました")
        sys.exit(1)
    
    # プロセスが終了するまで待機
    try:
        process.wait()
    except KeyboardInterrupt:
        print("ユーザーによる中断を検出しました。終了します...")
        process.terminate()
    
    print("Pyxelアプリの実行が終了しました")

if __name__ == "__main__":
    main()