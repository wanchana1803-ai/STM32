# Lab05_ADC — Python Tkinter

## เป้าหมาย

แสดงตัวเลขและกราฟ bounded history พร้อม export CSV

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

การเก็บ sample และวาดจอมีอัตราต่างกันได้ ต้องจำกัดหน่วยความจำและบันทึกหน่วย/ที่มาของข้อมูล

Widgets: Label raw/mV, Canvas graph, Pause/Resume, Export button

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. รับ ADC telemetry และ validate raw กับหน่วย
2. เก็บข้อมูลไม่เกิน 600 samples ด้วย deque
3. วาดกราฟด้วย Canvas ทุก 100 ms แยกจากความถี่รับข้อมูล
4. Pause หยุดการแสดงผลตามนิยามที่ประกาศ ไม่อ้างว่าหยุด ADC บน MCU
5. Export ด้วย csv module มี timestamp, raw, millivolts, mode และบันทึก VREF ที่ใช้

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
from collections import deque
samples = deque(maxlen=600)
def accept_adc(t_ms, raw, mv):
    if not (0 <= raw <= 4095 and mv >= 0):
        raise ValueError("invalid ADC")
    samples.append((t_ms, raw, mv))
# A separate root.after callback renders the latest samples.

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- raw=0/2048/4095 แสดงถูก ไม่หารด้วยศูนย์ตอนกราฟมี sample เดียว
- รับ 10000 samples แล้ว history ไม่เกิน 600
- export เปิดอ่านกลับแล้วจำนวนแถว/หน่วยตรง

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

ทำไมเวลา PC รับข้อมูลไม่เท่ากับเวลาที่ ADC sample?

แนวตอบ: มีคิวและเวลาเดินทาง Serial ควรใช้ timestamp MCU เพื่อดูช่วง sampling และเก็บ received time แยก

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

การเก็บ sample และวาดจอมีอัตราต่างกันได้ ต้องจำกัดหน่วยความจำและบันทึกหน่วย/ที่มาของข้อมูล

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab05_ADC/lesson.md)
