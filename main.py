import math
import scipy.stats
lines = []
with open('./em_data.txt') as f:
    lines = f.read().splitlines()

data = [float(d) for d in lines]

k_num = 3
n = len(data)




#Init
mean_init = 0
var_init = 1

theta = [(mean_init, var_init) for i in range(0,k_num)]

alpha = [(1/k_num) for i in range(0,k_num)]

w = [[0 for k in range(0,k_num)] for i in data]
print(theta)

#Expectation

def expectation(w, data, theta):
    for i in range(0,n):
        denom = [0 for z in range(0,k)]

        for k in range(0,k_num):
            dist = scipy.stats.norm(theta[k][0], theta[k][1])
            pdf = dist.pdf(data[i])

            denom[k] = pdf*alpha[k]

        total = sum(denom)    
        w[i] = [denom[k]/total for k in denom]

    return w
            



#Maximization