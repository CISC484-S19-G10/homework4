#!/usr/bin/python3

import math
import scipy.stats
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    #required args
    parser.add_argument('input_path', metavar='I',\
                        help='the path to the data file')
    parser.add_argument('n_distrib', metavar='K', type=int,\
                        help='the given data will be modeled as K Gaussian distributions')

    return parser.parse_args()

args = parse_args()
    
lines = []
with open(args.input_path) as f:
    lines = f.read().splitlines()

data = [float(d) for d in lines]

k_num = args.n_distrib
n = len(data)

import matplotlib.pyplot as p
zeros = [0 for i in data]

#g = p.scatter(data, zeros)
#p.show(g)


#Init

theta = [(random.uniform(0,20), random.uniform(1,5**2)) for i in range(0,k_num)]

alpha = [(1/k_num) for i in range(0,k_num)]

w = [[0 for k in range(0,k_num)] for i in data]


#print(n)

#theta[1] is var
def gaussian(point, theta):
    expd = math.exp(- ( (point-theta[0])**2) / (2*theta[1]) )
    scale = 1/(math.sqrt(2*math.pi*(theta[1])))
    return scale*expd

#Expectation
def expectation():
    #print(w[10])
    #print(theta)

    for i in range(0,n):
        #print(i)
        denom = [0 for z in range(0,k_num)]

        for k in range(0,k_num):
            pdf = gaussian(data[i], theta[k])
            denom[k] = pdf*alpha[k]
            
        
        total = sum(denom)

        #print(w[i])   
        w[i] = [(denom[k]/total) for k in range(0,k_num)]    
   # print(data[980],(w[980]))

    
    #print((data[0], w[0], theta))
        #print(w)        

#Maximization
def maximization():
    #Weighted Ns
    n_k = [0 for k in range(0,k_num)]

    for point in w:
        for k in range(0,k_num):
            n_k[k]+=point[k]

    #print(n_k)

    #print(n_k)
    

    #alphas
    alpha = [(n_k[k]/n) for k in range(0,k_num)]
    #print(alpha)

    #print(data[0], w[0], theta)
    #print(n_k)

    #print(alpha)

    #print(n_k)
    #means
    #print(theta)
    #print(n_k)
    for k in range(0,k_num):

        k_scale = 1/n_k[k]
        #Mean
        weighted_mean_sum = 0
        for i in range(0,n):
            weighted_mean_sum+=w[i][k]*data[i]

        #print(weighted_mean_sum)
        #print(weighted_mean_sum)
        new_mean = k_scale*weighted_mean_sum
        #print(new_mean)


        #Var
        weighted_var_sum = 0
        for i in range(0,n):
            weighted_var_sum += w[i][k] * ((data[i]-theta[k][0])**2)

        new_var = k_scale*weighted_var_sum 
        #new_var = 1

        theta[k] = (new_mean, new_var)

    #print(theta)
    #print("-----")

def find_log_likelihood(data, weights, param_weights, params):
    EPSILON = .00001
    log_likelihood = 0

    for i, datum in enumerate(data):

        #assume varience is 1 for now
        log_likelihood -= math.log(math.sqrt(1 * 2 * math.pi))
        
        total = 0
        for k, (mean, varience) in enumerate(params):
            #total += expected_weight(datum, mean, params) * (datum - mean) ** 2
            total += weights[i][k] * (datum - mean) ** 2

        log_likelihood -= total / (2 * 1)

    return log_likelihood

for i in range(0,50):
    #print(theta)
    #print("Expect")
    expectation()
    #print("Maximize")
    maximization()
    #print(theta)
    #print(theta)


import scipy.stats as stats
import numpy as np

likelihoods = []
for t in theta:
    mu = t[0]
    sigma = math.sqrt(t[1])

    x = np.linspace(mu - 6*sigma, mu+6*sigma, 100)
    #p.plot(x, stats.norm.pdf(x, mu, sigma))
    #p.xlabel('value')
    #p.ylabel('predicted frequency')

#p.show()

print(len(data))
print(theta)
print('e^{}'.format(find_log_likelihood(data, w, alpha, theta)))
