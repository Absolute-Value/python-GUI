#! /usr/bin/env python3
# main.py

import tkinter as tk
from tkinter import ttk
import players

class Baseball:
    def __init__(self, players):
        self.PLAYERS = players
        AWAY_TEAM_NUM, HOME_TEAM_NUM = 9, 9
        self.turn = 0
        self.inning = 1
        self.count = [0] * 3

        root = tk.Tk()
        root.title('野球')
        root.configure(bg="#55f")

        self.left_frame = ttk.Frame(root)
        self.left_frame.grid(row=0, column=0)
        self.center_frame = ttk.Frame(root)
        self.center_frame.grid(row=0, column=1, sticky=tk.N)
        self.right_frame = ttk.Frame(root)
        self.right_frame.grid(row=0, column=2)
        self.score_frame = ttk.Frame(self.center_frame)
        self.score_frame.grid(row=0, column=0)

        # left frame
        self.team = [0] * 2
        for i in range(len(self.team)):
            self.team[i] = tk.StringVar()
            self.team[i].set('中日')
        away_team_show = ttk.Label(self.left_frame, textvariable=self.team[0], width=7, font=("HG行書体", 20))
        away_team_show.grid(row=0,column=1,columnspan=3)
        self.away_team_player = [0] * AWAY_TEAM_NUM
        self.away_team_pos = [0] * AWAY_TEAM_NUM
        self.players(self.away_team_player, self.away_team_pos, self.left_frame, self.team[0])

        # right frame
        home_team_show = ttk.Label(self.right_frame, textvariable=self.team[1], width=7, font=("HG行書体", 20))
        home_team_show.grid(row=0,column=1,columnspan=3)
        self.home_team_player = [0] * HOME_TEAM_NUM
        self.home_team_pos = [0] * HOME_TEAM_NUM
        self.players(self.home_team_player, self.home_team_pos, self.right_frame, self.team[1])

        label2 = ('計', '安', '失')
        for i in range(len(label2)):
            label2_show = ttk.Label(self.score_frame, text=label2[i], justify='center')
            label2_show.grid(row=0, column=10+i)

        # チーム名
        teams = [0] * 2
        for i in range(2):
            teams[i] = ttk.Combobox(self.score_frame, textvariable=self.team[i], state='readonly', width=6)
            teams[i]['values'] = ('巨人', 'ヤクルト', 'DeNA', '中日', '阪神', '広島', '日本ハム', '楽天', '西武', 'ロッテ', 'オリックス', 'ソフトバンク')
            teams[i].grid(row=i+1, column=0) 
        teams[0].bind("<<ComboboxSelected>>", self.enter_away_team)
        teams[1].bind("<<ComboboxSelected>>", self.enter_home_team)

        self.team_score = [[0 for _ in range(12)] for _ in range(2)]
        for i in range(len(self.team_score)):
            for j in range(len(self.team_score[0])):
                self.team_score[i][j] = tk.StringVar()
        self.score_draw()

        self.team_score[0][0].set('-')

        self.score_sum = [0] * 2
        self.hit = [0] * 2
        error = [0] * 2
        for i in range(2):
            self.score_sum[i] = tk.IntVar()
            score_sum_show = ttk.Label(self.score_frame, textvariable=self.score_sum[i], width=2)
            score_sum_show.grid(row=i+1, column=10)
            self.hit[i] = tk.IntVar()
            hit_show = ttk.Label(self.score_frame, textvariable=self.hit[i], justify='center', width=2)
            hit_show.grid(row=i+1, column=11)
            error[i] = tk.IntVar()
            error_show = ttk.Label(self.score_frame, textvariable=error[i], justify='center', width=2)
            error_show.grid(row=i+1, column=12)

        self.bso_canvas = tk.Canvas(self.center_frame, width=56, height=48)
        self.bso_canvas.grid(row=1, column=0, sticky=tk.W)
        self.bso_draw()

        # calc frame
        calc_frame = ttk.Frame(root)
        calc_frame.grid(row=1,column=0,columnspan=3)

        ball_btn = ttk.Button(calc_frame, text='B', command=lambda:self.count_add(0), width=1)
        ball_btn.pack(side=tk.LEFT)
        strike_btn = ttk.Button(calc_frame, text='S', command=lambda:self.count_add(1), width=1)
        strike_btn.pack(side=tk.LEFT)
        out_btn = ttk.Button(calc_frame, text='O', command=lambda:self.count_add(2), width=1)
        out_btn.pack(side=tk.LEFT)
        hit_btn = ttk.Button(calc_frame, text='H', command=lambda:self.count_add(3), width=1)
        hit_btn.pack(side=tk.LEFT)
        error_btn = ttk.Button(calc_frame, text='E', command=lambda:add(error[self.turn-1]), width=1)
        error_btn.pack(side=tk.LEFT)
        for i in range(4):
            score_btn = ttk.Button(calc_frame, text=i+1, width=1)
            score_btn.bind("<1>", self.get_score)
            score_btn.pack(side=tk.LEFT)
        
        root.mainloop()

    def enter_away_team(self, event):
        self.players(self.away_team_player, self.away_team_pos, self.left_frame, event.widget)

    def enter_home_team(self, event):
        self.players(self.home_team_player, self.home_team_pos, self.right_frame, event.widget)

    def get_score(self, event):
        if self.team_score[self.turn][self.inning-1].get() == '-':
            self.team_score[self.turn][self.inning-1].set(0)
        add(self.team_score[self.turn][self.inning-1], int(event.widget["text"]))
        add(self.score_sum[self.turn], int(event.widget["text"]))
        

    def turn_change(self):
        if self.team_score[self.turn][self.inning-1].get() == '-':
            self.team_score[self.turn][self.inning-1].set('0')
        if self.turn == 0:
            self.turn = 1
            self.score_draw()
            if self.inning >= 9 and self.score_sum[0].get() < self.score_sum[1].get():
                self.team_score[1][self.inning-1].set('X')
                self.score_draw(False)
            else:
                self.team_score[self.turn][self.inning-1].set('-')
                self.score_draw()
        else:
            if self.inning >= 9 and self.score_sum[0].get() != self.score_sum[1].get():
                self.score_draw(False)
            else:
                self.turn = 0
                self.inning += 1
                self.score_draw()
                self.team_score[self.turn][self.inning-1].set('-')
            
    def players(self, team_player, team_pos, frame, team='中日'):
        for i in range(len(team_pos)):
            if i == 9:
                number = ttk.Label(frame, text='P', width=1, justify='center')
            else:
                number = ttk.Label(frame, text=i+1, width=1, justify='center')
            number.grid(row=i+1, column=0)
            team_player[i] = ttk.Combobox(frame, width=7)
            team_player[i]['values'] = self.PLAYERS[team.get()]['名前']
            team_player[i].grid(row=i+1, column=1)
            team_pos[i] = ttk.Combobox(frame, width=3)
            team_pos[i]['values'] = ('P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH')
            team_pos[i].grid(row=i+1, column=2)
        team_pos[-1].current(0)

    def score_draw(self, red=True):
        if self.inning >= 10:
            add_inning = self.inning - 9
        else:
            add_inning = 0
        inning_list = range(1+add_inning,10+add_inning)
        
        for j in range(len(inning_list)):
            # 回
            inning_list_show = ttk.Label(self.score_frame, text=inning_list[j], justify='center')
            inning_list_show.grid(row=0, column=j+1)
            for i in range(len(self.team_score)):
                team_score_show = ttk.Label(self.score_frame, textvariable=self.team_score[i][j+add_inning], justify='center', width=2)
                team_score_show.grid(row=i+1, column=j+1)

        if red:
            team_score_show = ttk.Label(self.score_frame, textvariable=self.team_score[self.turn][self.inning-1], justify='center', width=2, foreground='red')
            team_score_show.grid(row=1+self.turn, column=self.inning-add_inning)

    def bso_draw(self):
        self.bso_canvas.delete('all')
        self.bso_canvas.create_text(2, 2, text='B', anchor="nw", fill='black')
        self.bso_canvas.create_text(2, 18, text='S', anchor="nw", fill='black')
        self.bso_canvas.create_text(2, 34, text='O', anchor="nw", fill='black')

        for i in range(self.count[0]):
            self.bso_canvas.create_oval(16+14*i, 4, 16+12+14*i, 4+12, fill="#5d5", outline='white')
        for i in range(self.count[1]):
            self.bso_canvas.create_oval(16+14*i, 20, 16+12+14*i, 20+12, fill="#ee5", outline='white')
        for i in range(self.count[2]):
            self.bso_canvas.create_oval(16+14*i, 36, 16+12+14*i, 36+12, fill="#c00", outline='white')

    def count_add(self, c):
        if (c == 0 and self.count[0] == 3) or (c > 2):
            self.count[0], self.count[1] = 0, 0
            if c == 3:
                add(self.hit[self.turn])
        elif (c == 1 and self.count[1] == 2) or (c == 2):
            self.count[0], self.count[1] = 0, 0
            self.count[2] += 1
            if self.count[2] == 3:
                self.turn_change()
                self.count[2] = 0
        else:
            self.count[c] += 1
        self.bso_draw()

def add(s, num=1):
    s.set(int(s.get())+num)

Baseball(players.PLAYERS)
