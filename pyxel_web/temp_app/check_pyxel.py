import importlib.util
import subprocess
import sys

def check_pyxel_installation():
    """Pyxelのインストール状態とバージョンを確認する"""
    try:
        # Pyxelが存在するか確認
        spec = importlib.util.find_spec("pyxel")
        if spec is None:
            print("Pyxel is not installed. Installing now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyxel"])
            return False
        
        # Pyxelのバージョンを確認
        import pyxel
        version = getattr(pyxel, "__version__", "Unknown")
        print(f"Pyxel version: {version}")
        
        # バージョン文字列をパース
        try:
            major, minor, patch = map(int, version.split('.'))
            if major < 2:
                print("Your Pyxel version is too old for web export. Updating to 2.0.0+...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyxel"])
                return False
            else:
                print("Pyxel version is 2.0.0 or newer, which supports web export.")
                return True
        except (ValueError, AttributeError):
            print("Cannot parse version number. Updating Pyxel to be safe...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyxel"])
            return False
            
    except Exception as e:
        print(f"Error checking Pyxel installation: {e}")
        return False

def check_app2html_support():
    """app2html機能がサポートされているか確認"""
    try:
        import pyxel
        if hasattr(pyxel, 'app2html'):
            print("app2html is supported in this Pyxel version.")
            return True
        else:
            print("app2html is NOT supported in this Pyxel version.")
            return False
    except ImportError:
        print("Pyxel is not installed correctly.")
        return False

if __name__ == "__main__":
    if check_pyxel_installation():
        print("Pyxel installation check passed.")
        if check_app2html_support():
            print("Your Pyxel installation supports web export. You're good to go!")
        else:
            print("Your Pyxel installation doesn't support web export. Please upgrade.")
    else:
        print("Please restart the script to use the new Pyxel installation.")