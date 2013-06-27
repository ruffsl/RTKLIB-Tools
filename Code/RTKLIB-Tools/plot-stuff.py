'''
Created on Jun 26, 2013

@author: ruffin
'''

if __name__ == '__main__':
    pass

# Import everything from matplotlib (numpy is accessible via 'np' alias)
from pylab import *

# Create a new figure of size 8x6 points, using 80 dots per inch
# figure(figsize=(8,6), dpi=80)
figure(figsize=(10,6), dpi=80)

# Create a new subplot from a grid of 1x1
subplot(1,1,1)

X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
C,S = np.cos(X), np.sin(X)

# Plot cosine using blue color with a continuous line of width 1 (pixels)
# plot(X, C, color="blue", linewidth=1.0, linestyle="-")
# Plot sine using green color with a continuous line of width 1 (pixels)
# plot(X, S, color="green", linewidth=1.0, linestyle="--")
plot(X, C, color="blue", linewidth=2.5, linestyle="-")
plot(X, S, color="red",  linewidth=2.5, linestyle="-")

# Set x limits
# xlim(-4.0,4.0)
# Set y limits
# ylim(-1.0,1.0)
xlim(X.min()*1.1, X.max()*1.1)
ylim(C.min()*1.1, C.max()*1.1)

ax = gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

# Set x ticks
# xticks(np.linspace(-4,4,9,endpoint=True))
# Set y ticks
# yticks(np.linspace(-1,1,5,endpoint=True))
# xticks( [-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
# yticks([-1, 0, +1])
xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
       [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

yticks([-1, 0, +1],
       [r'$-1$', r'', r'$+1$'])

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65 ))

plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
plot(X, S, color="red",  linewidth=2.5, linestyle="-", label="sine")

legend(loc='upper left')

t = 2*np.pi/3
plot([t,t],[0,np.cos(t)], color ='blue', linewidth=2.5, linestyle="--")
scatter([t,],[np.cos(t),], 50, color ='blue')

annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
         xy=(t, np.sin(t)), xycoords='data',
         xytext=(+10, +30), textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plot([t,t],[0,np.sin(t)], color ='red', linewidth=2.5, linestyle="--")
scatter([t,],[np.sin(t),], 50, color ='red')

annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$',
         xy=(t, np.cos(t)), xycoords='data',
         xytext=(-90, -50), textcoords='offset points', fontsize=16,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# Save figure using 72 dots per inch
# savefig("exercice_2.png",dpi=72)

# Show result on screen
show()