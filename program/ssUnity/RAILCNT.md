# レールデータの要素（SS）

SSのレールデータについて解説する。

## 前提知識

まず、レールのモデルに関しては

これを覚えておかないといけない。

![model](/program/ssUnity/image/model.png)

図のようなモデルがあるとき、

![model_bone](/program/ssUnity/image/model_bone.png)

このモデルは、まるで背骨のように、8つの部分に分かれてそれぞれ動く

この８つの部分をそれぞれ **【ボーン】** と呼ぶ。


![model_bone2](/program/ssUnity/image/model_bone2.png)

単線、複線のボーンはそれぞれこう構成されている。

一番左側から初めて、下から 0～7 と定義し

複線の場合、右側に行くと100増えて、改めて下から 100～107 と定義する。

複々線の場合はもちろん、100ずつ増えるので 200～207、300～307となる。

<br>

![xyz](/program/ssUnity/image/xyz.png)

UnityのXYZ座標系は、こうなっている。

![xyz2](/program/ssUnity/image/xyz2.png)

blenderのような、このXYZではないので注意すること。

これが一番重要なので、覚えておく。


## index

現在、このレールのindex。

数字の順番を必ず合わせる必要はないが（内部で読込んだ順番で採番するため）

レール調整時、indexを付与した方が修正しやすい。

## prev_rail

レールのモデルそのものを、どのレールindex基準に置くかの番号

-1の場合、原点から置く

![prev_rail](/program/ssUnity/image/prev_rail.png)

つまり、もし52番のレールが、こう置いている場合

![prev_rail2](/program/ssUnity/image/prev_rail2.png)

レールの<br>index：53<br>prev_rail：52<br>と指定すると、こう置かれる

以前のprev_railが指す、最後のボーンの方向に合わせて置かれる。

## block

レールを表示するグループ番号と考えても良い。

現在車両位置で調べた、あるレールのblockの番号を基準に、

現在のblock番号と、±1したblock番号を表示する。

## pox_x, pox_y, pos_z

2番目の要素、prev_railに配置した基準に

並行移動させるXYZの数値

![pos](/program/ssUnity/image/pos.png)

これが必要な理由は、prev_railで配置したとき

図のように **【必ず中央寄せ】** で配置するので、pos_xの調整が必要になる。

![pos2](/program/ssUnity/image/pos2.png)

図は、pos_xに数値を入れた調整したもの。

調整する距離は必ず【6.5】になる。

もし単線を、**prev_railの複線** の左側に繋げたいときは、[-6.5]の調整を

右側に繋げたいときや、[6.5]の調整をする。

あるいは、**prev_railの単線** を、現在の複線の左側に繋げたいときは、[6.5]の調整を

右側に繋げたいときや、[-6.5]の調整をする。

<br>

その他、pos_y、pos_zの調整は **ほとんど** 使うことがない。

これは、prev_railを基準に、上下の平行移動

または、前後の平行移動になるため、

全く、別のスタート点から始まる路線を敷くときなどに使われる。

## dir_x, dir_y, dir_z

2番目の要素、prev_railに配置した基準に

回転させるXYZの数値

![dir](/program/ssUnity/image/dir.png)

少し極端な数値で適用した結果であるが

こういう方向に曲がることを覚えておくこと。

## mdl_no

MdlCntで定義されている、レールのモデル番号

レールに出来るモデルのリストは[【こちら】](/program/ssUnity/RAILLIST.md)のリンクを参照

## mdl_kasenchu

MdlCntで定義されている、レールの架線柱モデル番号

架線柱は基本的に大文字や小文字関係なく

「kasenchu」という名称が含まれていれば、そのモデルを置ける。

1. -1、または255の場合、MdlCntで定義している

    モデルのデフォルト架線柱を呼ぶ

    このデフォルト架線柱も-1の場合、架線柱がない状態になる。

2. -2、または254の場合、架線柱がない状態になる。

3. 上記以外の数値の場合、モデルを呼び出す。

## per

モデルをどれほど伸ばすかの倍率

1.0倍がデフォルトの長さであり、小数点まで細かく調整できる

1より小さいと縮むし、1より大きいと伸びる

## flg

レールをどのような状態にさせるかのフラグ

フラグについては、[【こちら】](/program/ssUnity/FLAG.md)のリンクを参照

よく分からないなら、まずは４つ全部０（0x00）にしても良い。

## rail_data

レールモデルで、進む方法の **個数** を定義する。

1の場合、単線の進み方になり、

2の場合、複線の進み方

4の場合、複々線の進み方になる。

また、単線のレールに複線の進み方とか

あるいは、複線のレールに単線の進み方などで書くと

エラーになることがある。

## next_rail, next_no, prev_rail, prev_no

レールの具体的な進み方を定義する。

next_rail、next_noは、次のどのレールとボーン番号にするか

prev_rail、prev_noは、現在レールは

どこから繋がって、現在レールに来たかのレールとボーン番号を定義する。

next_railを【-1】にすると、現在のレールで終わり

そこからはもう進めないようになる。

（※next_railが-1だと、next_noはどんな数字でも良いが-1として合わせるのが普通）

![raildata](/program/ssUnity/image/raildata.png)

このようなレールデータがある場合

![raildata2](/program/ssUnity/image/raildata2.png)

40番の複線レールの進み方の解説

![raildata3](/program/ssUnity/image/raildata3.png)

41番の単線レールの進み方の解説
