# Chinese Word Representation

Most of the popular methods used for learning word representations only consider the external context of words and ignore their internal structures. These techniques are limited for learning effective representations of Chinese words, the internal structures of which can also be semantically important. This project generates and compares Chinese word representations that exploit different subword and subcharacter components including characters, graphical components, and Wubi codes.

## Data
* Training corpus: [Chinese Wikipedia dump](https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2)
* Evalution data: Chinese Word similarity tasks [`wordsim-240` and `wordsim-296`](https://github.com/HKUST-KnowComp/JWE/tree/master/evaluation)
* Dictionaries: `subchar_dict/graphical_dict.p` and `subchar_dict/wubi_dict.p` contain dictionaries that map Chinese characters to graphical components and Wubi codes. These two file can be used to convert characters into subcharacter components or to train joint word embeddings (JWE).  

## Quick Start
### Install Packages
Run `pip install -r requirements.txt`

### Preprocess Wiki Dump:
After downloading the latest Chinese Wikipedia dump from the link above, use `preprocess_wiki.py` to
* Convert traditional Chinese to simplified Chinese
* Remove non-Chinese characters including punctuations and spaces
* Split sentences into words separated by space
* Convert xml into txt file

Parameters:
```python
input           # Wiki dump XML file path
output          # Preprocessed txt file path
```

### Convert Tokenized Wiki Text to Subcharacter Components
Use `convert_subchar.py` to convert tokenized text into subcharacter components (graphical components or Wubi codes) while keeping the delimeters between words
Parameters:
```python
input           # Tokenized txt file path
output          # Subcharacter output txt file path
subchar         # Subcharacter types {radical, wubi}
```

### Learn Word Representations
#### CBOW or skipgram
Use `python train.py` to train continuous-bag-of-words (CBOW) or skipgram models using `fastText`
Parameters:
```python
input           # Training txt file path
model_path      # Trained model path
model           # Model type {cbow, skipgram}
dim             # Size of the word vectors
ws              # Size of the context window
epoch           # Number of epochs
minn            # Minimum length of subword ngram
maxn            # Maximal length of subword ngram
```
Note: Depending on whether the training corpus contains characters, graphical components, or Wubi codes, word length may vary significantly, and different `minn` and `maxn` should be chosen accordingly. When `maxn = 0`, no subword information will be considered. 

#### JWE
For jointly learning word vectors, character vectors and subcharacter vectors, see [JWE](https://github.com/HKUST-KnowComp/JWE/)

### Evaluate
#### CBOW or skipgram
Use `eval.py` to evaluate the trained CBOW and skipgram models on word similarity tasks. The script will first compute the cosine similarity between each pair of words, and then compute the Spearman correlation coefficient between cosine similarity and human-labeled scores as final evaluation metric for model performance.
Parameters:
```python
input           # Evaluation data file path
model_path      # Trained model path
output          # Predicted score output txt file path
subword         # Subword type {character, graphical, wubi}
```