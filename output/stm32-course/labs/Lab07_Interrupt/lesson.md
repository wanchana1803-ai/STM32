# Lab07_Interrupt: Interrupt และ Event

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** ให้ CPU รับเหตุการณ์โดยไม่ต้องวนรออย่างต่อเนื่อง

EXTI จัดการขอบสัญญาณภายนอก ส่วน NVIC จัดการ interrupt ที่ส่งเข้า core ต้องตั้งทั้งแหล่งเหตุการณ์ เส้นทาง mapping mask/trigger และ NVIC ตามชนิด interrupt ISR ควรทำงานสั้น เช่น เก็บเวลา/เพิ่ม counter/ตั้ง flag แล้วให้ main จัดการงานแสดงผล

**ขั้นตอน:** เริ่ม timer interrupt → ตรวจชื่อ handler ใน startup → เปิด peripheral interrupt และ NVIC → เคลียร์ pending ตามคู่มือ → เพิ่ม EXTI button → debounce ใน main

**ตรวจผล:** ให้ LED ทำงานตามเวลาและกดปุ่มพร้อมกัน ต้องไม่มี delay ยาวใน ISR และไม่มี interrupt วนซ้ำจาก pending ที่ไม่ถูกเคลียร์ ถ้าใช้ flag เดียวให้ระบุว่าอาจรวมหลาย event เป็นหนึ่ง หากต้องนับครบให้ใช้ counter/queue และป้องกัน race ตอนอ่านหรือรีเซ็ต

**คำถาม:** volatile ทำให้ `count++` ปลอดภัยจากทุก race หรือไม่? ไม่ เพราะเป็นหลายขั้นตอน

**อ่าน:** RM0401 บท 9; หนังสือบท 7

## ตั้งค่า STM32CubeMX

ใช้ timer จาก Lab06 เปิด NVIC timer interrupt ที่ตรง instance และตรวจ generated handler เรียก HAL_TIM_IRQHandler; สำหรับ EXTI เพิ่ม GPIO_EXTI ตาม edge/pull จริงและเลือก NVIC IRQ ที่ครอบคลุม pin

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

TIM DIER.UIE เปิด update interrupt; SR.UIF pending; NVIC enable/priority; EXTI/SYSCFG route และ edge สำหรับขาภายนอก

ดูเส้นทาง event ถึง ISR และวิธีตรวจ pending ใน [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ลงมือทีละขั้น

1. ตรวจ generated IRQ handler และ breakpoint ใน callback ชั่วคราว
2. ISR เพิ่ม counter อย่างเดียว ไม่ส่ง UART/วาด OLED
3. main อ่าน snapshot ของ aligned uint32_t ที่ ISR เป็นผู้เขียนคนเดียว และส่งอัตราจำกัด
4. ถ้าต้อง reset/read-modify-write counter ให้ทำ critical section ที่เก็บคืน interrupt mask เดิม
5. เพิ่ม EXTI แล้วนำ edge ไป debounce ใน main ไม่ใช้ HAL_Delay ใน ISR

## Pseudocode

hardware event → pending → NVIC → IRQ handler → HAL dispatcher → callback สั้น → main consume snapshot/event

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN PV */
static volatile uint32_t irq_count = 0;
/* USER CODE BEGIN 4: do not duplicate an existing callback */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM5) { ++irq_count; }
}
/* USER CODE BEGIN 2 */
if (HAL_TIM_Base_Start_IT(&htim5) != HAL_OK) { Error_Handler(); }
/* Main may snapshot irq_count; do not reset it concurrently. */
```

## ทดสอบและเกณฑ์ผ่าน

- เพิ่มจำนวน IRQ ได้แม้ main มีงานอื่นระยะสั้น
- ไม่เกิด IRQ loop จาก pending ที่ไม่เคลียร์
- counter wrap หรือ snapshot race มีวิธีจัดการที่อธิบายได้

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

callback ไม่เข้า: NVIC/DIER/handler; ค้าง ISR: delay/printf; count หาย: reset แข่งกับ ISR

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab07_Interrupt](../../../../Antigravity-Tkinter/labs/Lab07_Interrupt/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

Interrupt แยกการรับเหตุการณ์จากงานหลัก ISR ที่สั้นช่วยจำกัด latency แต่ข้อมูลร่วมยังต้องออกแบบ ownership

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
