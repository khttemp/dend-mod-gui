# SetTexInfoの解説（SS）

SSのSetTexInfoついて解説する。

![texInfo](/program/ssUnity/image/texInfo.png)

普段、駅番号とか駅表などを設定するときに使う。

## amb番号、amb_child番号

2番目の要素で、ambの番号を

3番目の要素で、2番目で指定したambのchild番号で適用するモデルを特定させ、適用する

もし、2番目の要素が-1の場合、

3番目の要素で、モデル番号（MdlCntで定義）を設定して、全てのモデルに適用させる

## 路線別画像データ番号

4番目の要素で、StageResで設定したテクスチャーのindex番号で

特定したモデルに設定する

## tex_type, change_index, mat_index, f1, f2

### 全体的なモデルの適用

amb番号が-1で、全体的にモデルに適用する場合

tex_typeは10、11のみ適用される。

![TqLEDBord](/program/ssUnity/image/TqLEDBord.png)

【10】：時刻表示案内

AMBモデルに、「mTqLEDBord」がある場合適用される。

「mTqLEDBord」に定義されたモデルリストの中で、

change_indexで設定したLEDモデルを取得し、

路線別画像データ番号(res_data_index)で、変更する。

mTqLEDBordがあるAMBは、下記の通りである。

| モデル名 | index個数 |
| --- | --- |
| AMB_Ichigao | 2 |
| AMB_TQ_TimeBord | 1 |
| Aobadai | 4 |
| sibuya_hashira | 1 |
| ST_IronHashira | 2 |
| takatu_st | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 1 |


![HQLEDBord](/program/ssUnity/image/HQLEDBord.png)

【11】：阪急LED

AMBモデルに、「mHqLEDBord」がある場合適用される。

「mHqLEDBord」に定義されたモデルリストの中で、

change_indexで設定したLEDモデルを取得し、

路線別画像データ番号(res_data_index)で、変更する。

mHqLEDBordがあるAMBは、下記の通りである。

| モデル名 | index個数 |
| --- | --- |
| AMB_HQ_YANE0 | 1 |
| AMB_HQ_YANE1 | 1 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |


### AMBの部分的なモデルの適用

この場合、

tex_typeは「0、1、2、20、30、31、32」のみ適用される。

![Ekihyo](/program/ssUnity/image/Ekihyo.png)

【0】：駅表 表

【1】：駅表 裏

【2】：ローカルY軸反転

AMBモデルに、「mEkihyo」がある場合適用される。

「mEkihyo」に定義されたモデルリストの中で、

change_indexで設定した駅表のモデルを取得し、

そのモデルに定義されたマテリアルリストの中で、

mat_indexで設定したマテリアルを取得し、

路線別画像データ番号(res_data_index)で、変更する。

ローカルY軸反転の意味は、180度裏返すようにする。

mEkihyoがあるAMBは、下記の通りである。

| モデル名 | index個数 |
| --- | --- |
| AMB_DenWall | 1 |
| AMB_Ekihyo | 1 |
| AMB_Ekihyo_Reg | 1 |
| AMB_Ekihyo_Tate | 1 |
| AMB_HQ_YANE0 | 2 |
| AMB_HQ_YANE1 | 2 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |
| AMB_MINA_ST_WALL | 1 |
| AMB_Mina_Wall | 1 |
| AMB_MM_Ekihyo | 1 |
| AMB_ShibuyaWall | 1 |
| AMB_ST_WALL | 1 |
| AMB_TQLight | 6 |
| Aobadai | 2 |
| basha_wall | 1 |
| HQ_Ekihyo | 2 |
| ST_IronHashira | 2 |
| ST_IronHashira2 | 2 |
| takatu_st | 1 |
| takatu_st_none | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Obj1 | 2 |
| tq_st_wall2 | 1 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 2 |
| Yane_W2 | 2 |


<br><br>

【20】：ホーム

![HomeNo](/program/ssUnity/image/HomeNo.png)

AMBモデルに、「mHomeNo」がある場合適用される。

「mHomeNo」に定義されたモデルリストの中で、

change_indexで設定したホームのモデルを取得し、

そのモデルに定義されたマテリアルリストの中で、

mat_indexで設定したマテリアルを取得し、

路線別画像データ番号(res_data_index)で、変更する。

mHomeNoがあるAMBは、下記の通りである。

| モデル名 | index個数 |
| --- | --- |
| AMB_HQ_YANE0 | 1 |
| AMB_HQ_YANE1 | 1 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |
| AMB_Ichigao | 2 |
| AMB_TQ_HomeNo | 1 |
| AMB_TQLight | 3 |
| Aobadai | 4 |
| HQ_LEDBORD | 1 |
| takatu_st | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 2 |

<br><br>

![TexUV](/program/ssUnity/image/TexUV.png)

【30】：テクスチャー変更

【31】：UV変更

【32】：メッシュの表示切替

AMBモデルに、「mTexUV」がある場合適用される。

「mTexUV」に定義されたモデルリストの中で、

change_indexで設定したUVモデルを取得し、

そのモデルに定義されたマテリアルリストの中で、

mat_indexで設定したマテリアルを取得する。


1. 【30】：テクスチャー（マテリアル）変更の場合は、そのままテクスチャー変えるだけ

2. 【31】：UV変更の場合は、パラメータ２つで（f1, f2）

    Vectorの(x, y)として更に微調整する。

3. 【32】：メッシュの表示切替の場合

    路線別画像データ番号(res_data_index)が0より大きい場合、表示し

    それ以外の場合、非表示する。

mTexUVがあるAMBは、下記の通りである。

| モデル名 | index個数 |
| --- | --- |
| AMB_SHIBU_YANE | 2 |
| sibuya_hashira | 4 |
| sibuya_hashira_only | 4 |
