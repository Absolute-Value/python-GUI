## Tkinter
GUIアプリケーションを作成することができる

## 作成したソフトを実行ファイル(exe等)で実行できるようにする
pyinstallerをインストール
```console
pip install pyinstaller
```

実行ファイル(exe等)に出力
dist/ に出力される
```console
pyinstaller {ファイル名} --onefile
```
--onefile オプションで一つにまとまる