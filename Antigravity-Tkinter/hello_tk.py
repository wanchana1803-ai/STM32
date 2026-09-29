import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("STM32 GUI - MOCK (ทดสอบเริ่มต้น)")
    root.geometry("320x160")

    status = tk.StringVar(value="พร้อมเรียน")

    # ป้ายแสดงสถานะ
    lbl = ttk.Label(root, textvariable=status, font=("Segoe UI", 12))
    lbl.pack(padx=24, pady=16)

    # ปุ่มทดสอบ callback
    btn = ttk.Button(root, text="ทดลองกดปุ่ม", command=lambda: status.set("Callback ทำงานแล้ว!"))
    btn.pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    main()
