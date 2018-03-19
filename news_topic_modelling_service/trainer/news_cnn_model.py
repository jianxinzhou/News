# -*- coding: utf-8 -*-
import tensorflow as tf

# news title中的单词序列转化为数字（整数）
# 其中，每一个数字将转化为40个实数构成的序列
# 举例，假设unique words的数量为5，embedding size设为6，
# 现在只对"I like apple"做embedding
#
#  "I like apple"
#  ->
#  [1 2 3 0 0]
#  ->
#  [[[-0.15365833  0.60118073 -0.16130793 -0.51932704  0.27153915  0.20354986]
#    [ 0.15726829 -0.29960257  0.66570419 -0.34065881  0.22046089  0.12072778]
#    [ 0.06263393  0.14344341 -0.02278173 -0.58802676  0.19248533 -0.42651936]
#    [ 0.51072448 -0.03707522 -0.15842998 -0.63320112  0.49047202 -0.46788716]
#    [ 0.51072448 -0.03707522 -0.15842998 -0.63320112  0.49047202 -0.46788716]]]
EMBEDDING_SIZE = 40

# 每个卷积层filter的个数
N_FILTERS = 10

# 卷积核的height（行数）
WINDOW_SIZE = 20

# 第一层与第二层的卷积矩阵
FILTER_SHAPE1 = [WINDOW_SIZE, EMBEDDING_SIZE]
FILTER_SHAPE2 = [WINDOW_SIZE, N_FILTERS]

# 池化窗口大小，height方向
POOLING_WINDOW = 4

# 池化步长，height方向
POOLING_STRIDE = 2

# 学习速率
LEARNING_RATE = 0.05

# n_classes，总的类别数，我们有17个topic
# n_words，unique words的总数，我们的材料中为2127个
def generate_cnn_model(n_classes, n_words):
    """2 layer ConvNet to predict from sequence of words to a class."""
    def cnn_model(features, target):
        # target转化为Tensor("one_hot:0", shape=(?, 17), dtype=int32)
        # 即将代表类别的single number，转化为size为10的由1，0构成的序列
        target = tf.one_hot(target, n_classes, 1, 0)

        # 将数字序列构成的news title，进一步转换为embeddings，
        # 规格为[batch_size, sequence_length,EMBEDDING_SIZE]，
        # 即，[400(样本个数), 100(单个样本word数量), 40(embedding size)]
        # tensor: shape=(?, 100, 40)
        word_vectors = tf.contrib.layers.embed_sequence(features,
            vocab_size=n_words, embed_dim=EMBEDDING_SIZE, scope='words')

        # 扩大1个维度，满足conv2d的输入要求，
        # tensor: shape=(?, 100, 40, 1)
        word_vectors = tf.expand_dims(word_vectors, 3)

        with tf.variable_scope('CNN_layer1'):
            # 对经过预处理的样本word_vectors，进行卷积操作，
            # 100*40 ---(卷积矩阵20*40)---> 81*1
            # tensor: shape=(?, 81, 1, 10)
            conv1 = tf.contrib.layers.convolution2d(
                word_vectors, N_FILTERS, FILTER_SHAPE1, padding='VALID')

            # 激励函数，增加非线性性，
            # tensor: shape=(?, 81, 1, 10)
            conv1 = tf.nn.relu(conv1)

            # Max pooling across output of Convolution+Relu.
            # 81*1 ---(池化窗口大小为4*1，步长2*1(只往height移动))---> shape=(?, 41, 1, 10)
            # tensor: shape=(?, 41, 1, 10)
            pool1 = tf.nn.max_pool(
                conv1,
                ksize=[1, POOLING_WINDOW, 1, 1],
                strides=[1, POOLING_STRIDE, 1, 1],
                padding='SAME')

            # Transpose matrix so that n_filters from convolution becomes width.
            # 转置，(?, 41, 1, 10)--->(?, 41, 10, 1)
            pool1 = tf.transpose(pool1, [0, 1, 3, 2])

        with tf.variable_scope('CNN_layer2'):
            # Second level of convolution filtering.
            # 41*10 ---(卷积矩阵20*10)---> 22*1
            # tensor: shape=(?, 22, 1, 10)
            conv2 = tf.contrib.layers.convolution2d(
                pool1, N_FILTERS, FILTER_SHAPE2, padding='VALID')

            # Max across each filter to get useful features for classification.
            # shape=(?, 22, 1, 10) ---reduce_max---> shape=(?, 1, 10) ---降维---> shape=(?, 10)
            # 如下所示：
            # [ [[22个数字]],         [ [最大的数字],          [ 最大的数字,
            #   [[22个数字]],   --->    [最大的数字],    --->    最大的数字,
            #   ...                    ...                    ...
            #   [[22个数字]] ]          [最大的数字] ]           最大的数字, ]
            pool2 = tf.squeeze(tf.reduce_max(conv2, 1), squeeze_dims=[1])

        # Apply regular WX + B and classification.
        logits = tf.contrib.layers.fully_connected(pool2, n_classes, activation_fn=None)

        # logits, shape=(?, 17)
        # targets, shape(?, 17)
        loss = tf.contrib.losses.softmax_cross_entropy(logits, target)

        train_op = tf.contrib.layers.optimize_loss(
            loss,
            tf.contrib.framework.get_global_step(),
            optimizer='Adam',
            learning_rate=LEARNING_RATE)

        return ({'class': tf.argmax(logits, 1),
                 'prob': tf.nn.softmax(logits)},
                 loss, train_op)

    return cnn_model
