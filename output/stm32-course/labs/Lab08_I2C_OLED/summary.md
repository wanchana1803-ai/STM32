# สรุป Lab08_I2C_OLED — STM32

## ความรู้ที่ต้องจำ

I2C ACK ยืนยันการสื่อสารระดับ bus ไม่ยืนยันว่าจอวาดถูก ต้องตรวจทั้ง transport และ controller driver

**CubeMX:** ยืนยัน OLED controller, ขนาด, address และแรงดันก่อน เลือก I2C instance ที่ใช้งานได้พร้อม SCL/SDA AF open-drain ตรวจ pull-up จริง เริ่ม Standard mode 100 kHz และ timing ตาม clock อย่านำ register ของ FMPI2C ปนกับ I2C ปกติ

**รีจิสเตอร์สำคัญ:** GPIO AF/open-drain; I2C CR/SR/DR และ timing ของ instance; controller OLED มีคำสั่งอีกชุดแยกจาก peripheral MCU

**จุดผิดพลาดที่ต้องแยกให้ออก:** ACK แต่จอมืด: init/controller/contrast; bus busy: pull-up/wiring; อักษรผิด: framebuffer/font/offset

## ก่อนถือว่าจบ Lab

- probe ACK กับ address ที่ถูกและ NACK กับ address ผิด
- ส่งข้อความ 1 และ 20 ตัวอักษรได้โดยไม่ล้น
- จอไม่อยู่แล้ว main/UART ยังทำงานและรายงาน error

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
