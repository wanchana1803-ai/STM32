# Lab01_LED — Python Tkinter

## เป้าหมาย

สร้างหน้าต่างควบคุม LED แบบ mock และแยกค่าที่ขอออกจากค่าที่อุปกรณ์ยืนยัน

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

Tkinter callback สร้างคำสั่ง ส่วน ACK ยืนยัน state การเปลี่ยนสีปุ่มอย่างเดียวไม่พิสูจน์ว่า LED บนบอร์ดติด

Widgets: ttk.Frame, Label, Button, StringVar และ Canvas วงกลมสถานะ

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. วาดปุ่ม ON/OFF และป้าย MOCK, DISCONNECTED, confirmed=UNKNOWN
2. สร้าง callback ที่สร้าง CMD LED แล้วตั้ง pending โดยไม่แก้ confirmed ทันที
3. mock transport รับคำสั่งแล้วใช้ after จำลอง ACK หลัง 100 ms; ใช้ session/id ตาม protocol
4. เมื่อ ACK ตรง id จึงเปลี่ยนวงกลมและ confirmed; ถ้า timeout ให้ UNKNOWN
5. หลัง Lab03 เปลี่ยน transport เป็น Serial โดยไม่เปลี่ยน view

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
pending_id = 2
status.set("กำลังรอยืนยัน")
# Call from a main-thread event handler after parsing a matching ACK:
def show_led_ack(value):
    confirmed.set("ON" if value == 1 else "OFF")
    status.set("ยืนยันแล้ว")
```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- กด ON ได้ pending ก่อน confirmed ON
- mock ไม่ตอบต้องขึ้น timeout ไม่ขึ้นสำเร็จ
- ACK id เก่าไม่เปลี่ยนสถานะคำสั่งปัจจุบัน

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

ถ้าได้รับ ACK ของคำสั่ง OFF หลังคำสั่ง ON ล่าสุดควรทำอย่างไร?

แนวตอบ: เทียบ session/id กับ pending และไม่ใช้ ACK เก่าอัปเดตคำสั่งล่าสุด

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

Tkinter callback สร้างคำสั่ง ส่วน ACK ยืนยัน state การเปลี่ยนสีปุ่มอย่างเดียวไม่พิสูจน์ว่า LED บนบอร์ดติด

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab01_LED/lesson.md)
