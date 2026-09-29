# สรุป Lab04_PWM — STM32

## ความรู้ที่ต้องจำ

PWM แยกความถี่ออกจาก duty ค่า compare มีความหมายตาม counting mode และ polarity จึงต้องวัดที่ขาจริง

**CubeMX:** เลือก timer/channel ที่มี AF pin ว่าง ตั้ง Internal Clock, upcount, PWM Generation CHx และ PWM mode 1, active-high ตัวอย่าง f_TIM=16 MHz ใช้ PSC=15 ARR=999 Pulse=0 ได้ 1 kHz เปิด preload ตามที่จำเป็นและตรวจ pin output

**รีจิสเตอร์สำคัญ:** TIM PSC/ARR คุมความถี่; CCRx คุม compare; CCMRx เลือก PWM; CCER เปิด channel; CR1 เปิด timer; TIM1 ต้องเปิด BDTR.MOE

**จุดผิดพลาดที่ต้องแยกให้ออก:** ไม่มี output: channel/AF/MOE; duty ไม่ตรง: ARR+1 หรือ polarity; สะดุดเมื่อปรับ: preload/update timing

## ก่อนถือว่าจบ Lab

- 10/50/90% คงความถี่ 1 kHz ตาม clock สมมติ
- ค่า -1/101 ถูกปฏิเสธ ไม่ wrap
- 0/100% ให้ระดับปลายช่วงถูกต้องและ CCR อยู่ในช่วง register

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
