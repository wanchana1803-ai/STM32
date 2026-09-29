# Lab07_Interrupt — Python Tkinter

## เป้าหมาย

แสดง interrupt counters และ event stream โดยไม่ redraw จน UI ค้าง

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

จำนวน interrupt จำนวน telemetry frame และจำนวนแถวบนจอเป็นคนละสิ่ง ต้องแยก counters และจำกัดคิว

Widgets: Treeview event log, counter, dropped-frame label, Clear View

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. mock burst telemetry 1000 frame แล้วให้ UI drain ครั้งละจำกัด
2. เก็บ Treeview ไม่เกิน 500 rows และ queue มีขอบเขต
3. Clear View ล้างเฉพาะจอ ไม่ส่ง reset counter ถ้า protocol ไม่มีคำสั่ง
4. แสดง irq_count สะสมกับจำนวน frame ที่รับแยกกัน
5. ตรวจ missing seq และนับ dropped ไม่แต่ง event ขึ้นมา

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
MAX_ROWS = 500
def append_event(values):
    tree.insert("", "end", values=values)
    rows = tree.get_children()
    if len(rows) > MAX_ROWS:
        tree.delete(*rows[:len(rows) - MAX_ROWS])

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- burst แล้วปุ่ม/ปิดหน้าต่างยังตอบสนอง
- Clear View ไม่ทำให้ MCU counter เป็นศูนย์
- frame drop แสดงตัวนับและค่าล่าสุดได้

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

ถ้า irq_count เพิ่ม 100 แต่ GUI รับ 10 frame แปลว่าหาย 90 interrupt หรือไม่?

แนวตอบ: ไม่จำเป็น firmware อาจรายงาน counter แบบ batch ต้องดู protocol/seq และความถี่ publish

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

จำนวน interrupt จำนวน telemetry frame และจำนวนแถวบนจอเป็นคนละสิ่ง ต้องแยก counters และจำกัดคิว

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab07_Interrupt/lesson.md)
