#!/usr/bin/env python3

import matplotlib.pyplot as plt
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
    exit()

fig,ax=plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True,facecolor='#cccccc')
mng = plt.get_current_fig_manager()
mng.resize(1920,1080)
fig.canvas.mpl_connect('close_event',fig_closed)

ax[0].axis('off')
ax[1].axis('off')
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')

fig.tight_layout(pad=-0.5)

ax[0].set_ylim([-1.5,1.5])
if n_gen <= 2:
	ax[0].set_xlim([-1.6,1.6])

n_gen=n_gen+1
fe=5000
pas=int(100/prec)

t=np.linspace(0,1,fe)

cx=np.zeros((fe,n_gen))
cy=np.zeros((fe,n_gen))
c=[]
p=[]
px=np.zeros(n_gen)
py=np.zeros(n_gen)
l=[]
lx=np.zeros((fe,n_gen))
ly=np.zeros((fe,n_gen))

for n in range(1,n_gen):
	tmp_p,=ax[0].plot(0,0,'ob',zorder=2)
	tmp_cx=np.cos(2*np.pi*(2*n-1)*t)/(2*n-1)
	tmp_cy=np.sin(2*np.pi*(2*n-1)*t)/(2*n-1)
	tmp_c,=ax[0].plot(tmp_cx,tmp_cy,':c',linewidth=0.5,zorder=1)
	tmp_l,=ax[0].plot(0,0,'-y',zorder=3)
	
	cx[:,n-1]=tmp_cx
	cy[:,n-1]=tmp_cy
	c.append(tmp_c)
	p.append(tmp_p)
	l.append(tmp_l)

lh1,=ax[0].plot(0,0,'-b')
lh2,=ax[1].plot(0,0,'-b')

cfx=np.sum(cx,axis=1)
cfy=np.sum(cy,axis=1)
cf,=ax[0].plot(cfx,cfy,'-k',zorder=4)
pf,=ax[0].plot(0,0,'or',zorder=5)
lf,=ax[0].plot(0,0,'-y',zorder=3)

xlimax0=list(ax[0].get_xlim())
x=np.linspace(-1,2*xlimax0[1],fe)
ph=0

curve,=ax[1].plot(0,0,'-k')
pc,=ax[1].plot(-1,0,'or')
curve.set_xdata(x)
try:
	for n in range(0,fe,pas):
		y=0
		for m in range(1,n_gen-1):
			px[m]=np.sum(cx[n,:m])
			py[m]=np.sum(cy[n,:m])
			
			p[m].set_xdata(px[m])
			p[m].set_ydata(py[m])
			l[m].set_xdata(t*(px[m]-px[m-1])+px[m-1])
			l[m].set_ydata(t*(py[m]-py[m-1])+py[m-1])
			c[m].set_xdata(cx[:,m]+px[m])
			c[m].set_ydata(cy[:,m]+py[m])
		
		for m in range(1,n_gen):
			y=y+(np.sin(2*np.pi*(2*m-1)*(x-ph)-np.pi)/(2*m-1))
		
		lf.set_xdata(t*(np.sum(cx[n,:n_gen-1])-px[n_gen-2])+px[n_gen-2])
		lf.set_ydata(t*(np.sum(cy[n,:n_gen-1])-py[n_gen-2])+py[n_gen-2])
		
		pf.set_xdata(np.sum(cx[n,:n_gen-1]))
		pf.set_ydata(np.sum(cy[n,:n_gen-1]))

		ph=ph+(pas/fe)
		curve.set_ydata(y)
		pc.set_ydata(np.sum(cy[n,:n_gen-1]))

		tl1=[np.sum(cx[n,:n_gen-1]),xlimax0[1]]
		lh1.set_xdata(tl1)
		lh1.set_ydata(np.sum(cy[n,:n_gen-1]))

		tl2=[xlimax0[0],-1]
		lh2.set_xdata(tl2)
		lh2.set_ydata(np.sum(cy[n,:n_gen-1]))
		
		plt.pause(0.001)
	plt.show()

except KeyboardInterrupt:
	print("Stopped !")
	exit(0)
