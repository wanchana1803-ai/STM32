# Lab01_LED: LED และ SysTick

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** ตั้ง GPIO output และสร้างช่วงเวลาจาก clock ที่ทราบค่า

GPIO output ต้องระบุ mode, output type, speed และ pull ขา PA5 ใช้ field MODER[11:10] เพราะแต่ละขาใช้ 2 บิต ส่วน ODR/IDR ใช้หนึ่งบิตต่อขา Output speed ควบคุมลักษณะขอบสัญญาณ ไม่ใช่ความถี่กระพริบ

SysTick เป็นตัวนับถอยหลัง 24 บิต ถ้า clock 16 MHz ต้องใช้ 16,000 clock ต่อ 1 ms ดังนั้น LOAD=15,999 การสลับ LED ทุก 500 ms ทำให้หนึ่งรอบติดและดับใช้ประมาณ 1 วินาที

**ขั้นตอน:** ตรวจวงจร LED → เปิด clock GPIO → ตั้ง output → ทดสอบติด/ดับ → เพิ่ม SysTick → เปลี่ยนช่วง 100/500/1000 ms

**ตรวจผล:** ดู MODER/ODR ใน debugger และวัดคาบด้วยเครื่องมือถ้ามี การมองด้วยตาบอกได้เพียงทำงานคร่าว ๆ ไม่ใช่หลักฐานความแม่นยำระดับ ms

**คำถาม:** ถ้า SysTick ใช้ 8 MHz ค่า LOAD ต่อ 1 ms เท่าไร? เฉลย 7,999

**อ่าน:** RM0401 §5.3.8 และ §6.4; หนังสือบท 6 และ §11.4 ตัวอย่างเต็มอยู่ใน LAB01_LED_SYSTICK.md

## ตั้งค่า STM32CubeMX

เลือกขา LED ที่ตรวจแล้วเป็น GPIO_Output และ User Label เป็น LED; Output Push Pull, No Pull, Low speed; กำหนด initial level ตาม polarity เพื่อให้เริ่มดับ ตั้ง SYS Debug เป็น Serial Wire เพื่อคงขา debug ไว้ ตรวจ clock และคง HAL timebase เดิม

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

RCC AHB1ENR เปิด GPIO clock; MODER เลือก output; OTYPER/PUPDR/OSPEEDR กำหนดลักษณะขา; ODR/BSRR เขียนค่า output

## ลงมือทีละขั้น

1. สร้างโปรเจกต์ CubeMX ตั้ง LED label และ Generate จากนั้น build โปรแกรมเดิมให้ผ่านก่อนเพิ่มโค้ด
2. เพิ่มตัวแปรและโค้ดตามตำแหน่ง USER CODE ที่ระบุ ตรวจ LED สลับทุกประมาณ 500 ms
3. เปลี่ยนเป็น 100 และ 1000 ms บันทึกคาบเต็มซึ่งเป็นสองเท่าของช่วง toggle
4. อ่านค่า register หลัง MX_GPIO_Init และอธิบายเทียบกับค่าที่ตั้งใน CubeMX
5. เมื่อผ่าน HAL แล้วค่อยทำบท SysTick polling แยกตาม LAB01_LED_SYSTICK.md

## Pseudocode

init GPIO/timebase → จำเวลา → วนอ่านเวลา → ถ้าครบ interval ให้ toggle และจำเวลาใหม่ → ทำงานอื่นต่อ

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2: after generated initialization */
uint32_t last_led = HAL_GetTick();
/* USER CODE BEGIN 3: inside while (1) */
uint32_t now = HAL_GetTick();
if ((uint32_t)(now - last_led) >= 500U) {
    last_led = now;
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}
```

## ทดสอบและเกณฑ์ผ่าน

- เริ่มต้นขาตรงกับ initial level ที่ตั้งและ LED ไม่กลับ polarity ผิด
- 100/500/1000 ms ให้คาบประมาณ 200/1000/2000 ms โดยระบุเครื่องมือและความคลาดเคลื่อน
- เพิ่มการอ่านปุ่มหรือ counter ใน main แล้วไม่ติดค้างจาก delay

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

LED ไม่ติด: ตรวจขา/polarity/clock; เวลาเพี้ยน: ตรวจ clock/timebase; regenerate แล้วโค้ดหาย: ตรวจ USER CODE blocks

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab01_LED](../../../../Antigravity-Tkinter/labs/Lab01_LED/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

GPIO กำหนดระดับขา ส่วน timebase กำหนดเวลา การใช้ elapsed time ทำให้ main ทำงานอื่นได้ BSRR ใช้ set/reset เฉพาะบิต ส่วน toggle ต้องระวังผู้เขียนขาร่วมกัน

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
