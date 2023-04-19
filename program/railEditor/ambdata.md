# AMBデータの要素(RS)

## 1. index

レールの番号。RSでCSVで上書きする際、この情報は読み込まない。

## 2. type

未詳

## 3. length

AMBとの距離。距離が指定した範囲内の場合、表示する。

1000が普通。

## 4. rail_no

AMBを置く基準レールNo

## 5. rail_pos

AMBを置く基準レールNoからボーン数分ずらす

## 6. base_pos_x

4と5によって置かれた始点を基準にx軸に平行移動する。下記の図を参照

| デフォルト | base_pos_x (+10) | base_pos_x (-10) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_pos_x_10](/image/amb_base_pos_x_10.png) | ![base_pos_x_-10](/image/amb_base_pos_x_-10.png) |

## 7. base_pos_y

4と5によって置かれた始点を基準にy軸に平行移動する。下記の図を参照

| デフォルト | base_pos_y (+10) | base_pos_y (-5) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_pos_y_10](/image/amb_base_pos_y_10.png) | ![base_pos_y_-5](/image/amb_base_pos_y_-5.png) |

## 8. base_pos_z

4と5によって置かれた始点を基準にz軸に平行移動する。下記の図を参照

| デフォルト | base_pos_z (+10) | base_pos_z (-10) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_pos_z_10](/image/amb_base_pos_z_10.png) | ![base_pos_z_-10](/image/amb_base_pos_z_-10.png) |

## 9. base_dir_x

4と5によって置かれた始点を基準にモデル全体を上下に回転する。下記の図を参照

| デフォルト | base_dir_x (+10) | base_dir_x (-10) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_dir_x_10](/image/amb_base_dir_x_10.png) | ![base_dir_x_-10](/image/amb_base_dir_x_-10.png) |

## 10. base_dir_y

4と5によって置かれた始点を基準にモデル全体を左右に回転する。下記の図を参照

| デフォルト | base_dir_y (+10) | base_dir_y (-10) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_dir_y_10](/image/amb_base_dir_y_10.png) | ![base_dir_y_-10](/image/amb_base_dir_y_-10.png) |

## 11. base_dir_z

4と5によって置かれた始点を基準にモデル全体を横に傾くように回転する。

下記の図を参照

| デフォルト | base_dir_z (+10) | base_dir_z (-10) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![base_dir_z_10](/image/amb_base_dir_z_10.png) | ![base_dir_z_-10](/image/amb_base_dir_z_-10.png) |

## 12. priority

未詳

## 13. fog|child

fog→未詳

child→子モデルの数

## 14. mdl_no

「smf情報」リストのモデル番号。

## 15. pos_x

6番～11番で設定した座標、向きを基準に

x軸に平行移動する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| base_dir_z(-10) | base_dir_z(-10)<br>pos_x(+10) | base_dir_z (-10)<br>pos_x(-10) |
| --- | --- | --- | 
| ![base_dir_z_-10](/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_x_10](/image/amb_base_dir_z_-10_pos_x_10.png) | ![base_dir_z_-10_pos_x_-10](/image/amb_base_dir_z_-10_pos_x_-10.png) |

## 16. pos_y

6番～11番で設定した座標、向きを基準に

y軸に平行移動する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| base_dir_z(-10) | base_dir_z(-10)<br>pos_y(+10) | base_dir_z (-10)<br>pos_y(-5) |
| --- | --- | --- | 
| ![base_dir_z_-10](/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_y_10](/image/amb_base_dir_z_-10_pos_y_10.png) | ![base_dir_z_-10_pos_y_-5](/image/amb_base_dir_z_-10_pos_y_-5.png) |

## 17. pos_z

6番～11番で設定した座標、向きを基準に

z軸に平行移動する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| base_dir_z(-10) | base_dir_z(-10)<br>pos_z(+10) | base_dir_z (-10)<br>pos_z(-10) |
| --- | --- | --- | 
| ![base_dir_z_-10](/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_z_10](/image/amb_base_dir_z_-10_pos_z_10.png) | ![base_dir_z_-10_pos_z_-10](/image/amb_base_dir_z_-10_pos_z_-10.png) |

## 18. dir_x

6番～11番で設定した座標、向きを基準に

モデルを上下に曲げる。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| デフォルト | dir_x (+5) | dir_x (-5) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![dir_x_5](/image/amb_dir_x_5.png) | ![dir_x_-5](/image/amb_dir_x_-5.png) |

## 19. dir_y

6番～11番で設定した座標、向きを基準に

モデルを左右に曲げる。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| デフォルト | dir_y (+5) | dir_y (-5) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![dir_y_5](/image/amb_dir_y_5.png) | ![dir_y_-5](/image/amb_dir_y_-5.png) |

## 20. dir_z

6番～11番で設定した座標、向きを基準に

モデルのカントを設定する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照

| デフォルト | dir_z (+2) | dir_z (-2) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![dir_z_2](/image/amb_dir_z_2.png) | ![dir_z_-2](/image/amb_dir_z_-2.png) |

## 21. dir_x2

6番～11番で設定した座標、向きを基準に

モデル全体を上下に回転する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照(子モデルに適用)

| 子モデル<br>デフォルト | 子モデル<br>dir_x2 (+5) | 子モデル<br>dir_x2 (-5) |
| --- | --- | --- | 
| ![child_default](/image/amb_child_default.png) | ![dir_x2_5](/image/amb_dir_x2_5.png) | ![dir_x2_-5](/image/amb_dir_x2_-5.png) |

## 22. dir_y2

6番～11番で設定した座標、向きを基準に

モデル全体を左右に回転する。

シートの1番目の場合、親モデルの設定、

2番目以後は子モデルの設定になる。

下記の図を参照(子モデルに適用)

| 子モデル<br>デフォルト | 子モデル<br>dir_y2 (+5) | 子モデル<br>dir_y2 (-5) |
| --- | --- | --- | 
| ![child_default](/image/amb_child_default.png) | ![dir_y2_5](/image/amb_dir_y2_5.png) | ![dir_y2_-5](/image/amb_dir_y2_-5.png) |

## 22. dir_z2

6番～11番で設定した座標、向きを基準に

モデル全体を横に傾くように回転する。

下記の図を参照(子モデルに適用)

| 子モデル<br>デフォルト | 子モデル<br>dir_z2 (+5) | 子モデル<br>dir_z2 (-5) |
| --- | --- | --- | 
| ![child_default](/image/amb_child_default.png) | ![dir_z2_5](/image/amb_dir_z2_5.png) | ![dir_z2_-5](/image/amb_dir_z2_-5.png) |

## 23. per

モデルのperを設定する

下記の図を参照

| デフォルト | per(1.5) | dir_z (0.7) |
| --- | --- | --- | 
| ![default](/image/amb_default.png) | ![amb_per_1.5](/image/amb_per_1.5.png) | ![amb_per_0.7](/image/amb_per_0.7.png) |