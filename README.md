# dyloopman

## requirement
- Python
    - Pipfile 記載のものと違う場合はPipfileを書き換える
- pipenv


## setup (windows)
```
#### on git bash
$ pipenv install
$ curl 'https://raw.githubusercontent.com/opencv/opencv/refs/heads/4.x/data/haarcascades/haarcascade_frontalface_default.xml' > haarcascade_frontalface_default.xml
```

## how to use
### 設定変更
- 置換画像の変更
    - `if __name__ == '__main__':` 以下の `mask_img` を変更
- 顔認識モデルの変更の変更
    - `if __name__ == '__main__':` 以下の `cascade_file` を変更
- 顔認識のパラメータ変更
  `cascade.detectMultiScale()` の引数を変更

### ローカル実行
#### 画像に適用
画像に対して顔認識・置換を実施する。
```
$ pipenv run python local_main.py image {ファイル名}
```
ファイル名省略でテスト用画像が適用される。出力先は `/output_img`。

#### カメラチェック
PC に接続されているカメラのポート番号と映りを確認する。
```
$ pipenv run python local_main.py camcheck {確認する数}
```
`/output_img` に、各カメラから撮れる映像のスクショが `campera{カメラポート番号}.png` に保存される。

今のところ自動的に 640x480 になってしまう。

#### カメラ映像に適用
カメラ映像に対して顔認識・置換を実施する。
```
$ pipenv run python local_main.py video {カメラポート番号}
```
カメラポート番号省略時はポート番号0。  
キーボード `q` でビュアー終了。

今のところ自動的に 640x480 になってしまう。

#### 動画に適用
入力動画に対して顔認識・置換を実施する。
```
$ pipenv run python local_main.py movie {ファイル名}
```
ファイル名省略でテスト用動画が適用される。  
キーボード `q` でビュアー終了。

### Sora SFU 向け実行
- `.env.template` を `.env` にコピー
  - `SORA_SIGNALING_URLS`, `SORA_CHANNEL_ID`, `SORA_METADATA` を入力
  - カメラポート番号が 0 以外の場合 `SORA_CAMERA_ID` のコメントアウトを外して入力
  - 映像サイズを大きくしたい場合 `SORA_VIDEO_WIDTH`, `SORA_VIDEO_HEIGHT` のコメントアウトを外して入力
    - 今のところ設定しないと 640x480 になってしまう

```
$ pipenv run python send_main.py 
```
