import numpy as np
from scipy import fftpack
import wave
import scipy
from scipy.io.wavfile import write
from os.path import dirname, join as pjoin
import scipy.io as sio
import matplotlib.pyplot as plt
import sounddevice
import time
signal_duration=0.04 #seconds
fs=10000 #samplin freq
ffts=1024 #fft sampling frequency
num_samples=int(signal_duration*fs)
frq={'a':[400,1000,2000],'b':[400,1000,3000],'c':[400,1000,4000],'d':[400,1200,2000],'e':[400,1200,3000],'f':[400,1200,4000],'g':[400,1500,2000]
     ,'h':[400,1500,3000],'i':[400,1500,4000],'j':[600,1000,2000],'k':[600,1000,3000],'l':[600,1000,4000],'m':[600,1200,2000],'n':[600,1200,3000]
     ,'o':[600,1200,4000],'p':[600,1500,2000],'q':[600,1500,3000],'r':[600,1500,4000],'s':[800,1000,2000]
    ,'t':[800,1000,3000],'u':[800,1000,4000],'v':[800,1200,2000],'w':[800,1200,3000],'x':[800,1200,4000],'y':[800,1500,2000],'z':[800,1500,3000]
     ,' ':[800,1500,4000]}
stri="a good way to die hard"
l=[]
newstr=""
for i in stri:
    l=np.concatenate((l,[np.cos(frq[i][0]*2*np.pi*x/fs)+np.cos(frq[i][1]*2*np.pi*x/fs)+np.cos(frq[i][2]*2*np.pi*x/fs) for x in range(num_samples)]),axis=None)
x= np.arange(0,0.04*2,1/(320/0.04))


sounddevice.play(l, fs)  # releases GIL
time.sleep(1)

scipy.io.wavfile.write("lol.wav", 8000, l)

samplerate, l = sio.wavfile.read("hello.wav")


for i in  range(0,len(l),num_samples):
    freqMag=abs(fftpack.fft(l[i:i+num_samples],ffts))
    maxpoints=[(int(np.argmax(freqMag[int(350*(ffts/fs)):int(850*(ffts/fs))])+350*(ffts/fs))*(fs/ffts)),int((fs/ffts)*(np.argmax(freqMag[int(900*(ffts/fs)):int(1600*(ffts/fs))])+900*(ffts/fs))),int((fs/ffts)*(np.argmax(freqMag[int(1900*(ffts/fs)):int(4100*(ffts/fs))])+1900*(ffts/fs)))]
    for j in 0,1,2:
        maxpoints[j]=int(round(maxpoints[j]/100)*100)
    print(maxpoints)
    if maxpoints in frq.values():
        for x,y in frq.items():
            if  y == maxpoints:
                newstr=newstr+x


print(newstr)
#lmao=abs(fftpack.fft(l[0:num_samples],ffts))
#plt.plot(lmao)
#plt.show()
