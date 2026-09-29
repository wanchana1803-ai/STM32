# Lab10_PWM_Motor: PWM Motor และการรวมระบบ

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** ใช้ PWM สั่ง driver และอธิบายความต่างระหว่าง duty กับความเร็วจริง

GPIO ไม่ใช่แหล่งจ่ายมอเตอร์ ต้องใช้ driver ที่เหมาะกับชนิดมอเตอร์ แรงดันและกระแส โดยตรวจการป้องกันแรงดันย้อนจากวงจร/โมดูลที่ใช้ กำหนดไฟเลี้ยงและ GND ตาม datasheet driver เริ่มการทดลองจาก motor DC แบบ brushed หนึ่งตัวเมื่อยืนยันรุ่นแล้ว

**ขั้นตอน:** ทดสอบ PWM ด้วย LED ก่อน → ตรวจ truth table ของ driver → ตั้ง default disabled → ต่อระบบโดยยังไม่จ่ายไฟมอเตอร์ → เริ่ม duty ต่ำ → เพิ่มแบบ ramp → เพิ่มคำสั่ง stop → เพิ่มข้อมูล encoder ถ้ามี

**ตรวจผล:** เปิดเครื่องต้องหยุด, คำสั่งหยุดต้องตอบสนองตามเวลาที่กำหนด, เปลี่ยน duty แล้ววัดความเร็วจริง, reset แล้วไม่เริ่มหมุนเอง อย่าทดสอบ stall โดยไม่ทราบขีดจำกัดกระแสและอุณหภูมิ

**คำถาม:** duty 50% แปลว่า RPM ครึ่งหนึ่งของสูงสุดเสมอหรือไม่? ไม่ ขึ้นกับโหลด แรงดัน ความฝืด และคุณสมบัติมอเตอร์

**อ่าน:** บท PWM/Timer, เพิ่ม datasheet driver และ motor เมื่อทราบรุ่น

## ตั้งค่า STM32CubeMX

ยืนยัน motor DC brushed/driver/แหล่งจ่ายและ stop truth table ก่อน กำหนด PWM channel, enable pin และ initial output ให้หยุดตั้งแต่ boot คง SWD/UART และจัด timer ของ encoder/timebase ไม่ให้ชน เลือก PWM frequency ตาม driver จริง

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

TIM PWM/CCR/MOE และ GPIO driver enable; firmware state/watchdog เป็นอีกชั้น ไม่ได้เกิดเองจาก CubeMX

## ลงมือทีละขั้น

1. ทดสอบช่อง PWM ด้วย LED/logic analyzer ก่อนต่อภาคกำลัง
2. ทำ state machine และ watchdog แล้วจำลอง timeout บน firmware
3. ตรวจ boot/reset/new session/STOP ทั้งหมดกลับ output หยุด
4. ต่อ driver ที่ยืนยันแล้วและเริ่ม duty ต่ำภายใต้เงื่อนไขอุปกรณ์จริง
5. เพิ่ม ramp และ telemetry applied duty; command ACK หมายถึงรับ target ไม่ใช่ RPM ถึงเป้า
6. รวม ADC/OLED/encoder โดยใช้ resource allocation ที่ตรวจ pin/timer conflict

## Pseudocode

ทุก loop: จัดการ STOP/fault/watchdog ก่อน → parse control → update ramp ตามเวลา → sample/report แบบมีขอบเขต

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```text
/* Pseudocode only: implement driver_* for the actual driver. */
on_boot_or_new_session:
    driver_stop(); state = DISARMED; target = applied = 0;
on_ARM_if_no_fault:
    target = applied = 0; state = ARMED;
on_MOTOR_if_armed_and_percent_valid:
    target = requested;
on_STOP_or_watchdog_or_fault:
    driver_stop(); state = DISARMED; target = applied = 0;
periodic_nonblocking_task:
    if state == ARMED: ramp_applied_toward_target();
```

## ทดสอบและเกณฑ์ผ่าน

- boot/reset/reconnect ไม่หมุนเองและต้อง ARM ใหม่
- หยุด PING เกิน watchdog แล้ว firmware หยุดแม้ GUI ค้าง
- STOP ยกเลิก ramp ไม่รอให้ duty ลดช้า ๆ
- OLED/UART error ไม่ทำให้ main หยุดตรวจ watchdog

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

boot กระตุก: pin default/driver enable; STOP ช้า: blocking loop/TX queue; duty เปลี่ยนแต่ RPM ไม่ตาม: โหลด/ไฟ/feedback

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab10_PWM_Motor](../../../../Antigravity-Tkinter/labs/Lab10_PWM_Motor/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

การควบคุมมอเตอร์ต้องมี output state ที่แน่นอนและทางหยุดใน firmware GUI เป็นผู้ขอคำสั่ง ไม่ควรเป็นชั้นเดียวที่ดูแล link loss

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
