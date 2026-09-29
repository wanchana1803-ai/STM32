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

สถานะ: ผ่าน — ผู้เรียนทดสอบ LD2 บน NUCLEO-F410RB ด้วย HAL และ register สำเร็จ ใช้ elapsed time แบบไม่บล็อก ตรวจ ODR/MODER และ SysTick และทดลองช่วงเวลา 100/500/1000 ms แล้ว ผลเวลาอ้างอิงการสังเกตด้วยสายตา ยังไม่ได้ยืนยันด้วยเครื่องมือวัด

- วันที่ / รุ่นบอร์ด / toolchain: 29 กันยายน 2026 / NUCLEO-F410RB / STM32CubeIDE
- ค่าที่ตั้งและเหตุผล: PA5 output push-pull; SystemCoreClock=84,000,000 Hz; SysTick LOAD=83,999 ทำให้รอบ SysTick เท่ากับ 1 ms; CTRL[2:0]=7 คือ ENABLE, TICKINT และ CLKSOURCE เปิด
- หลักฐานและผล expected เทียบ actual: LD2 กระพริบที่ interval 100, 500 และ 1000 ms ตามลักษณะที่คาด; ตรวจ MODER5=1 และ ODR5 เปลี่ยนตาม LED; actual เชิงเวลาไม่ได้วัดด้วย oscilloscope หรือ logic analyzer
- ปัญหาที่พบและวิธีแก้: สับสนการแสดง bit field `[10:2]` ใน CubeIDE; แก้โดยอ่านว่าเริ่มบิต 10 ขนาด 2 บิต และตรวจด้วย shift/mask ใน Expressions
- สิ่งที่ยังไม่เข้าใจ: ไม่มีประเด็นค้างที่รายงาน
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป: ผ่านหัวข้อหลักของ Lab01; เริ่ม Lab02 Button และ debounce

[กลับบทเรียน](lesson.md)
