"""
Bag of Words model sentiment analysis.

Part 2 - Recurrent Neural Network
    2a - Without GloVe Features

@author: Zhenye Na
"""


import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import torch.distributed as dist

import time
import os
import sys
import io

from RNN_model import RNN_model


# imdb_dictionary = np.load('../preprocessed_data/imdb_dictionary.npy')
vocab_size = 8000

x_train = []
with io.open('../preprocessed_data/imdb_train.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    line = line.strip()
    line = line.split(' ')
    line = np.asarray(line, dtype=np.int)

    line[line > vocab_size] = 0

    x_train.append(line)
x_train = x_train[0:25000]
y_train = np.zeros((25000,))
y_train[0:12500] = 1


x_test = []
with io.open('../preprocessed_data/imdb_test.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    line = line.strip()
    line = line.split(' ')
    line = np.asarray(line, dtype=np.int)

    line[line > vocab_size] = 0

    x_test.append(line)
y_test = np.zeros((25000,))
y_test[0:12500] = 1


vocab_size += 1

# no_of_hidden_units is 500
# model = BOW_model(vocab_size, 500)
model = torch.load('rnn.model')
model.cuda()

# opt = 'sgd'
# LR = 0.01
opt = 'adam'
LR = 0.001

if(opt == 'adam'):
    optimizer = optim.Adam(model.parameters(), lr=LR)
elif(opt == 'sgd'):
    optimizer = optim.SGD(model.parameters(), lr=LR, momentum=0.9)


batch_size = 200
no_of_epochs = 6
L_Y_train = len(y_train)
L_Y_test = len(y_test)

model.train()

train_loss = []
train_accu = []
test_accu = []


# training
for epoch in range(no_of_epochs):

    model.eval()

    epoch_acc = 0.0
    epoch_loss = 0.0

    epoch_counter = 0

    time1 = time.time()

    I_permutation = np.random.permutation(L_Y_test)

    for i in range(0, L_Y_test, batch_size):

        x_input = [x_test[j] for j in I_permutation[i:i + batch_size]]
        y_input = np.asarray(
            [y_test[j] for j in I_permutation[i:i + batch_size]], dtype=np.int)
        target = Variable(torch.FloatTensor(y_input)).cuda()

        with torch.no_grad():
            loss, pred = model(x_input, target)

        prediction = pred >= 0.0
        truth = target >= 0.5
        acc = prediction.eq(truth).sum().cpu().data.numpy()
        epoch_acc += acc
        epoch_loss += loss.data.item()
        epoch_counter += batch_size

        sequence_length = (epoch+1)*50

    epoch_acc /= epoch_counter
    epoch_loss /= (epoch_counter / batch_size)

    test_accu.append(epoch_acc)

    time2 = time.time()
    time_elapsed = time2 - time1

    print("  ", "%.2f" % (epoch_acc * 100.0), "%.4f" % epoch_loss)

    torch.save(rnn, 'rnn.model')


torch.save(model, 'BOW.model')
data = [train_loss, train_accu, test_accu]
data = np.asarray(data)
np.save('data.npy', data)
