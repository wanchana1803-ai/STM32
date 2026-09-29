# เปิดหลักสูตรนี้ใน Google Antigravity

เปิดโฟลเดอร์ `Antigravity-Tkinter` เป็น workspace แล้วเริ่มด้วยข้อความ:

> ใช้ skill stm32-tkinter-tutor อ่าน roadmap.md และเริ่มสอนพื้นฐาน Python/Tkinter ก่อน Lab01 ทีละขั้น ใช้ mock mode ก่อน จบแต่ละ Lab ให้สรุปความรู้และบันทึกผลจริง

Skill อยู่ใน [.agents/skills/stm32-tkinter-tutor/SKILL.md](.agents/skills/stm32-tkinter-tutor/SKILL.md) ใช้ชื่อ SKILL.md ตัวพิมพ์ใหญ่ตามรูปแบบ Agent Skills โฟลเดอร์ `.agents/skills` เป็นตำแหน่ง workspace skill ตาม [เอกสาร Google Antigravity](https://antigravity.google/docs/skills) หากเปิดโฟลเดอร์ GPT ที่อยู่เหนือขึ้นไปแทน ให้ชี้ไฟล์ skill นี้ในคำสั่งโดยตรง

เริ่มอ่าน [roadmap.md](roadmap.md), [สรุปครบ 10 Lab](LAB_SUMMARIES.md), [สัญญาการสื่อสาร](protocol.md) และ [ความคืบหน้า](progress.md)

ชุดนี้เป็นบทเรียนและใบงานครบ 10 Lab สำหรับให้ Antigravity พาสร้าง GUI ไม่ใช่แอปสำเร็จรูปหรือ firmware ที่ flash ได้ทันที ยังไม่มีการทดสอบ Serial/บอร์ดจริง การใช้ mock เป็นส่วนแรกของหลักสูตร ไม่ต้องรอซื้ออุปกรณ์เพิ่ม

## เตรียม Python

ตรวจ interpreter ที่ใช้จริง แล้วรัน `python --version` และ `python -m tkinter` ใน terminal ของคุณ คำสั่งหลังควรเปิดหน้าต่างทดสอบ Tk ถ้าใช้ Python launcher บน Windows อาจใช้ `py` แทน `python` เมื่อมีอยู่

ก่อน Lab03 สร้าง virtual environment เช่น `python -m venv .venv` แล้วใช้ interpreter ในนั้นติดตั้ง `pyserial` ด้วย `python -m pip install pyserial` บันทึกเวอร์ชันที่ใช้ Tkinter ไม่ใช่ package ที่ควรติดตั้งด้วย pip

## ตัวอย่างเริ่มต้นที่รันได้

บันทึกเป็น `hello_tk.py` เมื่อเริ่มเรียน:

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("STM32 GUI - MOCK")
status = tk.StringVar(value="พร้อมเรียน")
ttk.Label(root, textvariable=status).pack(padx=24, pady=12)
ttk.Button(root, text="ทดลอง", command=lambda: status.set("callback ทำงานแล้ว")).pack(pady=12)
root.mainloop()
```

ผลที่คาด: หน้าต่างตอบสนองต่อปุ่มและปิดได้ ไม่มีการเชื่อมบอร์ดจากตัวอย่างนี้
