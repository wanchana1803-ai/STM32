# Lab04_PWM — Python Tkinter

## เป้าหมาย

สร้าง slider ที่ไม่ยิงคำสั่งถี่เกินและแสดง requested/applied แยกกัน

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

Slider เป็นแหล่งคำขอ ไม่ใช่ผลวัด ต้องจำกัดอัตราส่งและแสดงค่าที่ firmware ยืนยันแยกกัน

Widgets: ttk.Scale, Spinbox, Label percent, ป้าย pending/error

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. สร้างค่ากลาง duty 0–100 และ validate ช่องกรอก
2. slider เปลี่ยนเฉพาะ requested แล้ว debounce ก่อนส่ง 100 ms
3. ถ้ามีคำสั่ง pending เก็บเพียงค่าล่าสุดหนึ่งค่า ไม่สะสมทุกตำแหน่ง
4. ACK ตรง id จึงแก้ applied; disconnect ให้ applied UNKNOWN
5. วัดสัญญาณจริงเทียบค่าที่ GUI แสดง

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
scheduled = None
def on_slider(value):
    global scheduled
    duty = max(0, min(100, round(float(value))))
    requested.set(duty)
    if scheduled is not None:
        root.after_cancel(scheduled)
    scheduled = root.after(100, lambda: request_pwm(duty))

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- ลากเร็วแล้ว queue ไม่โตไม่จำกัด
- กรอกข้อความ/101 แล้วไม่ส่ง
- ACK ช้าทำให้ requested ต่าง applied ได้โดย UI ไม่หลอก

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

เหตุใดไม่ส่งทุกครั้งที่ slider callback ถูกเรียก?

แนวตอบ: ทำให้ UART/command queue ล้นและ ACK ล่าช้า ควร debounce/coalesce ค่าล่าสุด

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

Slider เป็นแหล่งคำขอ ไม่ใช่ผลวัด ต้องจำกัดอัตราส่งและแสดงค่าที่ firmware ยืนยันแยกกัน

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab04_PWM/lesson.md)
