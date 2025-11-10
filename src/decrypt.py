import pyzipper
from pathlib import Path
import json
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: decrypt <jsonstring>", file=sys.stderr)
        sys.exit(-1)

    arg = json.loads(sys.argv[1])
    zipfile, datas = Path(arg["zipfile"]), arg.get("data", [])
    output_dir = zipfile.parent / zipfile.stem
    os.makedirs(output_dir, exist_ok=True)

    msg = ""
    for data in datas:
        try:
            with pyzipper.AESZipFile(zipfile) as zf:
                zf.pwd = bytes(data.get("pswd"), "utf-8")
                zf.extractall(output_dir)
            basedir = [x.name for x in output_dir.iterdir() if x.is_dir()][0]
            open(output_dir / basedir / data["marker"], "w").close()

            print("解凍に成功しました。")
            sys.exit(0)
        except FileNotFoundError:
            print("ZIPファイルが見つかりません。", file=sys.stderr)
            sys.exit(-1)
        except pyzipper.BadZipFile:
            print("ZIPファイルが壊れています。", file=sys.stderr)
            sys.exit(-1)
        except RuntimeError:
            msg = "パスワードが間違っています。"
        except OSError as e:
            print(f"入出力エラー: {e}", file=sys.stderr)
            sys.exit(-1)
        except Exception as e:
            print(f"不明なエラーが発生しました。: {e}", file=sys.stderr)
            sys.exit(-1)
    print(msg, file=sys.stderr)
    sys.exit(-1)
