# สรุป Lab09_Encoder — STM32

## ความรู้ที่ต้องจำ

Count เป็นตำแหน่งเชิงดิจิทัล การคำนวณความเร็วต้องรู้เวลา ระยะต่อ count และแก้ counter wrap

**CubeMX:** ใช้ timer รองรับ encoder เช่น TIM5 ตั้ง Encoder Mode TI1 and TI2 ตรวจ CH1/CH2 AF คู่จริง, polarity, input filter และ period ตามความกว้าง counter ย้าย timer งานอื่นถ้าซ้ำ เริ่ม PSC=0

**รีจิสเตอร์สำคัญ:** SMCR encoder mode; CCMR input mapping/filter; CCER polarity; CNT count/direction; ARR wrap range

**จุดผิดพลาดที่ต้องแยกให้ออก:** count กลับด้าน: A/B/polarity; count สั่น: noise/filter; RPM ผิด 4 เท่า: decoding multiplier

## ก่อนถือว่าจบ Lab

- หนึ่งรอบได้ counts/rev ที่อธิบายได้ทั้งสองทิศ
- ข้าม wrap แล้วยังได้ delta ถูก
- สาย A/B หลวมไม่ถูกแสดงว่าเป็น RPM เชื่อถือได้

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
