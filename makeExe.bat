pyinstaller main.py --clean --onefile --noconsole --add-data "./ver.txt;./" --add-data "./program/fvtMaker/importPy/resource/*;./" --add-data "./program/orgInfoEditor/dendData/*;./" --add-binary "%LocalAppData%/Programs/Python/Python310/Lib/site-packages/UnityPy;./UnityPy"