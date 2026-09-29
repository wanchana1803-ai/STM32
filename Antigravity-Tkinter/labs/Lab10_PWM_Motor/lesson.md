# Lab10_PWM_Motor — Python Tkinter

## เป้าหมาย

สร้างหน้าควบคุมมอเตอร์ที่ state ชัดและไม่ replay คำสั่งหลังต่อใหม่

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

State ที่ GUI แสดงต้องตรงกับหลักฐาน การสูญเสีย link ทำให้ผลทางกายภาพไม่ทราบ และ firmware ต้องหยุดเองตาม watchdog

Widgets: ARM, STOP เด่น, duty slider, requested/applied labels, link/fault state และ heartbeat indicator

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. เริ่ม DISARMED และ disable slider จน HELLO และ ARM ACK สำเร็จ
2. ส่ง target ผ่าน MOTOR และแสดง applied จาก MOTOR telemetry แยกกัน
3. ขณะ ARMED จัด PING ทุก 200 ms ตาม protocol แต่ยอมรับว่า scheduling อาจช้า
4. STOP แซง TX queue และยกเลิก pending target; firmware watchdog ยังเป็นตัวคุมเมื่อส่งไม่ได้
5. disconnect/timeout/fault ล้างคำสั่งเก่าและแสดง UNKNOWN หรือ FAULT ไม่ยืนยันหยุดหากไม่มีหลักฐาน
6. ทดสอบ mock fault/link loss ก่อนเชื่อม driver จริง

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
# State transition sketch; transport and widgets are implemented in this Lab.
def on_link_lost():
    pending_controls.clear()
    motor_state.set("UNKNOWN - link lost")
    arm_button.state(["disabled"])
    duty_slider.state(["disabled"])
    # Do not claim physical stop; firmware watchdog must handle loss.

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- เปิด GUI/reconnect แล้วไม่มี MOTOR command อัตโนมัติ
- slider backlog ไม่ขวาง STOP
- ปิดโปรแกรมหรือ mock link loss แล้วไม่แสดง false stopped
- บนบอร์ดจริงพิสูจน์ watchdog ด้วยการหยุด heartbeatและวัด output

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

เมื่อ port หลุดควรตั้งข้อความ STOPPED ทันทีไหม?

แนวตอบ: ไม่ ให้ UNKNOWN/link lost จนมีหลักฐาน Firmware watchdog เป็นผู้สั่งหยุดโดยไม่พึ่ง GUI

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

State ที่ GUI แสดงต้องตรงกับหลักฐาน การสูญเสีย link ทำให้ผลทางกายภาพไม่ทราบ และ firmware ต้องหยุดเองตาม watchdog

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab10_PWM_Motor/lesson.md)
