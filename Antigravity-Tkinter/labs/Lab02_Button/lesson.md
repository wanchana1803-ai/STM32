# Lab02_Button — Python Tkinter

## เป้าหมาย

แสดงสถานะและจำนวนกดที่ firmware ยืนยัน โดยไม่เดานับจากอัตรา refresh ของจอ

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

GUI ใช้ stable state และ counter จาก firmware แยกเวลาได้รับข้อมูลจากเวลาเกิดเหตุการณ์ การแสดงซ้ำไม่ใช่การกดใหม่

Widgets: Label แสดง PRESSED/RELEASED, counter, event list และป้ายเวลาข้อมูลล่าสุด

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. ทำ mock ส่ง BUTTON state/count ตามชุดเหตุการณ์ที่กำหนดไว้
2. แสดง count ที่ firmware ส่ง ไม่เพิ่มเองทุกครั้งที่ GUI refresh
3. เพิ่มเวลา received และป้าย stale เมื่อหยุดส่งเกินค่าตั้ง
4. ทดสอบ raw bounce ใน mock firmware แล้วให้ GUI รับเฉพาะ stable event
5. เชื่อมจริงและเทียบจำนวนกดกับการสังเกต 20 ครั้ง

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
def render_button(state, count):
    if state not in (0, 1) or count < 0:
        raise ValueError("invalid button event")
    state_text.set("PRESSED" if state else "RELEASED")
    count_text.set(str(count))
```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- ส่ง event เดิมซ้ำแล้ว count ไม่เพิ่มเอง
- กดค้างแสดง state ค้างแต่ไม่เพิ่ม count
- หยุด telemetry แล้วแสดง stale

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

เหตุใดไม่ควรนับจำนวนกดจากจำนวนข้อความที่รับ?

แนวตอบ: ข้อความอาจซ้ำ/หายและมี state refresh ต้องใช้ counter หรือ event identity ที่ firmware ส่ง

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

GUI ใช้ stable state และ counter จาก firmware แยกเวลาได้รับข้อมูลจากเวลาเกิดเหตุการณ์ การแสดงซ้ำไม่ใช่การกดใหม่

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab02_Button/lesson.md)
