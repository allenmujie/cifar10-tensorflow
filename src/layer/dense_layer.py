# -*- encoding: utf8 -*-
# author: ronniecao
import numpy
import tensorflow as tf


class DenseLayer:
    
    def __init__(self, input_shape, hidden_dim, activation='relu', dropout=False, 
                 keep_prob=None, batch_normal=False, name='dense'):
        # params
        self.input_shape = input_shape
        self.hidden_dim = hidden_dim
        self.activation = activation
        self.dropout = dropout
        self.batch_normal = batch_normal
        # weight
        self.W = tf.Variable(
            initial_value=tf.random_normal(
                shape=[self.input_shape[1], self.hidden_dim],
                mean=0.0, stddev=0.01),
            name='W_%s' % (name))
        # bias
        self.b = tf.Variable(
            initial_value=tf.zeros(
                shape=[self.hidden_dim]),
            name='b_%s' % (name))
        # gamma
        self.epsilon = 1e-5
        if self.batch_normal:
            self.gamma = tf.Variable(
                initial_value=tf.random_normal(
                    shape=[self.hidden_dim]),
            name='gamma_%s' % (name))
        # keep_prob
        if self.dropout:
            self.keep_prob = keep_prob
        
    def get_output(self, input):
        # calculate input_shape and output_shape
        self.output_shape = [self.input_shape[0], self.hidden_dim]
        # hidden states
        intermediate = tf.matmul(input, self.W)
        # batch normalization
        if self.batch_normal:
            mean, variance = tf.nn.moments(intermediate, axes=[0])
            self.hidden = tf.nn.batch_normalization(
                intermediate, mean, variance, self.b, self.gamma, self.epsilon)
        else:
            self.hidden = intermediate + self.b
        # dropout
        if self.dropout:
            self.hidden = tf.nn.dropout(self.hidden, keep_prob=self.keep_prob)
        # activation
        if self.activation == 'relu':
            self.output = tf.nn.relu(self.hidden)
        elif self.activation == 'tanh':
            self.output = tf.nn.tanh(self.hidden)
        elif self.activation == 'softmax':
            self.output = tf.nn.softmax(self.hidden)
        
        return self.output