#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np

try:
	prec=int(input("Precision (0-100%) : "))
	if not prec in range(1,101):
		print("\nInvalid input !\nPrecision must be in range 1-100 (%)")
		exit()
	n_gen=int(input("Generations (too many generations could slow down the process) : "))
	if n_gen<1:
		print("\nInvalid input !\nGenerations must be upper than 0 (1-25 (recommanded))")
		exit()

except ValueError:
	print("\nInvalid input !\nPrecision and generations must be integers !")
	exit()

def fig_closed(evt):
    exit(0)

fig,ax=plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True,facecolor='#cccccc')
mng = plt.get_current_fig_manager()
mng.resize(1920,1080)
fig.canvas.mpl_connect('close_event',fig_closed)

ax[0].axis('off')
ax[1].axis('off')
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')

fig.tight_layout(pad=-0.5)

#Global
n_gen+=1
fe=5000
quadlim=150
pas=int(100/prec)

#Left plot
cx=np.zeros((fe,n_gen*2-2))
cy=np.zeros((fe,n_gen*2-2))
c=np.empty(n_gen*2-2,dtype=object)
p=np.empty(n_gen*2-1,dtype=object)
px=np.zeros(n_gen*2-1)
py=np.zeros(n_gen*2-1)
l=np.empty(n_gen*2-2,dtype=object)
lx=np.zeros((fe,n_gen*2-2))
ly=np.zeros((fe,n_gen*2-2))

#Right plot
T=2*np.pi
a=np.zeros(n_gen)
b=np.zeros(n_gen)
fy=np.zeros((fe,n_gen))

#Global
t=np.linspace(-T/2,T/2,fe)
#fx=input("Function : ")

def f(x):
    #y=eval(fx)
    
    x=np.array(x)
    y=np.zeros(np.shape(x))
    # Square #
    cond=(x<1)&(x>-1)
    y[cond]=1
    """# Triangle #
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

for n in range(1,n_gen):
    #calcul des coef
    a[n]=(2/T*quad(an,-T/2,T/2,limit=quadlim)[0])
    b[n]=(2/T*quad(bn,-T/2,T/2,limit=quadlim)[0])
    fy[:,n]=(a[n]*np.cos(n*t*(2*np.pi/T))+b[n]*np.sin(n*t*(2*np.pi/T)))

    #créa des plots
    tmp_cx1=-a[n]*np.sin(n*t)
    tmp_cy1=a[n]*np.cos(n*t)
    tmp_cx2=b[n]*np.cos(n*t)
    tmp_cy2=b[n]*np.sin(n*t)
    tmp_c1,=ax[0].plot(tmp_cx1,tmp_cy1,'-c',linewidth=0.5,zorder=1)
    tmp_c2,=ax[0].plot(tmp_cx2,tmp_cy2,'-c',linewidth=0.5,zorder=1)

    p[2*n-2],=ax[0].plot(0,0,'oy',zorder=2)
    p[2*n-1],=ax[0].plot(0,0,'oy',zorder=2)
    l[2*n-2],=ax[0].plot(0,0,'-g',zorder=1)
    l[2*n-1],=ax[0].plot(0,0,'-g',zorder=1)
    cx[:,(2*n-2)]=tmp_cx1
    cy[:,(2*n-2)]=tmp_cy1
    cx[:,(2*n-1)]=tmp_cx2
    cy[:,(2*n-1)]=tmp_cy2
    c[2*n-2]=tmp_c1
    c[2*n-1]=tmp_c2

p[0].set_color('k')
p[0].set_zorder(3)
p[2*n_gen-2],=ax[0].plot(0,0,'or',zorder=3)
sfy=np.sum(fy,axis=1)

ax[1].plot(t,sfy,'-k')
ax[1].plot(t,f(t),':b')
psfy,=ax[1].plot(-T/2,0,'or',zorder=3)
#############################################
ylimax1=ax[1].get_ylim()
ax[0].set_ylim(ylimax1[0]+(50*ylimax1[0]/100),ylimax1[1]+(50*ylimax1[1]/100))

lpl,=ax[0].plot(0,0,'-b')
rpl,=ax[1].plot(0,0,'-b')
lpl.set_xdata(t)
rpl.set_xdata(t)

ax[0].plot(np.sum(cx,axis=1),a[0]+np.sum(cy,axis=1),'-k',zorder=0)

try:
    for n in range(0,fe,pas):
        for m in range(2*n_gen-2):
            px[m]=np.sum(cx[n,:m])
            py[m]=np.sum(cy[n,:m])+a[0]
            p[m].set_xdata(px[m])
            p[m].set_ydata(py[m])
            l[m].set_xdata([np.sum(cx[n,:m]),np.sum(cx[n,:m+1])])
            l[m].set_ydata([np.sum(cy[n,:m])+a[0],np.sum(cy[n,:m+1])+a[0]])
            c[m].set_xdata(cx[:,m]+px[m])
            c[m].set_ydata(cy[:,m]+py[m])
        
        px[2*n_gen-2]=np.sum(cx[n,:])
        py[2*n_gen-2]=a[0]+np.sum(cy[n,:])
        p[2*n_gen-2].set_xdata(px[2*n_gen-2])
        p[2*n_gen-2].set_ydata(py[2*n_gen-2])
        
        psfy.set_xdata(t[n])
        psfy.set_ydata(py[2*n_gen-2])

        xlimax0=ax[0].get_xlim()
        tlpl=[px[2*n_gen-2],xlimax0[1]]
        lpl.set_xdata(tlpl)
        lpl.set_ydata(py[2*n_gen-2])
        trpl=[xlimax0[0],t[n]]
        rpl.set_xdata(trpl)
        rpl.set_ydata(py[2*n_gen-2])

        plt.pause(0.001)
    plt.show()

except KeyboardInterrupt:
	print("Stopped !")
	exit(0)
