# Lab08_I2C_OLED — Python Tkinter

## เป้าหมาย

ส่งข้อความพร้อม validation และแสดงผลตอบจากการอัปเดตจอ

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

Validate ให้ตรงกับความสามารถ firmware/font การมี preview ไม่แทนการตรวจจอจริงและ ACK ไม่รับรองคุณภาพภาพ

Widgets: Entry, character counter, Send, status และ mock preview

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. จำกัดรุ่นแรกเป็น ASCII 1–20 ตัวอักษร ไม่มี comma/newline ตาม protocol
2. preview แสดงสิ่งที่ขอส่งและติดป้ายว่าไม่ใช่ภาพจากจอจริง
3. ส่งแล้วรอ ACK/ERR ไม่แก้ status เป็นสำเร็จก่อนตอบ
4. mock จำลอง NACK/timeout เพื่อฝึก error state
5. เทียบข้อความบน OLED จริงกับคำขอเมื่อ driver พร้อม

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
def validate_oled(text):
    if not (1 <= len(text) <= 20):
        raise ValueError("ใช้ 1-20 ตัวอักษร")
    if any(ord(c) < 32 or ord(c) > 126 or c == "," for c in text):
        raise ValueError("ใช้ ASCII ที่พิมพ์ได้ ยกเว้น comma")
    return text

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- ข้อความปกติส่งได้; ภาษาไทย/comma/newline ถูกปฏิเสธตามรุ่น protocol
- ERR HW แสดง error ไม่แสดง success
- preview ไม่ถูกนำไปอ้างว่าฮาร์ดแวร์แสดงแล้ว

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

ทำไม GUI พิมพ์ภาษาไทยได้แต่ยังไม่ส่งในรุ่นแรก?

แนวตอบ: Tkinter รองรับไม่ได้หมายความว่า protocol/font/controller path พร้อม รุ่นแรกกำหนด ASCII ต้องขยายทั้งระบบก่อน

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

Validate ให้ตรงกับความสามารถ firmware/font การมี preview ไม่แทนการตรวจจอจริงและ ACK ไม่รับรองคุณภาพภาพ

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab08_I2C_OLED/lesson.md)
