"""
HW4: Implement a deep residual neural network for CIFAR100.

Part-1: Build the Residual Network

Due October 5 at 5:00 PM.

@author: Zhenye Na
"""

import torch
import torchvision
import torch.optim
import torch.nn as nn
import torch.utils.data
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms

import argparse

from resnet import ResNet
from utils import *

parser = argparse.ArgumentParser()

# directory
parser.add_argument('--dataroot', type=str, default="../data", help='path to dataset')
parser.add_argument('--ckptroot', type=str, default="../checkpoint/ckpt.t7", help='path to checkpoint')

# hyperparameters settings
parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--momentum', type=float, default=0.9, help='momentum factor')
parser.add_argument('--weight_decay', type=float, default=1e-5, help='weight decay (L2 penalty)')
parser.add_argument('--epochs', type=int, default=50, help='number of epochs to train')
parser.add_argument('--batch_size_train', type=int, default=256, help='training set input batch size')
parser.add_argument('--batch_size_test', type=int, default=256, help='test set input batch size')

# training settings
parser.add_argument('--resume', type=bool, default=False, help='whether re-training from ckpt')
parser.add_argument('--is_gpu', type=bool, default=True, help='whether training using GPU')

# parse the arguments
args = parser.parse_args()




# Load CIFAR100
trainloader, testloader, classes = data_loader(args.dataroot, args.batch_size_train, args.batch_size_test)







def train():
    pass







def main():    

    # resume training from the last time
    if args.resume:
        # Load checkpoint
        print('==> Resuming from checkpoint ...')
        assert os.path.isdir('../checkpoint'), 'Error: no checkpoint directory found!'
        checkpoint = torch.load(args.ckptroot)
        net = checkpoint['net']
        start_epoch = checkpoint['epoch']
    else:
        # start over
        print('==> Building new CNN model ...')
        net = ResNet()


    # For training on GPU, we need to transfer net and data onto the GPU
    # http://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#training-on-gpu
    if args.is_gpu:
        net = net.cuda()
        net = torch.nn.DataParallel(
            net, device_ids=range(torch.cuda.device_count()))
        cudnn.benchmark = True

    # Loss function, optimizer and scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(),
                                lr=args.lr,
                                momentum=args.momentum,
                                weight_decay=args.weight_decay)
    scheduler = torch.optim.ReduceLROnPlateau(optimizer)


    # for epoch in range(10):
    #     train(...)
    #     val_loss = validate(...)
    #     # Note that step should be called after validate()
    #     scheduler.step(val_loss)




if __name__ == '__main__':
    main()