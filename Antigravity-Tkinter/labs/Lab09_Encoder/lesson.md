# Lab09_Encoder — Python Tkinter

## เป้าหมาย

แสดงตำแหน่งทิศทางและความเร็วที่มีเงื่อนไข calibration ชัดเจน

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

RPM ต้องมี calibration และเวลาอ้างอิง ไม่ใช่เพียงนำ counter ไปใส่กราฟ การ reconnect ทำให้ baseline เดิมใช้ไม่ได้

Widgets: count label, direction indicator, counts/rev input, RPM label และ calibration status

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. ใช้ signed_count ที่ firmware unwrap แล้ว ไม่แก้ timer wrap ซ้ำใน GUI
2. วัด delta position/delta MCU timestamp แล้วคำนวณ RPM เมื่อเป็น shaft sensor
3. ถ้าเป็น rotary knob แสดง count/direction อย่างเดียว
4. ถ้า delta_t=0 หรือข้อมูลเก่าแสดง unavailable ไม่หาร
5. reconnect ล้าง baseline และไม่ใช้ delta ข้าม session

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
def rpm_from_delta(delta_count, dt_ms, counts_per_rev):
    if dt_ms <= 0 or counts_per_rev <= 0:
        return None
    return 60000.0 * delta_count / (counts_per_rev * dt_ms)

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- 100 counts ใน 500 ms ที่ 400 counts/rev ได้ 30 RPM
- delta_t=0 คืน unavailable
- session ใหม่ต้องรอ sample ที่สองก่อนคำนวณ

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

encoder knob หมุนด้วยมือใช้แสดง RPM มอเตอร์ได้หรือไม่?

แนวตอบ: ไม่ได้ ถ้าไม่ได้วัดเพลามอเตอร์นั้น ต้องแยกเป็น input knob และ shaft feedback

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

RPM ต้องมี calibration และเวลาอ้างอิง ไม่ใช่เพียงนำ counter ไปใส่กราฟ การ reconnect ทำให้ baseline เดิมใช้ไม่ได้

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab09_Encoder/lesson.md)
