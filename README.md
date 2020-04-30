# Chinese Word Representation

Most of the popular methods used for learning word representations only consider the external context of an input word, and ignore its internal structure. These techniques are limited for learning effective representations of Chinese words, whose subword and subcharacter components can also be semantically important. This project generates and compares Chinese word representations that exploit different internal structures of words and characters. 

## Data
* Training data: [Chinese Wikipedia dump](https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2)
* Evalution data: Chinese Word similarity tasks [`wordsim-240` and `wordsim-296`](https://github.com/HKUST-KnowComp/JWE/tree/master/evaluation)
