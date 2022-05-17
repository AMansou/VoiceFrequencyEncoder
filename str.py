from tkinter import *
from tkinter import filedialog as fd
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
from scipy import signal

##############UTILITY METHODS AND DEFINITIONS #####################
num_zeros=200
signal_duration=0.04 #seconds
fs=44000 #samplin freq
ffts=1024 #fft sampling frequency
num_samples=int(signal_duration*fs)
frq={'a':[400,1000,2000],'b':[400,1000,3000],'c':[400,1000,4000],'d':[400,1200,2000],'e':[400,1200,3000],'f':[400,1200,4000],'g':[400,1500,2000]
     ,'h':[400,1500,3000],'i':[400,1500,4000],'j':[600,1000,2000],'k':[600,1000,3000],'l':[600,1000,4000],'m':[600,1200,2000],'n':[600,1200,3000]
     ,'o':[600,1200,4000],'p':[600,1500,2000],'q':[600,1500,3000],'r':[600,1500,4000],'s':[800,1000,2000]
    ,'t':[800,1000,3000],'u':[800,1000,4000],'v':[800,1200,2000],'w':[800,1200,3000],'x':[800,1200,4000],'y':[800,1500,2000],'z':[800,1500,3000]
     ,' ':[800,1500,4000]}
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
#################################################
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu)
        self.l=[]
        self.newstr=StringVar()
        self.path=''
        fileMenu = Menu(menu)
        fileMenu.add_command(label="Save as",command=self.saveAs)
        fileMenu.add_command(label="Save",command=self.save)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)


        self.E1 = Entry(bd=5)
        self.E1.pack(side=TOP)
        L1=Label(textvariable=self.newstr,relief=RAISED)
        L1.pack(side=BOTTOM)
        B4=Button(text="Encode String",command=self.encode)
        B4.pack()
        B1=Button(text="Plot Encoded String",command=self.plotString)
        B1.pack()
        B2=Button(text="Listen",command=self.listen)
        B2.pack()
        B3=Button(text="Get encoded signal from a file Instead",command=self.fileInput)
        B3.pack()
        B5=Button(text="DECODE:" , command=self.decode)
        B5.pack()
        B6=Button(text="DECODE (Filters):" , command=self.decode1)
        B6.pack()
        var = StringVar()



    def exitProgram(self):
        exit()
    def saveAs(self):
        dum=self.path
        self.path=fd.asksaveasfilename()
        if self.path=='':
            self.path=dum
        if self.path!='':
            scipy.io.wavfile.write(self.path, 8000, self.l)
    def save(self):
        if self.path == '':
            self.saveAs()
        else:
            scipy.io.wavfile.write(self.path,8000,self.l)


    def fileInput(self):
        name= fd.askopenfilename()
        if name != '':
            samplerate, self.l = sio.wavfile.read(name)
    def encode(self):
        self.l=[]
        stri=self.E1.get() # get the string from the input box
        for i in stri:
            #for each letter in the string, use that letter to find the set of frequencies needed for it in the freq dictionary
            #then, concatinate it to the signal generated by the characters before.
            self.l=np.concatenate((self.l,np.zeros(num_zeros)))
            self.l=np.concatenate((self.l,[np.cos(frq[i][0]*2*np.pi*x/fs)+np.cos(frq[i][1]*2*np.pi*x/fs)+np.cos(frq[i][2]*2*np.pi*x/fs) for x in range(num_samples)]),axis=None)
    def plotString(self):
        fig = plt.figure()
        fig.subplots_adjust(top=0.8)
        ax1 = fig.add_subplot(211)
        ax1.set_ylabel('x(t)')
        ax1.set_xlabel('t')
        ax1.set_title('Time Domain Wave')
        ax1.plot(self.l)
        ax2 = fig.add_axes([0.15, 0.1, 0.7, 0.2])
        ax2.set_ylabel('X(f)')
        ax2.set_xlabel('f')
        ax2.set_title('Frequency Domain Wave')
        ax2.plot(abs(fftpack.fft(self.l)))

        plt.show()
    def listen(self):
        sounddevice.play(self.l, fs)  # releases GIL
        time.sleep(1)
    def decode(self):
        newstr="" #initialize empty string
        zeros=np.argwhere(self.l == 0).ravel()
        countz=0
        conseczeros=[]
        for i in range(len(zeros)-1): #algorithm to see the length of consecutive zeros
            if zeros[i]+1== (zeros [i+1]):
                countz=countz+1
            elif countz!=0:
                conseczeros.append(countz+1)
                countz=0
        for i in  range(0,len(self.l),num_samples+max(conseczeros)): #for each letter
            freqMag=abs(fftpack.fft(self.l[i:i+num_samples],ffts))  #find the magnitude of the signal in the frequency domain
            #now to find the max points of frq max in the [low/medium/high] frequency ranges
            maxpoints=[(int(np.argmax(freqMag[int(350*(ffts/fs)):int(850*(ffts/fs))])+350*(ffts/fs))*(fs/ffts)),int((fs/ffts)*(np.argmax(freqMag[int(900*(ffts/fs)):int(1600*(ffts/fs))])+900*(ffts/fs))),int((fs/ffts)*(np.argmax(freqMag[int(1900*(ffts/fs)):int(4100*(ffts/fs))])+1900*(ffts/fs)))]
            #argmax find the index of the max value
            for j in 0,1,2:
                maxpoints[j]=int(round(maxpoints[j]/100)*100) # round them up to the values of letters above (even if the value is 520, it should be rounded to 500 and so on)
            if maxpoints in frq.values(): # if the three frequencies found exist in the  freq dictionary defined above
                for x,y in frq.items():
                    if  y == maxpoints:
                        newstr=newstr+x # when you find that the array is equal to the one we found, add the array's key to the string
                        self.newstr.set(newstr)
    def decode1(self):
        newstr="Filters: "
        letterfrq=[0,0,0]
        self.l=np.trim_zeros(self.l)
        zeros=np.argwhere(self.l == 0).ravel()
        countz=0
        conseczeros=[]
        for i in range(len(zeros)-1): #algorithm to see the length of consecutive zeros
            if zeros[i]+1== (zeros [i+1]):
                countz=countz+1
            elif countz!=0:
                conseczeros.append(countz+1)
                countz=0


        for i in  range(0,len(self.l),num_samples+max(conseczeros)): # for each encoded letter + pause
            # use three bandpass filters for low high and medium frequencies of the signal
            #after using each filter find the frequency index of the maximum point and added to the etterfrq list
            x=butter_bandpass_filter(self.l[i:i+num_samples], 300, 850, fs, order=1)
            letterfrq[0]= np.argmax(abs(fftpack.fft(x,ffts)))*(fs/ffts)
            x=butter_bandpass_filter(self.l[i:i+num_samples], 950, 1550, fs, order=1)
            letterfrq[1]= np.argmax(abs(fftpack.fft(x,ffts)))*(fs/ffts)
            x=butter_bandpass_filter(self.l[i:i+num_samples], 1950, 4050, fs, order=1)
            letterfrq[2]= np.argmax(abs(fftpack.fft(x,ffts)))*(fs/ffts)
            #Now round the results
            for j in 0,1,2:
                letterfrq[j]=int(round(letterfrq[j]/100)*100)
            # And finally, find the keys to a list that equals letterfreq in the dictionary and add it to the string
            if letterfrq in frq.values():
                for x,y in frq.items():
                    if  y == letterfrq:
                        newstr=newstr+x
                        self.newstr.set(newstr)



root = Tk()
app = Window(root)
root.wm_title("DENCODER V3.0")
root.geometry("300x200")
root.mainloop()
