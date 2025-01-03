# AMBの要素（SS）

SSのAMBについて解説する。

## 注意

AMBの項目を見る前に、まずレールの知識を理解すること。

## AMBのフラグ

AmbCnt:の項目を見ると、実際のAMBのindex個数と横にまた数字がある

これは、最後の要素のkasenchu_perを適用するためのフラグであり

1以上設定されていると適用される。

0に設定すると適用せず、kasenchu_perは固定値１になる。

このフラグは１のままで、普通はいじらなくて良い。

## index

現在、このAMBのindex。

数字の順番を必ず合わせる必要はないが（内部で読込んだ順番で採番するため）

AMB調整時、indexを付与した方が修正しやすい。

## rail

最初に始めるAMBを、どのレール番号の基準で置くかの設定。

つまり、AMBを置くためには、まずレールを完成させないといけない。

指定したレールの、一番最初の点（ボーン0番）を基準に置かれる。

## length

AMBのモデルを、モデルの中心から車両の位置までの距離が

指定した距離範囲内の場合、表示する。

普段は1000で固定しても良い

## amb_data

1個のAMBが抱える実物のモデル個数。

<br>

【個数】であるため、『必ず！』1個以上である必要がある。

「0以下」に指定したら「一応は」、AMBを全く表示しないようになり、

ゲーム内では止まったりする深刻なエラーは起こらないが、（ただし、ログではエラーと出る）

エクセルで取り出すときにエラーになるため

0以下に指定したものは、必ず消すこと。

<br>

あるAMBのモデルを置いてから、次のAMBモデルを指定すると

後に説明するparentIndexに従って、直前のAMBが指す方向に合わせて置かれる。

## mdl_no

MdlCntで定義されている、AMBのモデル番号

AMBに出来るモデルのリストは[【こちら】](/program/ssUnity/AMBLIST.md)のリンクを参照

## parentIndex

![parentIndex](/program/ssUnity/image/parentIndex.png)

1個のAMBが抱えるモデルの中から、自分の親のAMB_index

つまり、amb_dataで定義した分、階層の形になり

一番先に始めるモデルは、parentIndexが-1になる。

この情報を元に、内部ではAMB_indexを定義するため

これは順番を-1から守る必要がある。

## pox_x, pox_y, pos_z

![AMB_pos](/program/ssUnity/image/AMB_pos.png)

レールのpos_x, pos_y, pos_zと同じく

モデルを平行移動させる。

## dir_x, dir_y, dir_z

![AMB_dir](/program/ssUnity/image/AMB_dir.png)

ちょっと名称が紛らわしいが、

**レールのdir_x, dir_y, dir_zとは違う。**

部分的に回転させて曲げたものとは違って

モデル全体、そのものの回転を意味する。

## joint_dir_x, joint_dir_y, joint_dir_z

![AMB_joint_dir](/program/ssUnity/image/AMB_joint_dir.png)

こっちの方が

レールのdir_x, dir_y, dir_zと同じ。

## per

レールのperと同じく、

モデルをどれほど伸ばすかの倍率

1.0倍がデフォルトの長さであり、小数点まで細かく調整できる

1より小さいと縮むし、1より大きいと伸びる

## kasenchu_per

こっちは、上記の「AMBのフラグ」説明してた、フラグが1以上ではないと

細かく設定できないようになっている。

またkasenchu_perは、AMBのオブジェクトに【mKasenChu】という項目が

定義されているモデルのみ適用され、

perと同じく、それをどれほど伸ばすかの倍率である。

![kasenchu_per](/program/ssUnity/image/kasenchu_per.png)

この項目があるモデルは

例えば、AMB_Kasenchu_Shortというモデルである。

![kasenchu_per2](/program/ssUnity/image/kasenchu_per2.png)

perで1.0より大きく設定すると、横に伸びる仕様になる。

mKasenChuがあるAMBは、下記の通りである。

| モデル名 |
| --- |
| AMB_BLACK_CHU |
| AMB_BlackCube |
| AMB_HQ_KasenLong0 |
| AMB_Kaidan2 |
| AMB_Kasenchu_Center |
| AMB_Kasenchu_Left |
| AMB_Kasenchu_Long0 |
| AMB_Kasenchu_Long1 |
| AMB_Kasenchu_Long2 |
| AMB_Kasenchu_Short |
| AMB_Mina_Wall2 |
| AMB_SAKU |
| AMB_Toyo_Kasenchu |
| AMB_TQ_Kaidan3 |
| TQ_Eda_Iron |
| TQ_Eda_Yane |

## ※ぶつけ判定があるAMBのモデル

### ドリフトした場合、自走不能

| モデル名 |
| --- |
| AMB_Bridgh_W_Hashira |
| AMB_CHIKA_IN |
| AMB_MetalBox |
| AMB_MetalBox_50 |
| AMB_UNDER_HASHIRA |
| AMB_UNDER_HASHIRA2 |
| AMB_UNDER_HASHIRA4 |
| AMB_UNDER_IN |
| TQ_Obj0 |

### ドリフト関係なく突っ込む場合、自走不能

| モデル名 |
| --- |
| AMB_3300Body |
| AMB_Stop |
| RailEnd |
| UmedaStop |

### ドリフトした場合、飛ぶ（片輪ドリフトの場合、解除）

| モデル名 |
| --- |
| AMB_1RAIL_UNDER_IN |
| AMB_DriftBlock |
| AMB_TQ_Wall0 |
| AMB_TrackMdl |
