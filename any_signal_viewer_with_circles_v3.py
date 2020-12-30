### By Sha ###
# | My thanks to Tamara Richardson for her help | #

import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np
#import sys

def str2func(s):
    s=s.replace(' ','')
    com=np.array(['+','-','*','/', 'x', '^', '(',')','pi','ln','exp', 'cos', 'sin', 'log', 'abs', 'sqrt'])
    expr=[]
    n=0
    c=0
    cmax=4*len(s)
    while n<len(s):
        c+=1
        if c>cmax:
            raise NameError('Got stuck "' + s[n:] +'"')
        temp=None
        for i in range(1,len(s)-n+1):
            try:
                temp = float(s[n:n+i])
                if n+i == len(s):
                    i += 1
                    raise ValueError('Dirty code to have a float at the end')
            except:
                if temp == None:
                    if s[n:n+1] in com or s[n:n+2] in com or s[n:n+3] in com or s[n:n+4] in com :
                        for j in range(len(com)+1):
                            if j == len(com):
                                raise NameError('Expression "'+s[n:n+4]+'" is not recognized...')
                            elif s[n:n+len(com[j])] == com[j]:
                                expr.append(com[j])
                                n += len(com[j])
                                break
                    else:
                        raise ValueError('Expression "'+s[n:n+4]+'" is not recognized...')
                    break
                else:
                    expr.append(temp)
                    n += i-1
                    break
    for i in range(len(expr)):
        if isinstance(expr[i], str):
            if expr[i]=='^':
                expr[i]='**'
            elif expr[i]=='log':
                expr[i]='np.log10'
            elif expr[i]=='ln':
                expr[i]='np.log'
            elif expr[i] in com and len(expr[i])>1:
                expr[i]='np.'+expr[i]
            else:
                continue
        else:
            continue
    ns=''
    for i in range(len(expr)):
        ns+=str(expr[i])
    return ns

try:
    prec=int(input("Precision (0-100%) : "))
	#prec=int(sys.argv[1])
	if not prec in range(1,101):
		print("\nInvalid input !\nPrecision must be in range 1-100 (%)\nCommand : script.py [precision] [generations]")
		exit(1)
	n_gen=int(input("Generations (too many generations could slow down the process) : "))
	#n_gen=int(sys.argv[2])
	if n_gen<1:
		print("\nInvalid input !\nGenerations must be upper than 0 (1-25 (recommanded))\nCommand : script.py [precision] [generations]")
		exit(1)

except ValueError:
	print("\nInvalid input !\nPrecision and generations must be integers !\nCommand : script.py [precision] [generations]")
	exit(1)


try:
    fxch=int(input("""Functions :
    1:Square singal
    2:Triangle singal
    3:Example #1 [cos(2π+x²)+x²]
    4:Example #2 [cos(2π)-x+2^(x-x*x)]
    5:Personalized function
Choose a function : """))
    #fxch=int(sys.argv[3])
    if not fxch in range(0,6):
        raise(ValueError)
except ValueError:
    print("Invalid input ! Please choose proposed functions. ")
    exit(1)

if fxch==1:
    def f(x):
        x=np.array(x)
        y=np.zeros(np.shape(x))
        cond=(x<1)&(x>-1)
        y[cond]=1
        return y
elif fxch==2:
    def f(x):
        x=np.array(x)
        y=np.zeros(np.shape(x))
        cond=(x<1)&(x>-1)
        y[cond]=1-np.abs(x[cond])
        return y
elif fxch==3:
    def f(x):
        y=np.cos(2*np.pi+x**2)+x**2
        return y
elif fxch==4:
    def f(x):
        y=np.cos(2*x)-x+(2**(x-x*x))
        return y
else:
    fx=input("Function : ")
    fx=str2func(fx)
    def f(x):
        y=eval(fx)
        return y

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
