# Lab03_UART: UART และ Serial Protocol

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** ใช้ข้อความเป็นเครื่องมือสังเกตและสั่งงานระบบ

UART ต้องตกลง baud rate, data bits, parity และ stop bits ให้ตรงกัน ขา TX/RX ต้องเป็น alternate function ที่ถูกต้องและต่อไขว้ TX → RX พร้อม GND ร่วม ใช้ logic level ที่เข้ากันได้ ไม่ต่อ RS-232 voltage เข้าขา MCU โดยตรง

**ขั้นตอน:** ตรวจ USART และ AF ใน datasheet → เริ่ม 115200 8N1 โดยตรวจ baud error จาก clock → ส่งข้อความคงที่ → echo → รับคำสั่ง LED ON/OFF → เพิ่ม receive แบบ interrupt พร้อม buffer จำกัดขนาด

**ตรวจผล:** ส่งคำสั่งถูก ผิด ยาวเกิน buffer และไม่มี newline ต้องไม่เขียนเกินขอบเขตหรือค้าง ระบุว่า timeout ทำงานจาก timebase ใด

**คำถาม:** ส่ง 100 byte แบบ 8N1 ที่ 115200 ใช้เวลาโดยประมาณเท่าไร? `100×10/115200 ≈ 8.68 ms` ไม่รวมช่องว่างระหว่าง byte

**อ่าน:** RM0401 บท USART; หนังสือบท 8

## ตั้งค่า STM32CubeMX

เลือก USART ที่ขา TX/RX ไม่ชนอุปกรณ์อื่น ตั้ง Asynchronous, 115200, 8 data bits, no parity, 1 stop bit, no flow control ตรวจ AF และ bus clock เปิด NVIC ของ USART เมื่อพัฒนา interrupt reception

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

RCC เปิด USART clock; GPIO AFR/MODER เลือก AF; USART BRR กำหนด baud; CR1 เปิด transmitter/receiver; SR/DR ใช้ status/data ตาม RM0401

ดู flag รับส่ง error และลำดับตรวจใน [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ลงมือทีละขั้น

1. เชื่อม TX/RX ไขว้และ GND ด้วย interface ที่เข้ากันได้ ปิด serial monitor อื่นก่อนเปิดพอร์ต
2. ส่ง greeting ครั้งเดียวและตรวจตัวอักษรใน terminal
3. ทำ receive ring buffer แบบมีขอบเขตใน ISR และ parse line ใน main; ห้าม parse/printf ยาวใน ISR
4. ใช้ LF จบ frame และเก็บ partial line; ถ้าเกิน 128 bytes ทิ้งจน LF
5. ทำ HELLO/PING/ACK/ERR ก่อน operation ของ Lab อื่นตาม protocol.md
6. ทดสอบสายหลุดและ UART error แล้วกำหนดวิธี reset/re-arm receive ที่ตรวจได้

## Pseudocode

ISR รับ byte เข้า ring buffer → main ประกอบ line → validate session/id/op/args → execute → enqueue ACK/ERR → TX เมื่อพร้อม

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* USER CODE BEGIN 2; replace huart2 with generated handle */
static const uint8_t greeting[] = "STM32 ready\n";
HAL_StatusTypeDef result = HAL_UART_Transmit(
    &huart2, (uint8_t *)greeting, sizeof greeting - 1U, 100U);
if (result != HAL_OK) { Error_Handler(); }
/* Greeting is a bring-up test, not a protocol ACK. */
```

## ทดสอบและเกณฑ์ผ่าน

- HELLO และ PING ได้ ACK ตรง session/id
- แบ่ง frame หลายส่วนและส่งหลาย frame พร้อมกันได้ผลเท่ากัน
- frame ยาว/เลขผิด/op ไม่รองรับไม่ล้น bufferและรับ frame ดีถัดไปได้

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

อักขระเพี้ยน: baud/clock; ไม่มีข้อมูล: TX-RX/GND/AF/port; รับครั้งเดียว: ไม่ re-arm interrupt; GUI เปิด port ไม่ได้: มีโปรแกรมอื่นครอบครอง

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab03_UART](../../../../Antigravity-Tkinter/labs/Lab03_UART/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

UART เป็น byte stream ไม่ได้แบ่งข้อความให้อัตโนมัติ ต้องออกแบบ framing, buffer, validation และ error recovery ก่อนเชื่อม GUI

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
