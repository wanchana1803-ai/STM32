# Lab02_Button: Button และ Debounce

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** แยกระดับลอจิกออกจากเหตุการณ์กดปุ่ม

Input ที่ไม่มี pull อาจลอย ปุ่มต่อ GND พร้อม pull-up จะอ่าน 1 ตอนปล่อยและ 0 ตอนกด หน้าสัมผัสอาจเด้งหลายครั้ง จึงต้องยืนยันสถานะคงที่ก่อนนับเป็นเหตุการณ์

**อัลกอริทึม:** อ่าน raw → ถ้า raw เปลี่ยนให้จำเวลา → ถ้าคงเดิมเกินช่วง debounce ที่ทดลอง เช่น 20 ms ให้ยอมรับเป็น stable → สร้าง pressed event เฉพาะขอบปล่อยไปกด ค่า 20 ms เป็นจุดเริ่มทดลอง ไม่ใช่ค่าที่เหมาะกับปุ่มทุกตัว

**ขั้นตอน:** เลือกขา input → อ่าน IDR → แสดงสถานะผ่าน LED → เพิ่ม debounce ด้วยเวลา → แยก pressed/released

**ตรวจผล:** กดช้า 20 ครั้งและกดค้าง 3 วินาที ต้องนับ 20 ครั้งและไม่เพิ่มซ้ำขณะค้าง ทดลองกดเร็วเพื่อหาขีดจำกัดของการกรอง

**คำถาม:** ทำไม toggle LED ทุกครั้งที่อ่านค่า 0 จึงผิด? เพราะ main อ่านซ้ำหลายรอบระหว่างการกดครั้งเดียว ต้องตอบสนองต่อ event

**อ่าน:** RM0401 GPIO IDR/PUPDR; หนังสือบท 6

## ตั้งค่า STM32CubeMX

เลือก input pin ที่ว่างและตั้ง User Label เป็น BUTTON; ตัวอย่างนี้ปุ่มต่อ GND จึงใช้ Pull-up และ active-low ใช้ GPIO_Input ก่อน EXTI ขา LED ใช้ค่าจาก Lab01

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

GPIO IDR อ่านค่าขา; PUPDR เลือก pull-up; MODER=00 เลือก input; debounce เป็น logic เวลาใน application

## ลงมือทีละขั้น

1. ต่อปุ่ม GND และเปิด pull-up ตามวงจรที่ตรวจจริง
2. ดู raw ใน debugger ตอนปล่อย/กดก่อนเพิ่ม debounce
3. เพิ่มโค้ดกรอง stable 20 ms และดู presses
4. ทดสอบกดค้างและกดติดกันแล้วปรับ debounce ตามผลจริง
5. หลัง Lab03 ให้ main ส่ง BUTTON event เฉพาะเมื่อ stable เปลี่ยน ไม่ส่งทุก loop

## Pseudocode

raw เปลี่ยน → จำเวลา → รอ stable ครบ debounce → ยอมรับ state → นับเฉพาะขอบกด

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2 */
GPIO_PinState raw_prev = HAL_GPIO_ReadPin(BUTTON_GPIO_Port, BUTTON_Pin);
GPIO_PinState stable = raw_prev;
uint32_t changed_at = HAL_GetTick(), presses = 0;
/* USER CODE BEGIN 3 */
uint32_t now = HAL_GetTick();
GPIO_PinState raw = HAL_GPIO_ReadPin(BUTTON_GPIO_Port, BUTTON_Pin);
if (raw != raw_prev) { raw_prev = raw; changed_at = now; }
if (raw != stable && (uint32_t)(now - changed_at) >= 20U) {
    stable = raw;
    if (stable == GPIO_PIN_RESET) { ++presses; }
}
```

## ทดสอบและเกณฑ์ผ่าน

- กด 20 ครั้งต้องเพิ่ม 20 ไม่เพิ่มซ้ำตอนค้าง
- เปิดเครื่องพร้อมกดค้าง: ไม่ถือเป็นขอบกดใหม่ในตัวอย่างนี้จนปล่อยและกดอีกครั้ง
- ทดลองกดเร็วกว่า debounce แล้วอธิบายเหตุการณ์ที่ถูกกรอง

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

ค่าลอย: ตรวจ pull/GND; นับซ้ำ: นับระดับแทน edge; ไม่ตอบกดเร็ว: debounce ยาวเกิน

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab02_Button](../../../../Antigravity-Tkinter/labs/Lab02_Button/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

ปุ่มให้ระดับสัญญาณ แต่โปรแกรมต้องสร้างเหตุการณ์จากขอบ Debounce ลดผลหน้าสัมผัสเด้ง โดยแลกกับเวลาในการตอบสนอง

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
