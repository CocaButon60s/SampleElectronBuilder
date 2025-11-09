import pyzipper
from pathlib import Path
import json
import os
import sys


def getErcdList() -> json:
    ercd_path = (
        Path(sys._MEIPASS)
        if getattr(sys, "frozen", False)
        else Path(os.path.dirname(__file__))
    )

    try:
        with open(ercd_path / "ercd.json", encoding="utf-8") as f:
            ercd = json.load(f)
    except FileNotFoundError:
        print("エラーコードファイルが見つかりません。", file=sys.stderr)
        sys.exit(-1)
    except json.JSONDecodeError as e:
        print(f"エラーコードファイルのJSONデコードに失敗しました: {e}", file=sys.stderr)
        sys.exit(-1)
    except OSError as e:
        print(f"エラーコードファイルの入出力エラー: {e}", file=sys.stderr)
        sys.exit(-1)
    except Exception as e:
        print(f"エラーコードの読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(-1)

    return ercd


if __name__ == "__main__":
    ercd = getErcdList()
    if len(sys.argv) != 3:
        print(
            "Usage: decrypt <zip file path> <password>",
            file=sys.stderr,
        )
        sys.exit(ercd["ERR_ARGS"])

    zip_file = Path(sys.argv[1])
    output_dir = zip_file.parent
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = bytes(sys.argv[2], "utf-8")
            zf.extractall(output_dir)
    except FileNotFoundError:
        print("ZIPファイルが見つかりません。", file=sys.stderr)
        sys.exit(ercd["ERR_FILE_NOT_FOUND"])
    except pyzipper.BadZipFile:
        print("ZIPファイルが壊れています。", file=sys.stderr)
        sys.exit(ercd["ERR_BAD_ZIP_FILE"])
    except RuntimeError:
        print("パスワードが間違っています。", file=sys.stderr)
        sys.exit(ercd["ERR_WRONG_PASSWORD"])
    except OSError as e:
        print(f"入出力エラー: {e}", file=sys.stderr)
        sys.exit(ercd["ERR_IO"])
    except Exception as e:
        print(f"不明なエラーが発生しました。: {e}", file=sys.stderr)
        sys.exit(ercd["ERR_UNKNOWN"])
