import numpy as np 
import matplotlib.pyplot as plt 
import sys

# Write a very simple demo for formal solution for scalar case 

def fs_sc_0(z, op, em, I_0):

	ND = len(z)
	dz = np.zeros(ND)
	dz[1:] = z[1:] - z[:-1]
	deltas = np.zeros(ND)
	deltas[1:] = dz[1:] * (op[1:] + op[:-1]) * 0.5

	# This one goes in reverse. I am not sure if this is the best choice. 
	# I am trying to make the marriage between counting from the bottom (physically makes sense)
	# and our general intuition of the optical depth - perhaps this is not even necessary?
	tau = np.zeros(ND)
	tau[1:] = np.cumsum(deltas[::-1][:-1])
	tau = tau[::-1]
	#print (tau)
	#print(deltas)

	S = em/op

	# Pseudo code for looop like solution
	'''
	I = np.zeros(ND)
	I[0] = I_0
	for z in range(1,ND):
		expdt = np.exp(-deltas[z])
		I[z] = I[z-1] * expdt + (1.0 - expdt) * (S[z] + S[z-1]) * 0.5
	'''
	expdt = np.exp(-deltas)
	psi_l = 0.5 * (1.0 - expdt)
	psi_u = 0.5 * (1.0 - expdt)

	# This is how the loop would do it: 
	I = np.zeros(ND)
	I[0] = I_0
	for d in range(1,ND):
		I[d] = I[d-1] * expdt[d] + psi_l[d] * S[d] + psi_u[d-1] * S[d-1]

	return I[-1]

	 

# Example
# z-grid, written geometrically so bottom first 

# Generate very simple z, opacity, emissivity - all scalar

z = np.linspace(0,1000,101) # 10 km spacing 
chi0 = 1.0
H = 100.0
op = chi0 * np.exp(-z/H)
# Let's make S a parabola, to begin with. Units: Kelvin - like 
S = 4000.0 + (z-500) * 4.0 + (z-300)**2.0 * 5E-2

x = np.linspace(-5,5,101)
profile = np.exp(-x**2.0)

em = S * op

I_s = np.zeros(len(x))

for i in range(0,len(x)):
	op_scale = 1E-2 + profile[i]
	I_s[i] = fs_sc_0(z, op * op_scale, em * op_scale, em[0]/op[0])