## 問題2: Python関数からC++関数へのトランスパイラ レポート
### 入力例と結果の確認
```bash
$ python sample.py > result.cpp
```
`result_with_comment.cpp`は`result.cpp`の出力にコメントを加えたものである。
### 追加の仕様
#### PythonのListの要素の型
Pythonではlistに異なる型の要素を格納することが許されているが、C++の配列では禁止されている。変換元のコードでlistに複数のTypeが確認された場合、errorとした。

#### 型変換
intとfloatの間の型変換について、以下を定めた。`t`, `v`はint or floatの変数とする。

|Statement|Specification|
|---|---|
|`t = v` (tは既に定義済み)|tとvは同じ型のみ|
|`t += v`|tとvは同じ型のみ|
|`t -= v`|tとvは同じ型のみ|
|`t *= v`|tとvは同じ型のみ|
|`t /= v`|tはintのみ|
|`t //= v`|t, v共にintのみ|
|`t %= v`|t, v共にintのみ|

#### Div(`/`, `/=`)

|Python|C++|
|---|---|
|`(INT)/(INT)`|`(double)(INT)/(INT)`|
|`(INT)/(FLOAT)`|`(INT)/(DOUBLE)`|
|`(FLOAT)/[=](INT)`|`(DOUBLE)/[=](INT)`|
|`(FLOAT)/[=](FLOAT)`|`(DOUBLE)/[=](DOUBLE)`|

#### Floor Div, Modulo (`//`, `//=`, `%`, `%=`)

|Python|C++|
|---|---|
|`(INT)//[=](INT)`|`(INT)/[=](INT)`|
|`(INT)%[=](INT)`|`(INT)%[=](INT)`|
|Other Operands|Not Supported|

#### Empty List `[]`
今回のトランスパイラでは、配列の要素の参照と書き込みのみを対応した。
Empty List `[]`で初期化した変数は、(1)Type Annotationを付ける、(2)型が分かっている要素をAppendする、(3)引数型が分かっている関数の引数として指定する、といった条件がなければ要素型を確定できない。そのためEmpty List `[]`による初期化を禁止した。

#### Multiple Return Types
Pythonの関数は異なる型の変数をReturnすることができるが、C++では返り値の型を指定しなければならないため、それが不可能である。そのため異なるReturn Typeを禁止した。

### 工夫した点
- `Statement`, `Expression`という基底クラスを継承する形で、文と式のClassを定義した。
- `Expression`のサブクラスはいずれも`cpp_str`というPropertyを持っていて、式の変換に必要な情報をコンストラクタに渡すことでClassの内部でC++のソースに変換している。また、`Expression`のサブクラスのコンストラクタはいずれも`type`を引数に取っていて、Statementにおける型のチェックやC++ソースの生成に使用している。
- `Statement`のサブクラスはいずれも`cpp_str`というPropertyを持っている。
- process_hoge系の関数は、[1]ASTの親子関係の追跡、[2]ASTのノードの情報の抽出・整理を担当していて、いずれも対応するClassのインスタンスを返す。これによりソースの生成部分は`ast`モジュールに関する処理とは切り離される。
- ASTのモジュールの構造・Pythonの文法規則にできるだけ近い形で、これらのサブクラスを定義した。
### 実装しきれなかった機能
- Overflowの検知
    - Pythonのintは任意長だがC++のintは通常32bitのため、Overflowの検知が必要になる。Transpilerでやるべきかは議論の余地があるが、言語間の差異の吸収という意味で追加を検討した機能の１つだった。
- 例外が発生した時に、原因となったStatementの行番号を出力してよりRichなエラーメッセージを出力する機能。
- `()`の冗長さを解消
    - 現在の実装では、`Expression`の`cpp_str`が両端に`()`を付けて返す方針にしていて、Operatorの優先度やStatement側からの`()`関連への追加情報の付与をしていない。そのためASTの分岐がある度に毎回`()`が付属している。