import tkinter as tk
from tkinter import messagebox, ttk


BACKGROUND = "#101827"
CARD = "#1a2638"
FIELD = "#25344a"
TEXT = "#f4f7fb"
MUTED = "#aab7c8"
ACCENT = "#5eead4"


def calculate_bmi():
    try:
        height_cm = float(height_entry.get())
        weight_kg = float(weight_entry.get())
        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入大於 0 的身高與體重。")
        return

    bmi = weight_kg / (height_cm / 100) ** 2
    if bmi < 18.5:
        status, color = "體重過輕", "#fbbf24"
    elif bmi < 24:
        status, color = "健康正常範圍", ACCENT
    elif bmi < 27:
        status, color = "過重", "#fb923c"
    elif bmi < 30:
        status, color = "輕度肥胖", "#f97316"
    elif bmi < 35:
        status, color = "中度肥胖", "#f43f5e"
    else:
        status, color = "重度肥胖", "#e11d48"

    bmi_value.configure(text=f"{bmi:.2f}", foreground=color)
    status_value.configure(text=status, foreground=color)
    result_hint.configure(text="請持續維持均衡飲食與規律運動")


def reset_form():
    height_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    bmi_value.configure(text="--", foreground=TEXT)
    status_value.configure(text="等待計算", foreground=TEXT)
    result_hint.configure(text="輸入資料後查看你的 BMI 結果")
    height_entry.focus_set()


root = tk.Tk()
root.title("BMI 健康計算器")
root.geometry("760x490")
root.minsize(680, 440)
root.configure(bg=BACKGROUND)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=(16, 10))
style.configure("Accent.TButton", background=ACCENT, foreground=BACKGROUND)
style.map("Accent.TButton", background=[("active", "#99f6e4")])
style.configure("Secondary.TButton", background=FIELD, foreground=TEXT)
style.map("Secondary.TButton", background=[("active", "#334762")])

main = tk.Frame(root, bg=BACKGROUND)
main.pack(fill="both", expand=True, padx=42, pady=34)

header = tk.Frame(main, bg=BACKGROUND)
header.pack(fill="x", pady=(0, 24))
tk.Label(header, text="BMI 健康計算器", font=("Helvetica", 27, "bold"),
         bg=BACKGROUND, fg=TEXT).pack(anchor="w")
tk.Label(header, text="輸入你的身高與體重，快速了解目前的身體質量指數",
         font=("Helvetica", 12), bg=BACKGROUND, fg=MUTED).pack(anchor="w", pady=(7, 0))

content = tk.Frame(main, bg=BACKGROUND)
content.pack(fill="both", expand=True)
content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(1, weight=1)
content.grid_rowconfigure(0, weight=1)

input_card = tk.Frame(content, bg=CARD, padx=28, pady=26)
input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
tk.Label(input_card, text="身體資料", font=("Helvetica", 16, "bold"),
         bg=CARD, fg=TEXT).pack(anchor="w")
tk.Label(input_card, text="請填寫以下欄位", font=("Helvetica", 11),
         bg=CARD, fg=MUTED).pack(anchor="w", pady=(5, 22))

tk.Label(input_card, text="身高（公分）", font=("Helvetica", 11, "bold"),
         bg=CARD, fg=TEXT).pack(anchor="w")
height_entry = tk.Entry(input_card, font=("Helvetica", 15), bg=FIELD, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", bd=0)
height_entry.pack(fill="x", ipady=10, pady=(7, 17))

tk.Label(input_card, text="體重（公斤）", font=("Helvetica", 11, "bold"),
         bg=CARD, fg=TEXT).pack(anchor="w")
weight_entry = tk.Entry(input_card, font=("Helvetica", 15), bg=FIELD, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", bd=0)
weight_entry.pack(fill="x", ipady=10, pady=(7, 22))

buttons = tk.Frame(input_card, bg=CARD)
buttons.pack(fill="x")
ttk.Button(buttons, text="開始計算", command=calculate_bmi,
           style="Accent.TButton").pack(side="left", fill="x", expand=True, padx=(0, 6))
ttk.Button(buttons, text="重設", command=reset_form,
           style="Secondary.TButton").pack(side="left", fill="x", expand=True, padx=(6, 0))

result_card = tk.Frame(content, bg="#20314a", padx=28, pady=26)
result_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
tk.Label(result_card, text="分析結果", font=("Helvetica", 16, "bold"),
         bg="#20314a", fg=TEXT).pack(anchor="w")
tk.Label(result_card, text="Body Mass Index", font=("Helvetica", 11),
         bg="#20314a", fg=MUTED).pack(anchor="w", pady=(5, 25))
bmi_value = tk.Label(result_card, text="--", font=("Helvetica", 48, "bold"),
                     bg="#20314a", fg=TEXT)
bmi_value.pack(anchor="w")
tk.Label(result_card, text="BMI 數值", font=("Helvetica", 11),
         bg="#20314a", fg=MUTED).pack(anchor="w", pady=(0, 25))
status_value = tk.Label(result_card, text="等待計算", font=("Helvetica", 21, "bold"),
                        bg="#20314a", fg=TEXT)
status_value.pack(anchor="w")
result_hint = tk.Label(result_card, text="輸入資料後查看你的 BMI 結果",
                       font=("Helvetica", 10), bg="#20314a", fg=MUTED)
result_hint.pack(anchor="w", pady=(9, 0))

root.bind("<Return>", lambda event: calculate_bmi())
height_entry.focus_set()
root.mainloop()