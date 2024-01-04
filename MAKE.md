## Windows 版実行バイナリ（ .exeファイル ）の作成方法

セキュリティソフトによって、実行できない環境で実行ファイルの作成方法


### インストール

まず、python3をインストールする。

3.10.9をインストールする。[【インストールリンク】](https://www.python.org/downloads/release/python-3109/)


![python](image/python.png)

Windows環境なら、「Windows installer (64-bit)」をクリックしてダウンロードする


![install](image/install.png)

ダウンロードしたファイルを起動する、

この画面が出たら、必ず①（Add python.exe to PATH）をチェックした状態で

②（インストール）をクリックする


### ソースダウンロード

インストールが出来たら、ソースをダウンロードしよう

![download](image/download.png)

Download Zipをクリックする

ダウンロードしたzipファイルを解凍する


### バッチファイルの実行

1. まず、setup.batのバッチファイルを実行する

2. 次に、makeExe.batのバッチファイルを実行する

3. distのフォルダーにmain.exeが作成される