#! /usr/bin/env python3
# main.py

import tkinter
from functools import partial

class Paint:
    def __init__(self):
        # 操作中の図形のID
        self.curr_id = -1
        self.color = "black"

        # メインウィンドウ作成
        root = tkinter.Tk()
        root.title("ペイントソフト")

        #  画像表示用キャンバス作成
        self.canvas = tkinter.Canvas(root, width=800, height=600, bg="white")
        # キーバインド
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_left)
        self.canvas.bind("<B1-Motion>", self.dragging)

        # ボタン配置用フレーム作成
        self.button_frame = tkinter.Frame(root)

        # カラーパレット
        self.color_buttons = []
        for i, color in enumerate(["black", "red", "blue", "green", "yellow"]):
            self.color_buttons.append(tkinter.Button(self.button_frame, text='■', fg=color, width=1, command=partial(self.press_color_button, color)))
            self.color_buttons[i].grid(row=0, column=i)

        # ボタン配置
        self.clear_button = tkinter.Button(self.button_frame, text="クリア", command=self.press_clear_button)
        self.clear_button.grid(row=0,column=5)

        #レイアウト
        self.canvas.pack(expand=True, fill=tkinter.BOTH)
        self.button_frame.pack()

        #ウィンドウの表示
        root.mainloop()

    # マウス左ボタン押下
    def on_mouse_left(self, event):
        # 直線描画
        self.curr_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill = self.color, width = 5, capstyle = tkinter.ROUND)

    # ドラッグ中
    def dragging(self, event):
        points = self.canvas.coords(self.curr_id)
        points.extend([event.x,event.y])
        self.canvas.coords(self.curr_id, points)

    def press_color_button(self, color):
        self.color = color

    def press_clear_button(self):
        self.canvas.delete('all')

Paint()