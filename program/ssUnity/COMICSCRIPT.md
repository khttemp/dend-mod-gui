# ComicScript読込の解説（SS）

SSのComicScriptの読込について解説する。

## 解説

### index

現在、このスクリプトのindex。

読込まないので、数字の順番を必ず合わせる必要はないので（内部で読込んだ順番で採番するため）

適当に付与しても良いが、あまりおすすめはしない。

### comic_bin

2番目の要素で、読込むコミックスクリプトの数字番号。

ファイルのコミックスクリプトは必ず「comicXXXX.bin」にする必要がある。

### event_type

3番目の要素で、状況によって読込したりスキップしたりするため調整する番号。

  * ストーリー

    タイプが「0、１、２、３、４」のスクリプトを呼び、一番最初に呼ばれたタイプ「０」の、コミックスクリプトを必ず実行する。

  * バトルモード

    タイプが「３、６」のスクリプトを呼び、一番最初に呼ばれたタイプ「６」の、コミックスクリプトを必ず実行する。

  * 試運転

    タイプが「３、５」のスクリプトを呼び、一番最初に呼ばれたタイプ「５」の、コミックスクリプトを必ず実行する。

<hr>

  * タイプ０（Player）

  ストーリーのみのスクリプト。プレイヤー基準で、設定したレールに到達した場合、自動で動作する。<br>
  レール位置を「-1」にすることで、自動で動作することを防ぎ、「GOTO_SCRIPT」で呼び出したいときに使う

  * タイプ１（CPU）

  ストーリーのみのスクリプト。<br>CPU基準で、設定したレールに到達した場合、自動で動作する。

  * タイプ２（Fast）

  ストーリーのみのスクリプト。<br>PlayerまたはCPUのどちらか、設定したレールに到達した場合、自動で動作する。

  * タイプ３（Goal）

  ストーリー、試運転、バトルどこでも使うスクリプト。<br>どのレールで、ゴールを配置するかなどに使う。<br>普段、このスクリプトは「comic2990」になる

  * タイプ４（GoalEvent）

  ストーリーのみのスクリプト。<br>ストーリーでGoalのイベントがあり、ゴールに達したとき、動作させるスクリプト。<br>普段、レール位置は「-1」になる。

  * タイプ５（FreeRunFastEvent）

  試運転のみのスクリプト。<br>一番先に呼ばれる。

  * タイプ６（BtlFastEvent）

  バトルのみのスクリプト。<br>一番先に呼ばれる。

### レール

4番目の要素で、読込んだコミックスクリプトをどのレールで到達したとき発動させるか決める。

レール番号「-1」を除いたスクリプトを【読み込んだ順に】

指定レール番号を過ぎるまでずっと待つ。過ぎた瞬間、スクリプトが実行される。

### オフセット

5番目の要素で、レール位置を基準にどれほどずらすかのoffset

## 内部で設定された、固定番号のスクリプト

### 共通

| 番号 | 説明 |
| --- | --- |
| comic2900 |・無条件でロードされるスクリプト<br>・カウントを数え、スタートさせるスクリプト |
| comic2990 |・無条件でロードされるスクリプト<br>・イベントタイプ「Goal」に使われるスクリプト |
| comic2991 |・無条件でロードされるスクリプト<br>・ゴールしたとき、GOTO_SCRIPTによって呼ばれる<br>・【Finish】の文字表示に使われるスクリプト |
| comic2992 |・無条件でロードされるスクリプト<br>・バトルモード時、自走不能になった車両があるか判断するためのスクリプト
| comic2993 |・バトルモードのみ、無条件でロードされるスクリプト<br>・1Pが自走不能になったとき、【自走不能】と表示し、2P側の勝利にするためのスクリプト |
| comic2994 |・バトルモードのみ、無条件でロードされるスクリプト<br>・2Pが自走不能になったとき、【自走不能】と表示し、1P側の勝利にするためのスクリプト |

<hr>

### JR2000専用イベントのスクリプト

JR2000を選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic3997 | ストーリーや試運転のタービンイベント |
| comic46020 | バトルモードの1Pのタービンイベント |
| comic46021 | バトルモードの2Pのタービンイベント |

<hr>

### KQ2199やKQ21XX専用イベントのスクリプト

KQ2199やKQ21XXを選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic21990、comic21991 | 試運転モードの過給スタート |
| comic21992、comic21993 | ストーリーモードの過給スタート |
| comic46050、comic46052 | バトルモードの1Pの過給スタート |
| comic46051、comic46053 | バトルモードの2Pの過給スタート |

<hr>

### H4050専用イベントのスクリプト

H4050を選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic36996 | H4050のドアを開くイベント |
| comic36997 | H4050のドアを開くイベント＋カメライベント |
| comic36999 | H920に変わる専用イベント |
| comic46010 | バトルモードで1PのH920に変わる専用イベント |
| comic46011 | バトルモードで2PのH920に変わる専用イベント |
| comic46012 | バトルモードで1PのH4050のドアを開くイベント＋カメライベント |
| comic46013 | バトルモードで2PのH4050のドアを開くイベント＋カメライベント |

<hr>

### Mu2000専用イベントのスクリプト

Mu2000を選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic36993 | Mu2000ドアを閉めるイベント |
| comic36994 | Mu2000ドアを開けるイベント |
| comic36995 | Mu2000ドアを開けるイベント＋カメライベント |
| comic46015 | バトルモードで1PのMu2000ドアを開けるイベント |
| comic46016 | バトルモードで2PのMu2000ドアを開けるイベント |
| comic46017 | 2PのMu2000ドアを閉めるイベント |

<hr>

### アーバン専用イベントのスクリプト

アーバンを選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic21000 | 試運転モードで1回目のRB26イベント |
| comic21001 | 試運転モードでTrackBombのイベント |
| comic21002 | 試運転モードで1回目のRB26のクーリングイベント |
| comic21003 | 試運転モードで2回目のRB26イベント |
| comic21004 | 試運転モードで2回目のRB26のクーリングイベント |
| comic21005 | 試運転モードで3回目のRB26イベント |
| comic21006 | ストーリーモードで1回目のRB26イベント |
| comic21007 | ストーリーモードで1回目のRB26のクーリングイベント |
| comic21008 | ストーリーモードで2回目のRB26イベント |
| comic21009 | ストーリーモードで2回目のRB26のクーリングイベント |
| comic21010 | ストーリーモードで3回目のRB26イベント |
| comic21011 | ストーリーモードでTrackBombのイベント |
| comic46030 | バトルモードで1Pの1回目のRB26イベント |
| comic46031 | バトルモードで2Pの1回目のRB26イベント |
| comic46032 | バトルモードで1Pの2回目のRB26イベント |
| comic46033 | バトルモードで2Pの2回目のRB26イベント |
| comic46034 | バトルモードで1Pの3回目のRB26イベント |
| comic46035 | バトルモードで2Pの3回目のRB26イベント |
| comic46036 | バトルモードで1Pの1回目のRB26のクーリングイベント |
| comic46037 | バトルモードで2Pの1回目のRB26のクーリングイベント |
| comic46038 | バトルモードで1Pの2回目のRB26のクーリングイベント |
| comic46039 | バトルモードで2Pの2回目のRB26のクーリングイベント |
| comic46040 | バトルモードで1PのTrackBombのイベント |
| comic46041 | バトルモードで2PのTrackBombのイベント |

<hr>

### Deki専用イベントのスクリプト

Dekiを選んだ車両がある場合、無条件でロードする

| 番号 | 説明 |
| --- | --- |
| comic37000 | 試運転モードで上り調子イベント |
| comic37001 | ストーリーモードで拓海バージョンの上り調子イベント |
| comic37002 | ストーリーモードで啓介バージョンの上り調子イベント |
| comic37005 | 試運転モードで本調子イベント |
| comic37006 | ストーリーモードで拓海バージョンの本調子イベント |
| comic37007 | ストーリーモードで啓介バージョンの本調子イベント |
| comic37010 | 試運転モードで本調子が終わるイベント |
| comic37011 | ストーリーモードで拓海バージョンの本調子が終わるイベント |
| comic37012 | ストーリーモードで啓介バージョンの本調子が終わるイベント |
| comic37015 | 試運転モードで上り調子が終わるイベント |
| comic37016 | ストーリーモードで拓海バージョンの上り調子が終わるイベント |
| comic37017 | ストーリーモードで啓介バージョンの上り調子が終わるイベント |
| comic37020 | ストーリー・試運転モードで2回目以後の本調子イベント |
| comic37021 | ストーリー・試運転モードで2回目以後の本調子が終わるイベント |
| comic37022 | ストーリー・試運転モードで2回目以後の上り調子イベント |
| comic37023 | ストーリー・試運転モードで2回目以後の上り調子が終わるイベント |
| comic46060 | バトルモードで1Pの上り調子イベント |
| comic46061 | バトルモードで2Pの上り調子イベント |
| comic46062 | バトルモードで1Pの本調子イベント |
| comic46063 | バトルモードで2Pの本調子イベント |
| comic46064 | バトルモードで1Pの本調子が終わるイベント |
| comic46065 | バトルモードで2Pの本調子が終わるイベント |
| comic46066 | バトルモードで1Pの上り調子が終わるイベント |
| comic46067 | バトルモードで2Pの上り調子が終わるイベント |
| comic46068 | バトルモードで1Pの2回目以後の本調子イベント |
| comic46069 | バトルモードで2Pの2回目以後の本調子イベント |
| comic46070 | バトルモードで1Pの2回目以後の上り調子イベント |
| comic46071 | バトルモードで2Pの2回目以後の上り調子イベント |
| comic46072 | バトルモードで1Pの2回目以後の本調子が終わるイベント |
| comic46073 | バトルモードで2Pの2回目以後の本調子が終わるイベント |
| comic46074 | バトルモードで1Pの2回目以後の上り調子が終わるイベント |
| comic46075 | バトルモードで2Pの2回目以後の上り調子が終わるイベント |