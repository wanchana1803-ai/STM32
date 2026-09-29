# Lab04_PWM: PWM ควบคุม Duty

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** ปรับ duty โดยคงความถี่ และตรวจสัญญาณที่ขาจริง

สำหรับ PWM mode 1 แบบ active-high, edge-aligned upcount: `f_PWM=f_TIM/((PSC+1)(ARR+1))` และในช่วงทั่วไป `duty=CCR/(ARR+1)` ตัวอย่าง f_TIM=16 MHz, PSC=15, ARR=999 ได้ 1 kHz ค่า CCR=100/500/900 ให้ 10/50/90%

**ขั้นตอน:** เลือก timer/channel/AF pin ที่รองรับ → ตั้ง PWM → เริ่มที่ 0% → ทดสอบ 10/50/90% ด้วย LED → เปลี่ยน duty โดยใช้ preload ตามคู่มือ ถ้าใช้ TIM1 ต้องตรวจ main output enable ด้วย

**ตรวจผล:** วัด frequency และ high time ทุกค่า ความสว่างที่ตาเห็นไม่เป็นสัดส่วนเชิงเส้นกับ duty เสมอไป กรณี 100% ต้องตรวจขอบเขต CCR/ARR และความกว้าง register ไม่เพิ่ม ARR+1 จนล้น

**คำถาม:** จากตัวอย่างต้องการ 25% ให้ CCR เท่าไร? เฉลย 250

**อ่าน:** RM0401 TIM1/TIM5; หนังสือ §11.3.7

## ตั้งค่า STM32CubeMX

เลือก timer/channel ที่มี AF pin ว่าง ตั้ง Internal Clock, upcount, PWM Generation CHx และ PWM mode 1, active-high ตัวอย่าง f_TIM=16 MHz ใช้ PSC=15 ARR=999 Pulse=0 ได้ 1 kHz เปิด preload ตามที่จำเป็นและตรวจ pin output

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

TIM PSC/ARR คุมความถี่; CCRx คุม compare; CCMRx เลือก PWM; CCER เปิด channel; CR1 เปิด timer; TIM1 ต้องเปิด BDTR.MOE

ดูสูตร clock ฟิลด์ PWM และขั้นตรวจ output ใน [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ลงมือทีละขั้น

1. คำนวณ f_TIM จาก clock tree ไม่ใช้ SYSCLK แทนโดยไม่ตรวจ
2. เริ่ม PWM 0% แล้วทดลอง 10/50/90% กับ LED
3. วัด period/high time และเทียบสูตร
4. เขียน function รับ percent ตรวจ 0–100 แล้วแปลง CCR โดยไม่ล้น
5. รับ operation PWM จาก UART และ ACK ค่าที่ใช้จริงหลังตรวจช่วง

## Pseudocode

validate percent → CCR=(ARR+1)×percent/100 → เขียน preload → timer latch ตาม update → ACK accepted duty

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2: example TIM1 CH1, adapt to .ioc */
if (HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1) != HAL_OK) {
    Error_Handler();
}
/* ARR=999 in this example; 250/1000 = 25% */
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 250U);
```

## ทดสอบและเกณฑ์ผ่าน

- 10/50/90% คงความถี่ 1 kHz ตาม clock สมมติ
- ค่า -1/101 ถูกปฏิเสธ ไม่ wrap
- 0/100% ให้ระดับปลายช่วงถูกต้องและ CCR อยู่ในช่วง register

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

ไม่มี output: channel/AF/MOE; duty ไม่ตรง: ARR+1 หรือ polarity; สะดุดเมื่อปรับ: preload/update timing

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab04_PWM](../../../../Antigravity-Tkinter/labs/Lab04_PWM/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

PWM แยกความถี่ออกจาก duty ค่า compare มีความหมายตาม counting mode และ polarity จึงต้องวัดที่ขาจริง

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
