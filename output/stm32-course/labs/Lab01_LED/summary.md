# สรุป Lab01_LED — STM32

## ความรู้ที่ต้องจำ

GPIO กำหนดระดับขา ส่วน timebase กำหนดเวลา การใช้ elapsed time ทำให้ main ทำงานอื่นได้ BSRR ใช้ set/reset เฉพาะบิต ส่วน toggle ต้องระวังผู้เขียนขาร่วมกัน

**CubeMX:** เลือกขา LED ที่ตรวจแล้วเป็น GPIO_Output และ User Label เป็น LED; Output Push Pull, No Pull, Low speed; กำหนด initial level ตาม polarity เพื่อให้เริ่มดับ ตั้ง SYS Debug เป็น Serial Wire เพื่อคงขา debug ไว้ ตรวจ clock และคง HAL timebase เดิม

**รีจิสเตอร์สำคัญ:** RCC AHB1ENR เปิด GPIO clock; MODER เลือก output; OTYPER/PUPDR/OSPEEDR กำหนดลักษณะขา; ODR/BSRR เขียนค่า output

**จุดผิดพลาดที่ต้องแยกให้ออก:** LED ไม่ติด: ตรวจขา/polarity/clock; เวลาเพี้ยน: ตรวจ clock/timebase; regenerate แล้วโค้ดหาย: ตรวจ USER CODE blocks

## ก่อนถือว่าจบ Lab

- เริ่มต้นขาตรงกับ initial level ที่ตั้งและ LED ไม่กลับ polarity ผิด
- 100/500/1000 ms ให้คาบประมาณ 200/1000/2000 ms โดยระบุเครื่องมือและความคลาดเคลื่อน
- เพิ่มการอ่านปุ่มหรือ counter ใน main แล้วไม่ติดค้างจาก delay

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
