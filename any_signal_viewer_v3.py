### By Sha ###
# | My thanks to Tamara Richardson for her help | #

import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np


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
	t_defil=float(input("Time between generations (around 0.05s) : "))
	if t_defil>1:
		print("\nInvalid input !\Scroll time is too high (scroll time must be less than or equal to 1)")
		exit(1)
	n_gen=int(input("Generations (too many generations could slow down the process) : "))
	if n_gen<1:
		print("\nInvalid input !\nGenerations must be upper than 0 (between 1 and 25 (recommanded))")
		exit(1)

except ValueError:
	print("\nInvalid input !\Scroll time must be a float number !\nGenerations must be integers !")
	exit(1)

try:
    fxch=int(input("""Functions :
    1:Square singal
    2:Triangle singal
    3:Example #1 [cos(2π+x²)+x²]
    4:Example #2 [cos(2π)-x+2^(x-x*x)]
    5:Personalized function
Choose a function : """))
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

fe=5000
T=2*np.pi
quadlim=100

t=np.linspace(-T/2,T/2,fe)
a=np.zeros(n_gen)
b=np.zeros(n_gen)
fy=np.zeros((fe,n_gen))

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
    exit(0)

fig=plt.figure()
mng = plt.get_current_fig_manager()
mng.resize(1920,1080)
fig.canvas.mpl_connect('close_event',fig_closed)

for n in range(1,n_gen):
    a[n]=(2/T*quad(an,-T/2,T/2,limit=quadlim)[0])
    b[n]=(2/T*quad(bn,-T/2,T/2,limit=quadlim)[0])
    fy[:,n]=(a[n]*np.cos(n*t*(2*np.pi/T))+b[n]*np.sin(n*t*(2*np.pi/T)))

plt.plot(t,f(t),'-b',label="f(x)")
pltsfy,=plt.plot(t,np.sum(fy,axis=1),'--r')

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
