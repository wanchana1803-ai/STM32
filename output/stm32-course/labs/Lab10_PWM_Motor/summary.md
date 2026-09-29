# สรุป Lab10_PWM_Motor — STM32

## ความรู้ที่ต้องจำ

การควบคุมมอเตอร์ต้องมี output state ที่แน่นอนและทางหยุดใน firmware GUI เป็นผู้ขอคำสั่ง ไม่ควรเป็นชั้นเดียวที่ดูแล link loss

**CubeMX:** ยืนยัน motor DC brushed/driver/แหล่งจ่ายและ stop truth table ก่อน กำหนด PWM channel, enable pin และ initial output ให้หยุดตั้งแต่ boot คง SWD/UART และจัด timer ของ encoder/timebase ไม่ให้ชน เลือก PWM frequency ตาม driver จริง

**รีจิสเตอร์สำคัญ:** TIM PWM/CCR/MOE และ GPIO driver enable; firmware state/watchdog เป็นอีกชั้น ไม่ได้เกิดเองจาก CubeMX

**จุดผิดพลาดที่ต้องแยกให้ออก:** boot กระตุก: pin default/driver enable; STOP ช้า: blocking loop/TX queue; duty เปลี่ยนแต่ RPM ไม่ตาม: โหลด/ไฟ/feedback

## ก่อนถือว่าจบ Lab

- boot/reset/reconnect ไม่หมุนเองและต้อง ARM ใหม่
- หยุด PING เกิน watchdog แล้ว firmware หยุดแม้ GUI ค้าง
- STOP ยกเลิก ramp ไม่รอให้ duty ลดช้า ๆ
- OLED/UART error ไม่ทำให้ main หยุดตรวจ watchdog

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
