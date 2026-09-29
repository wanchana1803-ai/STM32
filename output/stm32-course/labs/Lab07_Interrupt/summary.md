# สรุป Lab07_Interrupt — STM32

## ความรู้ที่ต้องจำ

Interrupt แยกการรับเหตุการณ์จากงานหลัก ISR ที่สั้นช่วยจำกัด latency แต่ข้อมูลร่วมยังต้องออกแบบ ownership

**CubeMX:** ใช้ timer จาก Lab06 เปิด NVIC timer interrupt ที่ตรง instance และตรวจ generated handler เรียก HAL_TIM_IRQHandler; สำหรับ EXTI เพิ่ม GPIO_EXTI ตาม edge/pull จริงและเลือก NVIC IRQ ที่ครอบคลุม pin

**รีจิสเตอร์สำคัญ:** TIM DIER.UIE เปิด update interrupt; SR.UIF pending; NVIC enable/priority; EXTI/SYSCFG route และ edge สำหรับขาภายนอก

**จุดผิดพลาดที่ต้องแยกให้ออก:** callback ไม่เข้า: NVIC/DIER/handler; ค้าง ISR: delay/printf; count หาย: reset แข่งกับ ISR

## ก่อนถือว่าจบ Lab

- เพิ่มจำนวน IRQ ได้แม้ main มีงานอื่นระยะสั้น
- ไม่เกิด IRQ loop จาก pending ที่ไม่เคลียร์
- counter wrap หรือ snapshot race มีวิธีจัดการที่อธิบายได้

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
