# Lab06_Timer: Timer และ Period

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** สร้าง timebase ที่คำนวณได้ก่อนนำไปใช้ PWM

สำหรับ upcounter edge-aligned ที่ใช้ internal clock: `f_update = f_TIM / ((PSC+1)(ARR+1))` ต้องหา f_TIM จาก clock tree จริง เพราะไม่จำเป็นต้องเท่ากับ CPU clock และมีเงื่อนไข prescaler/TIMPRE ตามรุ่น

ตัวอย่างสมมติ f_TIM=16 MHz, PSC=15999, ARR=999 ได้ update 1 Hz ถ้า toggle LED ทุก update จะได้ LED ครบหนึ่งรอบทุก 2 วินาที

**ขั้นตอน:** เลือก timer ที่มีใน F410 → บันทึก clock source → คำนวณค่า → เปิด clock → ตั้ง PSC/ARR → โหลดค่าและจัดการ update flag ตามคู่มือ → start → ตรวจ update แบบ polling ก่อน

**ตรวจผล:** เปรียบเทียบ 100 ms และ 1 s กับการวัด อธิบายผลของการเปลี่ยน PSC เพียงตัวเดียว ระบุข้อจำกัด polling ที่อาจพลาดเหตุการณ์เมื่อ main ทำงานนาน

**คำถาม:** ต้องการ update 10 Hz ที่ f_TIM=16 MHz, PSC=15999 ใช้ ARR เท่าไร? เฉลย 99

**อ่าน:** RM0401 บท RCC และ TIM5; หนังสือบท 10–11

## ตั้งค่า STM32CubeMX

Lab เดี่ยวใช้ TIM5 Internal Clock, Counter Up; ตัวอย่าง f_TIM=16 MHz ตั้ง PSC=15999 ARR=999 ได้ update ทุก 1000 ms เริ่ม polling ก่อน; คง HAL timebase แยกไว้ และอย่าใช้ TIM5 ร่วม encoder ในโปรเจกต์รวมโดยไม่จัดสรรใหม่

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

PSC แบ่ง clock; ARR กำหนดปลาย count; CNT ค่าปัจจุบัน; EGR โหลดค่าผ่าน update; SR.UIF ระบุ update

## ลงมือทีละขั้น

1. เขียนสูตร PSC/ARR และตรวจ clock tree ก่อน generate
2. เริ่ม timer และตรวจ CNT เดิน
3. ใช้ polling UIF ทดลอง 100/1000 ms โดย main ไม่มีงานบล็อก
4. จงใจเพิ่มงานช้าแล้วสังเกต UIF ไม่ใช่ counter จำนวน event
5. ถ้ารับ PERIOD จาก GUI ให้หยุด timer/reload/update/clear flag/restart ตามลำดับที่ตรวจแล้ว จึง ACK

## Pseudocode

clock → prescaler → counter → update flag → application; เปลี่ยน period ต้องจัดการค่า buffered และ pending

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2 */
if (HAL_TIM_Base_Start(&htim5) != HAL_OK) { Error_Handler(); }
__HAL_TIM_CLEAR_FLAG(&htim5, TIM_FLAG_UPDATE);
/* USER CODE BEGIN 3: polling-only experiment */
if (__HAL_TIM_GET_FLAG(&htim5, TIM_FLAG_UPDATE) != RESET) {
    __HAL_TIM_CLEAR_FLAG(&htim5, TIM_FLAG_UPDATE);
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}
```

## ทดสอบและเกณฑ์ผ่าน

- CNT เดินและ wrap ที่ ARR
- คาบตรงกับสูตรภายใต้ clock ที่วัด/ยืนยัน
- อธิบายได้ว่าการ polling ช้าอาจรวมหลาย update เป็นหนึ่ง

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

CNT ไม่เดิน: CEN/clock; คาบสองเท่า: สับสน toggle กับ cycle; เปลี่ยน PSC แล้วไม่ทันที: ค่า buffered ยังไม่ latch

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab06_Timer](../../../../Antigravity-Tkinter/labs/Lab06_Timer/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

Timer ทำงานจาก hardware clock ส่วน main มาสังเกต flag การสังเกตช้าไม่ทำให้ได้จำนวนเหตุการณ์ครบเสมอ

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
