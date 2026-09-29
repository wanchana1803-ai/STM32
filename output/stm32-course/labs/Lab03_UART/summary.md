# สรุป Lab03_UART — STM32

## ความรู้ที่ต้องจำ

UART เป็น byte stream ไม่ได้แบ่งข้อความให้อัตโนมัติ ต้องออกแบบ framing, buffer, validation และ error recovery ก่อนเชื่อม GUI

**CubeMX:** เลือก USART ที่ขา TX/RX ไม่ชนอุปกรณ์อื่น ตั้ง Asynchronous, 115200, 8 data bits, no parity, 1 stop bit, no flow control ตรวจ AF และ bus clock เปิด NVIC ของ USART เมื่อพัฒนา interrupt reception

**รีจิสเตอร์สำคัญ:** RCC เปิด USART clock; GPIO AFR/MODER เลือก AF; USART BRR กำหนด baud; CR1 เปิด transmitter/receiver; SR/DR ใช้ status/data ตาม RM0401

**จุดผิดพลาดที่ต้องแยกให้ออก:** อักขระเพี้ยน: baud/clock; ไม่มีข้อมูล: TX-RX/GND/AF/port; รับครั้งเดียว: ไม่ re-arm interrupt; GUI เปิด port ไม่ได้: มีโปรแกรมอื่นครอบครอง

## ก่อนถือว่าจบ Lab

- HELLO และ PING ได้ ACK ตรง session/id
- แบ่ง frame หลายส่วนและส่งหลาย frame พร้อมกันได้ผลเท่ากัน
- frame ยาว/เลขผิด/op ไม่รองรับไม่ล้น bufferและรับ frame ดีถัดไปได้

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
