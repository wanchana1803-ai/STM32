# Lab06_Timer — Python Tkinter

## เป้าหมาย

ตั้ง period และเปรียบเทียบ timestamp MCU กับ callback UI

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

after จัดตาราง UI ไม่ได้แทน hardware timer การวิเคราะห์เวลาต้องรู้ว่า timestamp มาจากฝั่งใด

Widgets: Spinbox 10–5000 ms, Apply, labels requested/confirmed, ตาราง timestamp

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. validate period เป็นจำนวนเต็มและส่งเฉพาะกด Apply
2. รอ ACK ก่อนยืนยันค่าใหม่
3. รับ TIMER telemetry ที่มี MCU ms/update_count
4. คำนวณ delta ด้วย unsigned wrap สำหรับ tick MCU แยกจาก received time ฝั่ง PC
5. ทำ UI tick ด้วย after แล้วทดลองลากหน้าต่าง/งานอื่นเพื่อดู jitter

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
def tick_delta_ms(new, old):
    return (new - old) & 0xFFFFFFFF

def ui_heartbeat():
    ui_tick.set(ui_tick.get() + 1)
    root.after(100, ui_heartbeat)
# 100 ms is a scheduling request, not a precise hardware period.

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- 10/1000/5000 ส่งได้และ 0/5001 ไม่ส่ง
- old=0xFFFFFFF0,new=0x10 ได้ delta=32
- UI delay ไม่ถูกบันทึกเป็น timer error ฝั่ง MCU โดยอัตโนมัติ

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

ถ้า UART รวม 10 timer updates เป็น telemetry เดียวควรคำนวณ period อย่างไร?

แนวตอบ: ใช้ delta MCU time และ delta update_count ที่สอดคล้องกัน ไม่ถือว่าช่องว่างระหว่าง frame คือ period หนึ่งรอบ

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

after จัดตาราง UI ไม่ได้แทน hardware timer การวิเคราะห์เวลาต้องรู้ว่า timestamp มาจากฝั่งใด

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab06_Timer/lesson.md)
