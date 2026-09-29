# Lab09_Encoder: Encoder และการวัดรอบ

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** แปลงลำดับสัญญาณ A/B เป็นทิศทางและระยะการหมุน

Quadrature encoder ให้ A และ B เหลื่อมเฟสกัน Timer ที่รองรับ encoder mode ใช้สองช่องรับเพื่อเพิ่ม/ลด counter ได้ ต้องตรวจขา AF คู่และโหมดการนับ x1/x2/x4 ก่อนใช้ค่า pulses per revolution

**ขั้นตอน:** ระบุว่าเป็น knob หรือ encoder เพลา → ตรวจสัญญาณและ pull → เลือก TIM1 หรือ TIM5 ตามทรัพยากรที่เหลือ → ตั้ง input/filter/encoder mode → อ่าน CNT → หมุนจริงหนึ่งรอบแล้วเทียบจำนวน count

**ตรวจผล:** หมุนทั้งสองทิศทางและผ่านจุด counter wrap ได้ สำหรับความเร็วใช้ `RPM=60×delta_count/(counts_per_rev×delta_t_seconds)` โดย delta_count ต้องแก้ wrap และ counts_per_rev ต้องรวม decoding multiplier และอัตราทดที่เกี่ยวข้อง

**คำถาม:** 400 count ต่อรอบ วัด 100 count ใน 0.5 s ได้เท่าไร? 30 RPM

**อ่าน:** RM0401 encoder interface ในบท timer; หนังสือ §11.3.9

## ตั้งค่า STM32CubeMX

ใช้ timer รองรับ encoder เช่น TIM5 ตั้ง Encoder Mode TI1 and TI2 ตรวจ CH1/CH2 AF คู่จริง, polarity, input filter และ period ตามความกว้าง counter ย้าย timer งานอื่นถ้าซ้ำ เริ่ม PSC=0

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

SMCR encoder mode; CCMR input mapping/filter; CCER polarity; CNT count/direction; ARR wrap range

ดู input mapping, filter และการจัดการ counter wrap ใน [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ลงมือทีละขั้น

1. ยืนยันชนิด encoder และแรงดัน output ก่อนต่อ A/B
2. หมุนหนึ่งรอบช้า ๆ บันทึก counts จริงในโหมด decoding ที่เลือก
3. สลับทิศทางและตรวจ signed delta
4. แก้ wrap ของ counter ก่อนสะสมตำแหน่งในชนิดข้อมูลที่พอ
5. คำนวณ RPM เฉพาะเมื่อ encoder ผูกกับเพลาและรู้ counts/rev/gear ratio

## Pseudocode

sample CNT ตามช่วงเวลา → modular delta → unwrap → accumulate position → ถ้าข้อมูล calibration พร้อมจึงคำนวณ RPM

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2 */
if (HAL_TIM_Encoder_Start(&htim5, TIM_CHANNEL_ALL) != HAL_OK) {
    Error_Handler();
}
uint32_t previous = __HAL_TIM_GET_COUNTER(&htim5);
/* Main sample task; assumes a 32-bit full-range TIM5 counter */
uint32_t current = __HAL_TIM_GET_COUNTER(&htim5);
uint32_t modular = current - previous;
int64_t delta = (modular <= 0x7FFFFFFFU)
    ? (int64_t)modular : (int64_t)modular - 4294967296LL;
previous = current;
/* Valid only if travel per sample is less than half the counter range. */
```

## ทดสอบและเกณฑ์ผ่าน

- หนึ่งรอบได้ counts/rev ที่อธิบายได้ทั้งสองทิศ
- ข้าม wrap แล้วยังได้ delta ถูก
- สาย A/B หลวมไม่ถูกแสดงว่าเป็น RPM เชื่อถือได้

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

count กลับด้าน: A/B/polarity; count สั่น: noise/filter; RPM ผิด 4 เท่า: decoding multiplier

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab09_Encoder](../../../../Antigravity-Tkinter/labs/Lab09_Encoder/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

Count เป็นตำแหน่งเชิงดิจิทัล การคำนวณความเร็วต้องรู้เวลา ระยะต่อ count และแก้ counter wrap

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
