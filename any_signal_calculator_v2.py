#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np

try:
	t_defil=float(input("Time between generations (around 0.05s) : "))
	if t_defil>1:
		print("\nInvalid input !\Scroll time is too high (scroll time must be less than or equal to 1)")
		exit()
	n_gen=int(input("Generations (too many generations could slow down the process) : "))
	if n_gen<1:
		print("\nInvalid input !\nGenerations must be upper than 0 (between 1 and 25 (recommanded))")
		exit()

except ValueError:
	print("\nInvalid input !\Scroll time must be a float number !\nGenerations must be integers !")
	exit()

fe=5000
T=2*np.pi
quadlim=100

t=np.linspace(-T/2,T/2,fe)
a=np.zeros(n_gen)
b=np.zeros(n_gen)
fy=np.zeros((fe,n_gen))
fx=input("Function : ")

def f(x):
    y=eval(fx)
    """x=np.array(x)
    y=np.zeros(np.shape(x))
    # Square #
    cond=(x<1)&(x>-1)
    y[cond]=1
    # Triangle #
    cond=(x<1)&(x>-1)
    y[cond]=1-np.abs(x[cond])"""
    return y

def an(x):
    y=f(x)*np.cos(n*x*((2*np.pi)/T))
    return y

def bn(x):
    y=f(x)*np.sin(n*x*((2*np.pi)/T))
    return y

a[0]=1/T*quad(f,-T/2,T/2,limit=quadlim)[0]
b[0]=0
fy[:,0]+=a[0]

def fig_closed(evt):
    exit()

fig=plt.figure()
mng = plt.get_current_fig_manager()
mng.resize(1920,1080)
fig.canvas.mpl_connect('close_event',fig_closed)

for n in range(1,n_gen):
    a[n]=(2/T*quad(an,-T/2,T/2,limit=quadlim)[0])
    b[n]=(2/T*quad(bn,-T/2,T/2,limit=quadlim)[0])
    fy[:,n]=(a[n]*np.cos(n*t*(2*np.pi/T))+b[n]*np.sin(n*t*(2*np.pi/T)))

plt.plot(t,f(t),'-b',label="f(x)")
pltsfy,=plt.plot(t,np.sum(fy,axis=1),'-r')

try:
    for n in range(0,n_gen+1):
        pltsfy.set_label("Fourier series of f(x) with "+str(n)+" sine waves")
        fig.legend(loc=9,fontsize='x-large')
        pltsfy.set_ydata(np.sum(fy[:,:n],axis=1))
        plt.pause(t_defil)
    
    plt.show()

except KeyboardInterrupt:
	print("Stopped !")
	exit(0)
