'''
Author: ChiaEnKang
Date: 2021-09-02 17:05:04
LastEditors: ChiaEnKang
LastEditTime: 2021-09-23 16:50:02
'''
import configparser
import cv2
import sys
from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk, messagebox

class CreateTk():

    def __init__(self, left_y=0, right_y=0):
        self.left_y = left_y
        self.right_y = right_y
        self.ppbox_cfg = Tk()
        self.while_loop = True

    def create_tk_v(self, img_heigth):
        self.ppbox_cfg.title('Control Frame')
        ppbox_line_left = Scale(self.ppbox_cfg, label='ppbox警戒線左邊底部(左y)', length=300, from_=0, to=img_heigth-1, orient=HORIZONTAL)
        ppbox_line_right = Scale(self.ppbox_cfg, label='ppbox警戒線右邊底部(右y)', length=300, from_=0, to=img_heigth-1, orient=HORIZONTAL)
        ppbox_line_left.set(self.left_y)   
        ppbox_line_right.set(self.right_y)  
        ppbox_line_left.pack()
        ppbox_line_right.pack()

        return ppbox_line_left, ppbox_line_right

    def create_tk_img(self, img_heigth):
        self.ppbox_cfg.title('Image Color Parameters Setting')
        red_line = Label(self.ppbox_cfg, text='Red Line', font=('Arial', 16, BOLD))
        self.ppbox_line_left = Scale(self.ppbox_cfg, label='ppbox警戒線左邊底部(左y)', length=300, from_=0, to=img_heigth-1, orient=HORIZONTAL)
        self.ppbox_line_right = Scale(self.ppbox_cfg, label='ppbox警戒線右邊底部(右y)', length=300, from_=0, to=img_heigth-1, orient=HORIZONTAL)
        hsv_mask = Label(self.ppbox_cfg, text='HSV mask', font=('Arial', 16, BOLD))
        self.l_h = Scale(self.ppbox_cfg, label='lower h', length=300, from_=0, to=180, orient=HORIZONTAL)
        self.l_s = Scale(self.ppbox_cfg, label='lower s', length=300, from_=0, to=255, orient=HORIZONTAL)
        self.l_v = Scale(self.ppbox_cfg, label='lower v', length=300, from_=0, to=255, orient=HORIZONTAL)
        self.u_h =  Scale(self.ppbox_cfg, label='upper h', length=300, from_=0, to=180, orient=HORIZONTAL)
        self.u_s = Scale(self.ppbox_cfg, label='upper s', length=300, from_=0, to=255, orient=HORIZONTAL)
        self.u_v = Scale(self.ppbox_cfg, label='upper v', length=300, from_=0, to=255, orient=HORIZONTAL)
        white_b = Label(self.ppbox_cfg, text='White Balance', font=('Arial', 16, BOLD))
        self.b = Scale(self.ppbox_cfg, label='Blue', length=300, from_=0, to=255, orient=HORIZONTAL)
        self.g = Scale(self.ppbox_cfg, label='Green', length=300, from_=0, to=255, orient=HORIZONTAL)
        self.r = Scale(self.ppbox_cfg, label='Red', length=300, from_=0, to=255, orient=HORIZONTAL)
        chk_btn = Button(self.ppbox_cfg, bg='orange', text='確認並產生設定檔', command=self.generate_ini)
        separator1 = ttk.Separator(self.ppbox_cfg, orient='horizontal')
        separator2 = ttk.Separator(self.ppbox_cfg, orient='horizontal')
        separator3 = ttk.Separator(self.ppbox_cfg, orient='horizontal')
        chk_btn.config(height='3')
        detect_t_txt = StringVar(value='10')
        detect_t_lbl = Label(self.ppbox_cfg, text="Detect Time(s):", font=('Arial', 16, BOLD))
        self.detect_t = Entry(self.ppbox_cfg, textvariable=detect_t_txt)
        self.u_h.set(180)
        self.u_s.set(255)
        self.u_v.set(255)
        red_line.pack(pady=5)
        self.ppbox_line_left.pack()
        self.ppbox_line_right.pack()
        separator1.pack(fill='x', pady=10)
        hsv_mask.pack()
        self.l_h.pack()
        self.l_s.pack()
        self.l_v.pack()
        self.u_h.pack()
        self.u_s.pack()
        self.u_v.pack()
        separator2.pack(fill='x', pady=10)
        white_b.pack()
        self.b.pack()
        self.g.pack()
        self.r.pack()
        separator3.pack(fill='x', pady=10)
        detect_t_lbl.pack()
        self.detect_t.pack(pady=10)
        chk_btn.pack(pady=10)

    def generate_ini(self, configfile_name=r'./video_config.ini'):
        # Check if there is already a configurtion file
        # Create the configuration file as it doesn't exist yet
        msg_result = messagebox.askokcancel("Notification", "確定要產生設定檔嗎?")
        if msg_result == True:
            cfgfile = open(configfile_name, 'w')
            # Add content to the file
            cfg = configparser.ConfigParser()
            sectione_name = ['Line', 'Color', 'DETECT_TIME']
            for i in sectione_name:
                cfg.add_section(i)
                if i == 'Line':
                    cfg.set(i, 'left_y', str(self.ppbox_line_left.get()))
                    cfg.set(i, 'right_y', str(self.ppbox_line_right.get()))
                elif i == 'Color':
                    l_pink_str = 'np.array([{}, {}, {}])'.format(self.l_h.get(), self.l_s.get(), self.l_v.get())
                    u_pink_str = 'np.array([{}, {}, {}])'.format(self.u_h.get(), self.u_s.get(), self.u_v.get())
                    cfg.set(i, 'l_pink', l_pink_str)
                    cfg.set(i, 'u_pink', u_pink_str)
                    cfg.set(i, 'b_plus', str(self.b.get()))
                    cfg.set(i, 'g_plus', str(self.g.get()))
                    cfg.set(i, 'r_plus', str(self.r.get()))
                else:
                    cfg.set(i, 't_setting', str(self.detect_t.get()))
            cfg.write(cfgfile)
            cfgfile.close()
            self.ppbox_cfg.destroy()
            cv2.destroyAllWindows()

