# Chinese Word Representation

Most of the popular methods used for learning word representations only consider the external context of an input word, and ignore its internal structure. These techniques are limited for learning effective representations of Chinese words, whose subword and subcharacter components can also be semantically important. This project generates and compares Chinese word representations that exploit different internal structures of words and characters. 

## Data
* Training data: [Chinese Wikipedia dump](https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2)
* Evalution data: Chinese Word similarity tasks [`wordsim-240` and `wordsim-296`](https://github.com/HKUST-KnowComp/JWE/tree/master/evaluation)

## Quick Start
### Install Packages
Run `pip install -r requirements.txt`

### Preprocess Wiki Dump
After downloading the latest Chinese Wikipedia dump from the link above, run `python preprocess_wiki.py --input zhwiki-latest-pages-articles.xml.bz2 --output zhwiki_tokenized.txt` to
* Convert traditional Chinese to simplified Chinese
* Remove non-Chinese characters including punctuations and spaces
* Split sentences into words separated by space
* Convert xml into txt file

### Convert Tokenized Wiki Text to Subcharacter Components
* Convert text to Wubi codes: run `python convert_subchar.py --input zhwiki_tokenized.txt --output zhwiki_wubi.txt --subchar wubi`
* Convert text to radicals and subcharacter components: run `python convert_subchar.py --input zhwiki_tokenized.txt --output zhwiki_radical.txt --subchar radical`

### Learn Word Representations

### Evaluate