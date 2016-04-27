# coding: utf-8

print 'EXPLICIT'
print '---------------------------------------------------------------------------------------------------'

n = 20
m = 1000
tau = .5/m
h = 1./n
sigma = tau / h**2

def phi(x):
	return 1.0 / (1 + x**2)**2
	
u_cur = [phi(i*h) for i in range(n+1)]
u_up = [0 for dummy_idx in range(n+1)]

for k in range(m):
	for i in range(1,n):
		u_up[i] = sigma * (u_cur[i+1] + u_cur[i-1]) + (1 - 2*sigma - tau) * u_cur[i]
	u_up[0] = (4 * u_up[1] - u_up[2]) / 3.0
	u_up[n] = (4 * u_up[n-1] - u_up[n-2]) / 3.0
		
	u_cur = [u_up[i] for i in range(n+1)]
	
	if ((k+1) % (m / 10) == 0):
		print 'the ', k+1, "'th layer is: ", u_cur
		print
	
print '==================================================================================================='
