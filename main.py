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

n_k = [0 for k in range(0,k_num)]

#print(n)

def gaussian(point, theta):
    expd = math.exp(- ( (point-theta[0])**2) / (2*theta[1]**2) )
    scale = 1/(math.sqrt(2*math.pi*(theta[1]**2)))
    return scale*expd

#Expectation
def expectation():
    #print(w[10])

    for i in range(0,n):
        #print(i)
        denom = [0 for z in range(0,k_num)]

        for k in range(0,k_num):
            pdf = gaussian(data[i], theta[k])

            denom[k] = pdf*alpha[k]
            

        total = sum(denom)

        #print(w[i])   
        w[i] = [denom[k]/total for k in range(0,k_num)]    
        #print(w)        

#Maximization
def maximization():
    #Weighted Ns
    for point in w:
        for k in range(0,k_num):
            n_k[k]+=point[k]

    #print(n_k)

    

    #alphas
    alpha = [n_k[k]/n for k in range(0,k)]

    #means
    for k in range(0,k_num):
        k_scale = 1/n_k[k]
        #Mean
        weighted_mean_sum = 0
        for i in range(0,n):
            weighted_mean_sum+=w[i][k]*data[i]
        
        new_mean = k_scale*weighted_mean_sum

        #Var
        weighted_var_sum = 0
        for i in range(0,n):
            weighted_var_sum += w[i][k] * ((data[i]-theta[k][0])**2)

        new_var = k_scale*weighted_var_sum 

        theta[k] = (new_mean, new_var)


for i in range(0,10):
    #print(theta)
    #print("Expect")
    expectation()
    #print("Maximize")
    maximization()
    print(theta)