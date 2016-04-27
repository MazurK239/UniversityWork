# coding: utf-8

print 'IMPLICIT'
print '---------------------------------------------------------------------------------------------------'

n = 20
m = 1000
tau = .5/m
h = 1./n
sigma = tau / h**2

def phi(x):
	return 1.0 / (1 + x**2)**2
	
u_prev = [phi(i*h) for i in range(n+1)]
u_cur = [0 for dummy_idx in range(n+1)]

for k in range(1,m+1):
	alpha = [0, 2*sigma / (2*sigma + 3*tau + 3)]
	beta = [0, 3*u_prev[1] / (2*sigma + 3*tau + 3)]
	for i in range(2,n):
		alpha.append(sigma / (sigma * (2 - alpha[i-1]) + tau + 1))
		beta.append((sigma * beta[i-1] + u_prev[i]) / (sigma * (2 - alpha[i-1]) + tau + 1))
		
	u_cur[n] = ((4 - alpha[n-2]) * beta[n-1] - beta[n-2]) / (3 + alpha[n-1] * (alpha[n-2] - 4))
	for i in range(n-1, 0, -1):
		u_cur[i] = alpha[i] * u_cur[i+1] + beta[i]
	u_cur[0] = (4 * u_cur[1] - u_cur[2]) / 3.
	
	u_prev = [u_cur[i] for i in range(n+1)]
	
	if (k % (m / 10) == 0):
		print 'the ', k, "'th layer is: ", u_cur
		print

print '==================================================================================================='
