# Evaluate learned word representation on word similarity task
import sys
import os
import logging
import argparse
import numpy as np
from fasttext import load_model
from scipy.stats import spearmanr
from tqdm import tqdm

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    parser = argparse.ArgumentParser(description='Evaluate word representations')
    parser.add_argument('--input', type=str, default='wordsim-296.txt', help='Evaluation data path')
    parser.add_argument('--model_path', type=str, default='model.bin', help='Trained model path')
    parser.add_argument('--task', type=str, default='word_similarity', help='Evaluation task {word_similarity, word_analogy}')
    args = parser.parse_args()

    logging.info('Start evaluation {} on task {}'.format(args.model_path,
                                                         args.task))
    model = load_model(args.model_path)
    eval_data = open(args.input, 'r')
    pred_score = []
    human_score = []
    for line in tqdm(eval_data):
        w1, w2, human = line.split()
        emb1, emb2 = model[w1], model[w2]
        pred = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        human_score.append(human)
        pred_score.append(pred)
    corr = spearmanr(human_score, pred_score)
    logging.info('Finish evaluation. Score = {}'.format(corr))

if __name__ == '__main__':
    main()
