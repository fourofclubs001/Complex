import math
import cmath

def pow(z, n):
	
	(module, phase) = cmath.polar(z)
	res = cmath.rect(math.pow(module, n), phase*n) 

	return res

def conjugate(z):

	return z.real - z.imag*1j

def inverse(z):

	return conjugate(z)/math.pow(cmath.polar(z)[0], 2)

# Calculate the solucion of (x^n) = 1
def unitary_roots(n):

	roots = []

	for k in range(0, n):

		roots.append(cmath.rect(1, (2*math.pi*k)/n))

	return roots

# Calculate the primitive roots of 1
def unitary_primitive_roots(n):

	roots = []

	for k in range(0, n):

		if math.gcd(k,n) == 1:

			roots.append(cmath.rect(1, (2*math.pi*k)/n))

	return roots

# Calculate any roots of any number!!!
def roots(z, n):

	roots = []

	for k in range(0, n):

		roots.append(cmath.rect(math.pow(cmath.polar(z)[0], 1/n),
		             (cmath.polar(z)[1]+(2*math.pi*k))/n))

	return roots