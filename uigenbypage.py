from cmath import inf
import wave
import scipy
from tensorflow import keras
from models.afilm import AFiLM
from models.tfilm import TFiLM
from keras.utils.generic_utils import CustomObjectScope
import sys
import os
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog
import librosa
import librosa.display
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
from tkinter import messagebox
import pygame
pygame.mixer.init()
import soundfile as sf
#rom pypesq import pesq
from matplotlib.colors import LogNorm

from utils import get_spectrum, save_spectrum, upsample_wav


filename=''
f = Figure(figsize=(3, 2), dpi=80)
f_plot = f.add_subplot(111)
g = Figure(figsize=(3, 2),dpi=80)
g_plot= g.add_subplot(111)

pathc=''




class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40' # X11 color: #666666
        _ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
        _ana2color = 'beige' # X11 color: #f5f5dc
        _tabfg1 = 'black' 
        _tabfg2 = 'black' 
        _tabbg1 = 'grey75' 
        _tabbg2 = 'grey89' 
        _bgmode = 'light' 
        
        top.geometry("800x550+400+140")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0,  0)
        top.title("音频超分辨率重建")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        global f
        self.top = top
        self.rfact = tk.IntVar()
        self.rfact.set(2)

        self.open_btn = tk.Button(self.top)
        self.open_btn.place(x=520, y=66, height=30, width=150)
        self.open_btn.configure(activebackground="beige")
        self.open_btn.configure(activeforeground="#000000")
        self.open_btn.configure(background="#d9d9d9")
        self.open_btn.configure(compound='left')
        self.open_btn.configure(disabledforeground="#a3a3a3")
        self.open_btn.configure(foreground="#000000")
        self.open_btn.configure(highlightbackground="#d9d9d9")
        self.open_btn.configure(highlightcolor="black")
        self.open_btn.configure(pady="0")
        self.open_btn.configure(text='读取音频')
        self.open_btn.configure(command=self.choosefile)

        self.restore_btn = tk.Button(self.top)
        self.restore_btn.place(x=440, y=230, height=30, width=320)
        self.restore_btn.configure(activebackground="beige")
        self.restore_btn.configure(activeforeground="#000000")
        self.restore_btn.configure(background="#d9d9d9")
        self.restore_btn.configure(compound='left')
        self.restore_btn.configure(disabledforeground="#a3a3a3")
        self.restore_btn.configure(foreground="#000000")
        self.restore_btn.configure(highlightbackground="#d9d9d9")
        self.restore_btn.configure(highlightcolor="black")
        self.restore_btn.configure(pady="0")
        self.restore_btn.configure(text='重建音频')
        self.restore_btn.configure(command=self.restoreaudio)

        self.play_hr_btn = tk.Button(self.top)
        self.play_hr_btn.place(x=440, y=270, height=30, width=150)
        self.play_hr_btn.configure(activebackground="beige")
        self.play_hr_btn.configure(activeforeground="#000000")
        self.play_hr_btn.configure(background="#d9d9d9")
        self.play_hr_btn.configure(compound='left')
        self.play_hr_btn.configure(disabledforeground="#a3a3a3")
        self.play_hr_btn.configure(foreground="#000000")
        self.play_hr_btn.configure(highlightbackground="#d9d9d9")
        self.play_hr_btn.configure(highlightcolor="black")
        self.play_hr_btn.configure(pady="0")
        self.play_hr_btn.configure(text='播放原音频')
        self.play_hr_btn.configure(command=self.play_hr)

        self.play_lr_btn = tk.Button(self.top)
        self.play_lr_btn.place(x=440, y=310, height=30, width=150)
        self.play_lr_btn.configure(activebackground="beige")
        self.play_lr_btn.configure(activeforeground="#000000")
        self.play_lr_btn.configure(background="#d9d9d9")
        self.play_lr_btn.configure(compound='left')
        self.play_lr_btn.configure(disabledforeground="#a3a3a3")
        self.play_lr_btn.configure(foreground="#000000")
        self.play_lr_btn.configure(highlightbackground="#d9d9d9")
        self.play_lr_btn.configure(highlightcolor="black")
        self.play_lr_btn.configure(pady="0")
        self.play_lr_btn.configure(text='播放下采样音频')
        self.play_lr_btn.configure(command=self.play_lr)

        self.play_pr_btn = tk.Button(self.top)
        self.play_pr_btn.place(x=440, y=350, height=30, width=150)
        self.play_pr_btn.configure(activebackground="beige")
        self.play_pr_btn.configure(activeforeground="#000000")
        self.play_pr_btn.configure(background="#d9d9d9")
        self.play_pr_btn.configure(compound='left')
        self.play_pr_btn.configure(disabledforeground="#a3a3a3")
        self.play_pr_btn.configure(foreground="#000000")
        self.play_pr_btn.configure(highlightbackground="#d9d9d9")
        self.play_pr_btn.configure(highlightcolor="black")
        self.play_pr_btn.configure(pady="0")
        self.play_pr_btn.configure(text='播放机器学习音频')
        self.play_pr_btn.configure(command=self.play_pr)

        self.play_rr_btn = tk.Button(self.top)
        self.play_rr_btn.place(x=440, y=390, height=30, width=150)
        self.play_rr_btn.configure(activebackground="beige")
        self.play_rr_btn.configure(activeforeground="#000000")
        self.play_rr_btn.configure(background="#d9d9d9")
        self.play_rr_btn.configure(compound='left')
        self.play_rr_btn.configure(disabledforeground="#a3a3a3")
        self.play_rr_btn.configure(foreground="#000000")
        self.play_rr_btn.configure(highlightbackground="#d9d9d9")
        self.play_rr_btn.configure(highlightcolor="black")
        self.play_rr_btn.configure(pady="0")
        self.play_rr_btn.configure(text='播放重健音频')
        self.play_rr_btn.configure(command=self.play_rr)

        self.play_stop_btn = tk.Button(self.top)
        self.play_stop_btn.place(x=440, y=430, height=30, width=150)
        self.play_stop_btn.configure(activebackground="beige")
        self.play_stop_btn.configure(activeforeground="#000000")
        self.play_stop_btn.configure(background="#d9d9d9")
        self.play_stop_btn.configure(compound='left')
        self.play_stop_btn.configure(disabledforeground="#a3a3a3")
        self.play_stop_btn.configure(foreground="#000000")
        self.play_stop_btn.configure(highlightbackground="#d9d9d9")
        self.play_stop_btn.configure(highlightcolor="black")
        self.play_stop_btn.configure(pady="0")
        self.play_stop_btn.configure(text='停止播放')
        self.play_stop_btn.configure(command=self.play_stop)

        self.arguframe = tk.LabelFrame(self.top)
        self.arguframe.place(x=500, y=100, height=111, width=212)
        self.arguframe.configure(relief='groove')
        self.arguframe.configure(foreground="#000000")
        self.arguframe.configure(text='''参数选择''')
        self.arguframe.configure(background="#d9d9d9")
        self.arguframe.configure(highlightbackground="#d9d9d9")
        self.arguframe.configure(highlightcolor="black")

        self.rFact2button = tk.Radiobutton(self.arguframe)
        self.rFact2button.place(x=30, y=30, height=26, width=123
                 , bordermode='ignore')
        self.rFact2button.configure(activebackground="beige")
        self.rFact2button.configure(activeforeground="#000000")
        self.rFact2button.configure(anchor='w')
        self.rFact2button.configure(background="#d9d9d9")
        self.rFact2button.configure(compound='left')
        self.rFact2button.configure(disabledforeground="#a3a3a3")
        self.rFact2button.configure(foreground="#000000")
        self.rFact2button.configure(highlightbackground="#d9d9d9")
        self.rFact2button.configure(highlightcolor="black")
        self.rFact2button.configure(justify='left')
        self.rFact2button.configure(selectcolor="#d9d9d9")
        self.rFact2button.configure(text='''下采样系数r=2''')
        self.rFact2button.configure(value='2')
        self.rFact2button.configure(variable=self.rfact)

        self.rFact4button = tk.Radiobutton(self.arguframe)
        self.rFact4button.place(x=30, y=70, height=26, width=123
                 , bordermode='ignore')
        self.rFact4button.configure(activebackground="beige")
        self.rFact4button.configure(activeforeground="#000000")
        self.rFact4button.configure(anchor='w')
        self.rFact4button.configure(background="#d9d9d9")
        self.rFact4button.configure(compound='left')
        self.rFact4button.configure(disabledforeground="#a3a3a3")
        self.rFact4button.configure(foreground="#000000")
        self.rFact4button.configure(highlightbackground="#d9d9d9")
        self.rFact4button.configure(highlightcolor="black")
        self.rFact4button.configure(justify='left')
        self.rFact4button.configure(selectcolor="#d9d9d9")
        self.rFact4button.configure(text='''下采样系数r=4''')
        self.rFact4button.configure(value='4')
        self.rFact4button.configure(variable=self.rfact)

        self.hr_plot_btn = tk.Button(self.top)
        self.hr_plot_btn.place(x=610, y=270, height=30, width=150)
        self.hr_plot_btn.configure(activebackground="beige")
        self.hr_plot_btn.configure(activeforeground="#000000")
        self.hr_plot_btn.configure(background="#d9d9d9")
        self.hr_plot_btn.configure(compound='left')
        self.hr_plot_btn.configure(disabledforeground="#a3a3a3")
        self.hr_plot_btn.configure(foreground="#000000")
        self.hr_plot_btn.configure(highlightbackground="#d9d9d9")
        self.hr_plot_btn.configure(highlightcolor="black")
        self.hr_plot_btn.configure(pady="0")
        self.hr_plot_btn.configure(text='显示原音频图')
        self.hr_plot_btn.configure(command=self.plot_hr)

        self.lr_plot_btn = tk.Button(self.top)
        self.lr_plot_btn.place(x=610, y=310, height=30, width=150)
        self.lr_plot_btn.configure(activebackground="beige")
        self.lr_plot_btn.configure(activeforeground="#000000")
        self.lr_plot_btn.configure(background="#d9d9d9")
        self.lr_plot_btn.configure(compound='left')
        self.lr_plot_btn.configure(disabledforeground="#a3a3a3")
        self.lr_plot_btn.configure(foreground="#000000")
        self.lr_plot_btn.configure(highlightbackground="#d9d9d9")
        self.lr_plot_btn.configure(highlightcolor="black")
        self.lr_plot_btn.configure(pady="0")
        self.lr_plot_btn.configure(text='显示下采样音频图')
        self.lr_plot_btn.configure(command=self.plot_lr)

        self.pr_plot_btn = tk.Button(self.top)
        self.pr_plot_btn.place(x=610, y=350, height=30, width=150)
        self.pr_plot_btn.configure(activebackground="beige")
        self.pr_plot_btn.configure(activeforeground="#000000")
        self.pr_plot_btn.configure(background="#d9d9d9")
        self.pr_plot_btn.configure(compound='left')
        self.pr_plot_btn.configure(disabledforeground="#a3a3a3")
        self.pr_plot_btn.configure(foreground="#000000")
        self.pr_plot_btn.configure(highlightbackground="#d9d9d9")
        self.pr_plot_btn.configure(highlightcolor="black")
        self.pr_plot_btn.configure(pady="0")
        self.pr_plot_btn.configure(text='显示机器学习音频图')
        self.pr_plot_btn.configure(command=self.plot_pr)

        self.rr_plot_btn = tk.Button(self.top)
        self.rr_plot_btn.place(x=610, y=390, height=30, width=150)
        self.rr_plot_btn.configure(activebackground="beige")
        self.rr_plot_btn.configure(activeforeground="#000000")
        self.rr_plot_btn.configure(background="#d9d9d9")
        self.rr_plot_btn.configure(compound='left')
        self.rr_plot_btn.configure(disabledforeground="#a3a3a3")
        self.rr_plot_btn.configure(foreground="#000000")
        self.rr_plot_btn.configure(highlightbackground="#d9d9d9")
        self.rr_plot_btn.configure(highlightcolor="black")
        self.rr_plot_btn.configure(pady="0")
        self.rr_plot_btn.configure(text='显示重建音频图')
        self.rr_plot_btn.configure(command=self.plot_rr)

        self.clr_plot_btn = tk.Button(self.top)
        self.clr_plot_btn.place(x=610, y=430, height=30, width=150)
        self.clr_plot_btn.configure(activebackground="beige")
        self.clr_plot_btn.configure(activeforeground="#000000")
        self.clr_plot_btn.configure(background="#d9d9d9")
        self.clr_plot_btn.configure(compound='left')
        self.clr_plot_btn.configure(disabledforeground="#a3a3a3")
        self.clr_plot_btn.configure(foreground="#000000")
        self.clr_plot_btn.configure(highlightbackground="#d9d9d9")
        self.clr_plot_btn.configure(highlightcolor="black")
        self.clr_plot_btn.configure(pady="0")
        self.clr_plot_btn.configure(text='清理画布')
        self.clr_plot_btn.configure(command=self.plot_clear)

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(x=10, y=12, height=483, width=385)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
 
        self.Canvas2 = FigureCanvasTkAgg(f, self.Frame1)
        self.Canvas2.get_tk_widget().place(x=0, y=225, height=252, width=382)
        self.Canvas2.get_tk_widget().configure(background="#d9d9d9")
        self.Canvas2.get_tk_widget().configure(borderwidth="2")
        self.Canvas2.get_tk_widget().configure(highlightbackground="#d9d9d9")
        self.Canvas2.get_tk_widget().configure(highlightcolor="black")
        self.Canvas2.get_tk_widget().configure(insertbackground="black")
        self.Canvas2.get_tk_widget().configure(relief="ridge")
        self.Canvas2.get_tk_widget().configure(selectbackground="#c4c4c4")
        self.Canvas2.get_tk_widget().configure(selectforeground="black")

 
        self.Canvas1 = FigureCanvasTkAgg(g, self.Frame1)
        self.Canvas1.get_tk_widget().place(x=0, y=0, height=224, width=382)
        self.Canvas1.get_tk_widget().configure(background="#d9d9d9")
        self.Canvas1.get_tk_widget().configure(borderwidth="2")
        self.Canvas1.get_tk_widget().configure(insertbackground="black")
        self.Canvas1.get_tk_widget().configure(relief="ridge")
        self.Canvas1.get_tk_widget().configure(selectbackground="#c4c4c4")
        self.Canvas1.get_tk_widget().configure(selectforeground="black")
        
        self.filelabel = tk.Label(self.top)
        self.filelabel.place(x=440, y=10, height=23, width=360)
        self.filelabel.configure(activebackground="#f9f9f9")
        self.filelabel.configure(anchor='w')
        self.filelabel.configure(background="#d9d9d9")
        self.filelabel.configure(compound='left')
        self.filelabel.configure(disabledforeground="#a3a3a3")
        self.filelabel.configure(foreground="#000000")
        self.filelabel.configure(highlightbackground="#d9d9d9")
        self.filelabel.configure(highlightcolor="black")
        self.filelabel.configure(text='')

        self.testlabel = tk.Label(self.top)
        self.testlabel.place(x=440, y=480, height=23, width=360)
        self.testlabel.configure(anchor='w')
        self.testlabel.configure(background="#d9d9d9")
        self.testlabel.configure(compound='left')
        self.testlabel.configure(disabledforeground="#a3a3a3")
        self.testlabel.configure(foreground="#000000")
        self.testlabel.configure(text='''小组''')

        self.versionlabel = tk.Label(self.top)
        self.versionlabel.place(x=440, y=40, height=23, width=100)
        self.versionlabel.configure(activebackground="#f9f9f9")
        self.versionlabel.configure(anchor='w')
        self.versionlabel.configure(background="#d9d9d9")
        self.versionlabel.configure(compound='left')
        self.versionlabel.configure(disabledforeground="#a3a3a3")
        self.versionlabel.configure(foreground="#000000")
        self.versionlabel.configure(highlightbackground="#d9d9d9")
        self.versionlabel.configure(highlightcolor="black")
        self.versionlabel.configure(text='''''')

        self.SNR = tk.Label(self.top)
        self.SNR.place(x=550, y=40, height=23, width=100)
        self.SNR.configure(activebackground="#f9f9f9")
        self.SNR.configure(anchor='w')
        self.SNR.configure(background="#d9d9d9")
        self.SNR.configure(compound='left')
        self.SNR.configure(disabledforeground="#a3a3a3")
        self.SNR.configure(foreground="#000000")
        self.SNR.configure(highlightbackground="#d9d9d9")
        self.SNR.configure(highlightcolor="black")
        self.SNR.configure(text='''SNR''')

        self.LSD = tk.Label(self.top)
        self.LSD.place(x=660, y=40, height=23, width=100)
        self.LSD.configure(activebackground="#f9f9f9")
        self.LSD.configure(anchor='w')
        self.LSD.configure(background="#d9d9d9")
        self.LSD.configure(compound='left')
        self.LSD.configure(disabledforeground="#a3a3a3")
        self.LSD.configure(foreground="#000000")
        self.LSD.configure(highlightbackground="#d9d9d9")
        self.LSD.configure(highlightcolor="black")
        self.LSD.configure(text='''LSD''')

    def choosefile(self):
        global filename
        filename =filedialog.askopenfilename(filetypes=[("wav",".wav")])
        self.filelabel['text'] = filename

    def restoreaudio(self):
        if not messagebox.askokcancel("提示",'耗时可能较长，是否开始重建', default="cancel", icon="warning"):
            return 
        global filename
        pathm=self.get_model_path('model.h5') #model训练方法见KYShek/AFILM
        self.message("load model path success")
        model=self.loadmodel(pathm)
        self.message("load model success")
        #model=self.loadmodel(self.get_model_path('model.h5'))
        #upsample_wav(args.wav_file_list, args, model
        upsample_wav(filename,model,self.rfact.get())
        #self.testlabel['text'] = 'upsample done'
        messagebox.showinfo("重建完成", "重建已完成")

    def loadmodel(self,pathM):
        with CustomObjectScope({"AFiLM":AFiLM, "TFiLM":TFiLM}):
           return keras.models.load_model(pathM)

    def message(self,message):
        top2 = tk.Toplevel()
        top2.geometry("150x50")
        self.center(top2)
        top2.title('模型生成中')
        tk.Message(top2, text=message, padx=20, pady=20).pack()
        top2.after(1000, top2.destroy)

    def center(self,win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def join_path(self, res:'str'):
        global filename
        #path=os.path.dirname(__file__)
        #如被封装为exe
        #path=os.path.dirname(os.path.abspath(__file__))
        pathw=filename+"."+res+".wav"
        return pathw

    def play_hr(self):
        global filename
        pygame.mixer.stop()
        path_play=self.join_path("hr")
        self.play(path_play)

    def play_lr(self):
        global filename
        pygame.mixer.stop()
        path_play=self.join_path("lr")
        self.play(path_play)

    def play_pr(self):
        global filename
        pygame.mixer.stop()
        path_play=self.join_path("pr")
        self.play(path_play)

    def play_rr(self):
        global filename
        pygame.mixer.stop()
        path_play=self.join_path("rr")
        self.play(path_play)

    def play_stop(self):
        pygame.mixer.stop()

    def play(self,path):
        music=pygame.mixer.Sound(path)
        music.set_volume(0.4)
        music.play()

    def plot_hr(self):
        path_draw=self.join_path("hr")
        self.draw_waveform(path_draw) 
        self.draw_spectrum(path_draw)
        self.clear_label()

    def plot_lr(self):
        path_draw=self.join_path("lr")
        self.draw_waveform(path_draw)
        self.draw_spectrum(path_draw)
        self.show_SNR_lr()
        self.versionlabel['text']='''lr'''
        self.LSD['text']=''''''

    def plot_pr(self):
        path_draw=self.join_path("pr")
        self.draw_waveform(path_draw)
        self.draw_spectrum(path_draw)
        self.show_SNR_pr()
        self.versionlabel['text']='''pr'''
        self.show_LSD_pr()       

    def plot_rr(self):
        path_draw=self.join_path("rr")
        self.draw_waveform(path_draw)
        self.draw_spectrum(path_draw)
        self.show_SNR_rr()
        self.versionlabel['text']='''rr'''
        self.show_LSD_rr()  

    def plot_clear(self):
        g_plot.clear()
        self.Canvas1.draw()
        f_plot.clear()
        self.Canvas2.draw()
        self.clear_label()

    def draw_waveform(self,path):
        global g_plot
        g_plot.clear()
        f = wave.open(path,"rb")
        #plt.figure(1)
        signal = f.readframes(-1)
        signal = np.fromstring(signal, dtype=np.int16)
        fs = f.getframerate()
        t = np.linspace(0, len(signal) / fs, num=len(signal))
        g_plot.plot(t,signal)
        self.Canvas1.draw()

    def draw_spectrum(self,path):
        f_plot.clear()
        x, sr = librosa.load(path, sr=None)
        print(len(x))
        ft =scipy.fft.fft(x)
        magnitude = np.absolute(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
        frequency = np.linspace(0, sr, len(magnitude))  # (0, 16000, 121632)
        f_plot.plot(frequency[:40000], magnitude[:40000])  # magnitude spectrum   
        self.Canvas2.draw() 

    def clear_picture(self):
        global f_plot
        f_plot.clear()
        self.Canvas1.draw()

    def get_model_path(self,modelfile):
        path=os.path.dirname(__file__)
        #如被封装为exe
        #path=os.path.dirname(os.path.abspath(__file__))
        path=os.path.join(path,modelfile)
        pathc = "/".join(path.split("\\"))
        return pathc
    
    def clear_label(self):
        self.versionlabel['text']=''''''
        self.SNR['text']=''''''
        self.LSD['text']=''''''

    def SNR_singlech(self,clean_file, original_file):
        clean, clean_fs = librosa.load(clean_file, sr=None, mono=True)#导入干净语音
        ori, ori_fs = librosa.load(original_file, sr=None, mono=True)#导入原始语音
        length = min(len(clean), len(ori))
        est_noise = ori[:length] - clean[:length]#计算噪声语音
        SNR = 10*np.log10((np.sum(clean**2))/(np.sum(est_noise**2)))
        return SNR
    
    def show_SNR_lr(self):
        global filename
        path_hr=self.join_path("hr")
        path_lr=self.join_path("lr")
        SNR=self.SNR_singlech(path_hr,path_lr)
        self.SNR['text'] = SNR
    
    def show_SNR_rr(self):
        global filename
        path_hr=self.join_path("hr")
        path_rr=self.join_path("rr")
        SNR=self.SNR_singlech(path_hr,path_rr)
        self.SNR['text'] = SNR
        
    def show_SNR_pr(self):
        global filename
        path_hr=self.join_path("hr")
        path_pr=self.join_path("pr")
        SNR=self.SNR_singlech(path_hr,path_pr)
        self.SNR['text'] = SNR
    
    def show_LSD_rr(self):
        path_hr=self.join_path("hr")
        path_rr=self.join_path("rr")
        self.plot_all(path_rr)

    def show_LSD_pr(self):
        path_hr=self.join_path("hr")
        path_pr=self.join_path("pr")
        self.plot_all(path_pr)

    def read_audio_spectrum(self,x, **kwd_args):
        return librosa.core.stft(x, **kwd_args)

    def plot_all(self,path_r):
        n_fft = 2048
        global filename
        path_original=self.join_path("hr")
        path_lr=self.join_path("lr")

        y_true, true_sr = librosa.load(path_original, sr=None)
        y_ds, ds_sr = librosa.load(path_lr, sr=None)
        y_ds = librosa.core.resample(y_ds, orig_sr=ds_sr, target_sr=true_sr)
        y_reco, reco_sr = librosa.load(path_r, sr=None)

        if(len(y_ds)<len(y_true)):
            y_ds = np.pad(y_ds,(0,len(y_true)-len(y_ds)),'edge')
        print(len(y_ds))
        print(len(y_true))
        print(len(y_reco))
        true_spectrogram = self.read_audio_spectrum(y_true, n_fft=n_fft)
        ds_spectrogram = self.read_audio_spectrum(y_ds, n_fft=n_fft)
        reco_spectrogram = self.read_audio_spectrum(y_reco, n_fft=n_fft)

        if not (true_sr == ds_sr == reco_sr):
            print('Warning: time axis on waveform plots will be meaningless')

        # compute LSD
        true_X = np.log10(np.abs(true_spectrogram)**2)
        ds_X = np.log10(np.abs(ds_spectrogram)**2)
        reco_X = np.log10(np.abs(reco_spectrogram)**2)
        true_X =self.replaceZeroes(true_X)
        ds_X =self.replaceZeroes(ds_X)
        print(ds_X)
        reco_X =self.replaceZeroes(reco_X)
        ds_X_diff_squared = (true_X - ds_X)**2
        reco_X_diff_squared = (true_X - reco_X)**2
        #ds_lsd = np.mean(np.sqrt(np.mean(ds_X_diff_squared, axis=0)))
        reco_lsd = np.mean(np.sqrt(np.mean(reco_X_diff_squared, axis=0)))
        self.LSD['text'] = reco_lsd

        # compute SNR for waveform plots
        #ds_snr = self.compute_signal_to_noise(y_true, y_ds)
        #reco_snr = self.compute_signal_to_noise(y_true, y_reco)
    
    def replaceZeroes(self,data):
        zero = 0.000000000001
        min_ninf = np.min(data[data != -inf])
        max_inf = np.max(data[data!=inf])
        data[data == 0] = zero
        data[data == inf]= max_inf
        data[data == -inf] = min_ninf
        return data

    def compute_signal_to_noise(self, truth, reco):
        return 10.*np.log10(np.sqrt(np.sum(truth**2))/np.sqrt(
            np.sum((truth - reco)**2)))

def main(*args):
    '''Main entry point for the application.'''
    global root
    if keras.__version__ != "2.6.0":
        messagebox.showinfo("keras版本", "keras版本错误")
        exit(1)
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    main()



