# -*- coding: utf-8 -*-
import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = '../model/'
DATA_SET_FILE = '../data/labeled_news.csv'
VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'
MAX_DOCUMENT_LENGTH = 100
N_CLASSES = 17

# 迭代次数
STEPS = 200

def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # 导入训练数据集和测试数据集，
    # 数据集的格式为：topic，title，description，source
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0:400]
    test_df = df.drop(train_df.index)

    # x代表news的title，y代表news的topic（类别）
    x_train = train_df[1]
    y_train = train_df[0]
    x_test = test_df[1]
    y_test = test_df[0]

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    # x_train经过fit_transform后转化为以下形式：
    # array([[   1,    2,    3, ...,    0,    0,    0],
    #       [   1,    8,    9, ...,    0,    0,    0],
    #       [  17,    1,   18, ...,    0,    0,    0],
    #       ...,
    #       [2112, 2113, 1417, ...,    0,    0,    0],
    #       [2120,   49, 2121, ...,    0,    0,    0],
    #       [2123, 1895, 2124, ...,    0,    0,    0]])
    # 每一条news的title由字符串序列转换为数字序列，
    # 400条news的title转变为400个数字序列
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    # 总共有2127个unique words
    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    # 将unique words的总数以及vocab_processor存到文件中
    with open(VARS_FILE, 'w') as f:
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # 构建模型
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # 训练
    classifier.fit(x_train, y_train, steps=STEPS)

    # 对测试集进行预测，评估泛化性能
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.run(main=main)
