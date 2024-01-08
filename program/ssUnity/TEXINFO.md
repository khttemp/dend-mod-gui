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

change_indexで設定したLEDボードのテクスチャーを取得し、内部ソースで変更する。


![HQLEDBord](/program/ssUnity/image/HQLEDBord.png)

【11】：阪急LED

AMBモデルに、「mHqLEDBord」がある場合適用される。

change_indexで設定したLEDボードのテクスチャーを取得し、内部ソースで変更する。


### AMBの部分的なモデルの適用

この場合、

tex_typeは「0、1、2、20、30、31、32」のみ適用される。

![Ekihyo](/program/ssUnity/image/Ekihyo.png)

【0】：駅表 表

【1】：駅表 裏

【2】：ローカルY軸反転

AMBモデルに、「mEkihyo」がある場合適用される。

change_index, mat_indexで設定した駅表のテクスチャーを取得し、内部ソースで変更する。

ローカルY軸反転の意味は、180度裏返すようにする。

<br><br>

【20】：ホーム

![HomeNo](/program/ssUnity/image/HomeNo.png)

AMBモデルに、「mHomeNo」がある場合適用される。

change_index, mat_indexで設定した駅表のテクスチャーを取得し、内部ソースで変更する。

<br><br>

![TexUV](/program/ssUnity/image/TexUV.png)

【30】：テクスチャー変更

【31】：UV変更

【32】：メッシュの表示切替

AMBモデルに、「mHomeNo」がある場合適用される。

change_index, mat_indexで設定した駅表のテクスチャーを取得し、内部ソースで変更する。

1. 【30】：テクスチャー変更の場合は、そのままテクスチャー変えるだけ

2. 【31】：UV変更の場合は、パラメータ２つで（f1, f2）

    Vectorの(x, y)として更に微調整する。

3. 【32】：メッシュの表示切替の場合

    路線別画像データ番号が0より大きい場合、表示し

    それ以外の場合、非表示する。
