# stagedataの要素

SSのステージデータについて解説する。

ここには、レールデータやAMBの解説が書かれてないので

レールデータは[【こちら】](/program/ssUnity/RAILCNT.md)のリンクを参照

AMBは[【こちら】](/program/ssUnity/AMBCNT.md)のリンクを参照

## Story:

コメント通り、読み込むBGMを決めるもの

普段はいじらなくても良い

## Dir:

コメント通り、基本の向きを決めるもの

「１」がデフォルトで、レールを敷いた方向に進む

「ー１」は反対方向に進む

ただし、コミックスクリプトでまた上書きすることが多いので

普段はいじらなくても良い

ちなみに、必ずこの項目を書く必要はなく

存在しない場合、内部で１と決める。

## Track:

コメント通り、台車モデルを決めるもの

「０」は標準軌で、

「１」は狭軌で設定し、狭軌がデフォルトになっている。

ちなみに、必ずこの項目を書く必要はなく

存在しない場合、内部で１と決める。

## COMIC_DATA

コロンが付いてないことに注意

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

読込むコミックスクリプトのフォルダーを決める

## COMIC_IMAGE

コロンが付いてないことに注意

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

読込む画像のフォルダーを決める

## COMIC_SE

コロンが付いてないことに注意

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

読込むSEのフォルダーを決める

## RailPos:

コメント通り、「ストーリーモード」で選択した車両の初期位置を決めるもの

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

それぞれレール番号、ボーン番号、ボーン番号からの距離を決める

3番目の要素は普段0になることが多い。

ただし、コミックスクリプトでまた上書きすることが多く、

ストーリーモードを改造しない限り、普段はいじらなくても良い

## FreeRun:

コメント通り、「試運転モード」で選択した車両の初期位置を決めるもの

Tab区切りで読込む数字がないため、

読込む文字列は1個に決まっている。

それぞれレール番号、ボーン番号、ボーン番号からの距離を決める

3番目の要素は普段0になることが多い。

ただし、コミックスクリプトでまた上書きすることが多いので、

普段はいじらなくても良い

## VSPos:

コメント通り、「バトルモード」で選択した車両の初期位置を決めるもの

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

それぞれレール番号、ボーン番号、ボーン番号からの距離を決める

3番目の要素は普段0になることが多い。

ただし、コミックスクリプトでまた上書きすることが多いので、

普段はいじらなくても良い

## ~~VSStation:~~

駅判定開始・・・と書いているが・・・

内部コードで読込みはするが・・・

実際には使わないダミーデータ

## ~~VSMusic:~~

対戦ＢＧＭ変更レールと書いているが・・・

内部コードでそもそも読込すらしない、ダミーデータ

## FadeImage:

ステージを選択してから、ローディング中の画面

ゴールしてからメニューに戻るまでの、ローディングする画面を決める。

Tab区切りで読込む数字を決め、すぐ下の文字列を読み込む。

1番目の要素で、denファイルを読み込み、

2番目の要素で、denファイル中の画像ファイルを読み込む

## StageRes:

路線別画像データ

後で説明する、「SetTexInfo:」で使うためのもの。

2番目の要素で、denファイルを読み込み、

3番目の要素で、denファイル中の画像ファイルを読み込む

## SetTexInfo:

画像設定情報

AMBで設定したモデルの画像を設定するためのもの。

詳しい解説は[【こちら】](/program/ssUnity/TEXINFO.md)のリンクを参照

## STCnt:

駅名情報

右上に表示させる駅名の設定。

2番目の要素は、内部コードで使う駅のindex

3番目の要素は、レール位置

4番目の要素は、指定したレール位置からどれほどずらすかのoffset

5番目以後は、駅名、ふりがな、英語表記の順だが

必ず書く必要ない。（こうすると全く表示しない）

## CPU:

ストーリーモードのＣＰＵ切り替え情報

2番目の要素は、レール位置

3番目の要素は、車両indexで「1」の固定数値

4番目以後は、コミックスクリプトのCPU_MODEとほとんど同じ

ストーリーモードを改造しない限り、普段はいじらなくても良い

## ComicScript:

読み込ませるコミックスクリプト情報

2番目にコミックスクリプトの番号

3番目にコミックスクリプトのタイプ

4番目にレール位置、

5番目にどれほどずらすかのoffset

コミックスクリプトで、GOTO_SCRIPTで呼び出したいときは

勝手に発動しないように、レール位置を-1にする。

## RainChecker:

![RainChecker](/program/ssUnity/image/RainChecker.png)

雨のイベント情報・・・のみのように見えるが

実際は、雨のイベント、ワイパーのイベントはもちろん

外の夜景の位置設定まで担当している。

### イベントタイプ

【0】：雨停止

【3】：ワイパー停止

イベントが分かれているように見えるが、

実際はワイパー停止が、雨停止イベントまで同時にやっている。

パラメータ必要なし。

<br>

【1】：雨開始

【2】：ワイパー開始

同じくイベントが分かれているように見えるが、

実際はワイパー開始が、雨開始イベントまで同時にやっている。

パラメータ必要なし。

<br>

~~【4】：音だけ停止~~

~~【5】：音だけ開始~~

ダミーデータ

<br>

【10】：地下突入

外の夜景を非表示させる。パラメータ必要なし。

【11】：地下から出現

外の夜景を表示させる。パラメータ必要なし。

<br>

【100】：CityPos

パラメータ６つが必要な、夜景の建物のY軸を調整するもの。

・1番目と6番目で、CityのY軸を調整する。

・2番目と6番目でBillMdl1のY軸を、3番目と6番目でBillMdl1のY軸を調整する。

・4番目と6番目でBill0のY軸を、5番目と6番目でBill1のY軸を調整する。

<br>

【101】：CityScale

パラメータ２つが必要な、夜景のScaleを調整するもの。

・1番目と2番目で、CityのScaleを調整する。

<br>

【102】：MountPos

パラメータ２つが必要な、外の山の位置を調整するもの。

・1番目と2番目で、山の位置を調整する。

## DosanInfo:

![DosanInfo](/program/ssUnity/image/DosanInfo.png)

土讃線スペシャル領域・・・と書いているが

現状SSの仕様は、そのまま高くジャンプさせることしかやってない。

### イベントの前提条件

event_typeは10のみ設定できない。

パラメータの1番目の、ジャンプさせる速度を設定しておき

現在の速度がパラメータの速度より低い場合、ジャンプイベントは発動されない。

### コミックスクリプトの（SET_LV_JUMP）で、ジャンプ数値を0より高く定義している

3番目でジャンプする高さ、4番目でどれくらいジャンプするかの要素に

SET_LV_JUMPで定義している数値分、倍率を適用してジャンプを設定する。

### 未定義、もしくは0以下で定義されている

次のような式を計算する。

```
num2 = (現在速度 - パラメータ1番目) / (パラメータ2番目 - パラメータ1番目)
```

3番目でジャンプする高さ、4番目でどれくらいジャンプするかの要素に

上記の式で出た結果値に、倍率を適用してジャンプを設定する。

ただし、結果値が1.25より高い場合、1.25に設定する。


## MdlCnt:

読み込ませるモデルの情報

レールとAMBのすべては、ここから始まる。

2番目の要素は、読み込むモデルの名称

3番目と4番目の要素は、モデル自体のフラグ

このフラグは、後にレールのフラグと連携させる

詳しい説明は、[【こちら】](/program/ssUnity/FLAG.md)のリンクを参照

5番目の要素は、デフォルトの架線柱番号

MdlCntのindexから決める、自己参照の形になっている。

## RailPri:

優先レール設定

ただし、これはnext_noが0、prev_noが7のように

デフォルト数値同士で繋がっている分岐線路に対して

どっちに行かせるかの決めるものであり

next_noやprev_noがそれぞれ違う数字で繋がっているレールに対しては

優先レールが適用されない。

## BtlPri:

バトルモードのみ適用する

優先レールの設定

必ず書く必要はない。

## NoDriftRail:

ドリフトさせないレール

必ず書く必要はない。