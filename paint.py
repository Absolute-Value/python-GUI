#! /usr/bin/env python3
# main.py

import tkinter

class Paint:
    def __init__(self):
        # 操作中の図形のID
        self.curr_id = -1

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
        # ボタン配置
        self.clear_button = tkinter.Button(self.button_frame, text="クリア", command=self.press_save_button)
        self.save_button = tkinter.Button(self.button_frame, text='セーブ')

        #レイアウト
        self.canvas.pack(expand=True, fill=tkinter.BOTH)
        self.button_frame.pack()
        self.clear_button.grid(row=0,column=0)
        self.save_button.grid(row=0,column=1)

        #ウィンドウの表示
        root.mainloop()

    # マウス左ボタン押下
    def on_mouse_left(self, event):
        # 直線描画
        self.curr_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill = "black", width = 5)

    # ドラッグ中
    def dragging(self, event):
        points = self.canvas.coords(self.curr_id)
        points.extend([event.x,event.y])
        self.canvas.coords(self.curr_id, points)

    def press_save_button(self):
        self.canvas.delete('all')

Paint()