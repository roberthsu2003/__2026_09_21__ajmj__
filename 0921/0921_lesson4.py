import tkinter as tk
from tkinter import messagebox


def calculate_bmi():
    try:
        height_cm = float(height_entry.get())
        weight_kg = float(weight_entry.get())

        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入大於 0 的數字。")
        return

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        status = "體重過輕"
    elif bmi < 24:
        status = "健康正常範圍"
    elif bmi < 27:
        status = "過重"
    elif bmi < 30:
        status = "輕度肥胖"
    elif bmi < 35:
        status = "中度肥胖"
    else:
        status = "重度肥胖"

    result_label.config(text=f"BMI：{bmi:.2f}\n體重狀態：{status}")


def clear_inputs():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    result_label.config(text="請輸入資料後開始計算")
    height_entry.focus()


window = tk.Tk()
window.title("BMI 計算器")
window.geometry("360x300")
window.resizable(False, False)

title_label = tk.Label(window, text="BMI 計算器", font=("Helvetica", 20, "bold"))
title_label.pack(pady=(24, 18))

form_frame = tk.Frame(window)
form_frame.pack()

tk.Label(form_frame, text="身高（公分）：", font=("Helvetica", 12)).grid(
    row=0, column=0, padx=5, pady=6, sticky="e"
)
height_entry = tk.Entry(form_frame, width=15, font=("Helvetica", 12))
height_entry.grid(row=0, column=1, padx=5, pady=6)

tk.Label(form_frame, text="體重（公斤）：", font=("Helvetica", 12)).grid(
    row=1, column=0, padx=5, pady=6, sticky="e"
)
weight_entry = tk.Entry(form_frame, width=15, font=("Helvetica", 12))
weight_entry.grid(row=1, column=1, padx=5, pady=6)

button_frame = tk.Frame(window)
button_frame.pack(pady=16)
tk.Button(button_frame, text="計算 BMI", width=10, command=calculate_bmi).pack(
    side=tk.LEFT, padx=5
)
tk.Button(button_frame, text="清除", width=10, command=clear_inputs).pack(
    side=tk.LEFT, padx=5
)

result_label = tk.Label(
    window,
    text="請輸入資料後開始計算",
    font=("Helvetica", 13),
    fg="#1f4e79",
    justify=tk.CENTER,
)
result_label.pack(pady=8)

height_entry.focus()
window.mainloop()