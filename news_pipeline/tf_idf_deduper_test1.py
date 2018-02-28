# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer

doc1 = "I like apples. I like oranges too"
doc2 = "I love apples. I hate doctors"
doc3 = "An apple a day keeps the doctor away"
doc4 = "Never compare an apple to an orange"

documents = [doc1, doc2, doc3, doc4]

tfidf = TfidfVectorizer().fit_transform(documents)
pairwise_sim = tfidf * tfidf.T

print pairwise_sim.A

# Output:
#
# [[ 1.          0.12693309  0.          0.        ]
#  [ 0.12693309  1.          0.          0.        ]
#  [ 0.          0.          1.          0.27993128]
#  [ 0.          0.          0.27993128  1.        ]]
#
# 以上矩阵中的数值是make sence的，解释如下：
#
# 位置(0,0)数值为1，代表doc1和doc1的相似度
# 位置(0,1)数值为0.12693309，代表doc1和doc2的相似度
# 位置(0,2)数值为0，代表doc1和doc3的相似度
# 位置(0,3)数值为0，代表doc1和doc4的相似度
# 同理，(1,0)数值为0.12693309，代表doc2和doc1的相似度
#
# 因此对新的news做查重的时候，可以只看第一行，
# 把新的news设置成第一行第一个，把mongodb中已存的新闻设置成第一行其余位置，
# 那么，对这条news的查重可以转换为判断其余位置的值是否大于设定的阈值（一般超过0.8，可以认为是同一篇文章）
