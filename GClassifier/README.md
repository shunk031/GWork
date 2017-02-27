# GClassifier

ナイーブベイズ分類器を用いてニュース記事を分類する。

## Dataset

* [Gunosy news articles](https://gunosy.com/)  
  2017年2月23日現在の「エンタメ」・「スポーツ」・「おもしろ」・「国内」・「海外」・「コラム」・「IT・科学」・「グルメ」の8カテゴリから記事を収集した。

## Result

5-fold cross validationを用いて分類器の評価を行った。

| method                 | accuracy |
|------------------------|----------|
| use only nouns         | 0.8917   |
| word 2-gram            | 0.8385   |
| word 3-gram            | 0.8348   |
