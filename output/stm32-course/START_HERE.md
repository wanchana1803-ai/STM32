# เริ่มเรียน STM32F410RB ด้วย STM32CubeMX

อ่าน [Roadmap](ROADMAP.md), เลือกบทจาก [สารบัญครบ 10 Lab](LAB_SUMMARIES.md) และใช้ [คู่มือ Register ครบ 10 Lab](REGISTER_GUIDE_ALL_LABS.md) ระหว่าง Debug คู่บท Python GUI อยู่ในโฟลเดอร์ Antigravity-Tkinter

## เตรียมข้อมูลครั้งเดียว

จด part number เต็ม, ชื่อบอร์ด, schematic, รุ่น debugger, IDE/toolchain และ CubeMX/STM32Cube firmware package version ผู้เรียนยืนยันแล้วเฉพาะ STM32F410RB และ CubeMX จึงยังไม่กำหนดหมายเลขขา LED/UART/อุปกรณ์อื่นแบบตายตัว

ตรวจ Flash 128 KB, SRAM 32 KB และ pinout package ที่ตรงกับชิปจาก DS11144 ที่ให้ไว้ ไฟล์ชื่อ stm32f410cb.pdf ครอบคลุมรุ่น RB ด้วย อย่าใช้ผัง CB 48 ขาแทน RB

## สร้างโปรเจกต์ฐาน

1. เปิด MCU Selector เลือก part number ให้ตรง ตรวจ package หากรู้ชื่อบอร์ดแน่ชัดจึงใช้ Board Selector
2. ตั้ง SYS Debug เป็น Serial Wire และสงวนขา debug ไว้
3. สำหรับบทเริ่มต้นตั้ง clock โดยใช้ HSI และตรวจ HCLK ที่แสดง ถ้าใช้ตัวอย่างคำนวณ 16 MHz ต้องยืนยัน HCLK/timer clock ที่เกี่ยวข้องจริง
4. ตั้ง pin/peripheral ตามบท อ่านคำอธิบายค่า ไม่เลือกขาที่ชนกับอุปกรณ์บนบอร์ด
5. Project Manager ตั้งชื่อและโฟลเดอร์ เช่น Lab01_LED เลือก Toolchain/IDE ตามเครื่องมือที่คุณติดตั้ง ไม่ถือว่ามี STM32CubeIDE อยู่แล้ว
6. เปิดตัวเลือกเก็บ user code เมื่อ regenerate ตามเวอร์ชันที่ใช้ Generate Code แล้วเปิดโปรเจกต์ใน IDE นั้น
7. Build โดยยังไม่เพิ่ม application code แล้ว flash/debug ให้หยุดที่ main ได้ บันทึกผล baseline
8. เพิ่ม snippet ใน USER CODE หรือไฟล์ application แยก ตัวแปรที่ต้องคงค่าข้าม loop ต้องประกาศก่อน while หรือเป็น static/global ตามขอบเขตที่เหมาะสม
9. Regenerate ทดลองหนึ่งครั้งและตรวจ diff ให้แน่ใจว่าโค้ดที่เขียนคงอยู่ ไม่มี init ชุดหลังเขียนทับค่าที่ตั้งเอง

## อ่าน snippets อย่างไร

ชื่อ `huart2`, `htim1`, `htim5`, `hadc1`, `hi2c1` เป็นตัวอย่างตาม peripheral ที่เลือก ต้องเปลี่ยนให้ตรง `.ioc` และ include header ที่ CubeMX สร้าง ชื่อ `LED_GPIO_Port/LED_Pin` และ `BUTTON_GPIO_Port/BUTTON_Pin` มาจาก User Label ที่ต้องตั้งก่อน

ตำแหน่ง USER CODE BEGIN 2 อยู่หลัง init ก่อน main loop ส่วน BEGIN 3 อยู่ใน main loop BEGIN PV ใช้ตัวแปรที่ต้องมี file scope และ BEGIN 4 ใช้ function/callback ให้ตรวจตำแหน่งจริงในเวอร์ชันที่ generate อย่าสร้าง callback ชื่อเดียวซ้ำ ถ้า project มีอยู่แล้วให้รวม logic

## ทำแต่ละ Lab แยกก่อนรวม

เริ่มด้วย `.ioc` แยกต่อ Lab เพื่อไม่ให้ TIM5 ของ Timer กับ Encoder ชนกัน เมื่อทำโปรเจกต์รวมต้องจัด resource allocation ใหม่:

| หน้าที่ | สิ่งที่ต้องเลือกและตรวจ |
|---|---|
| HAL timebase | SysTick หรือ timer ที่ตั้งจริง |
| LED / Button | GPIO และ polarity จากวงจร |
| UART GUI | USART instance + TX/RX AF + interface ถึง PC |
| PWM LED / Motor | channel/ขาแยกหรือปิดคำสั่ง PWM เมื่อใช้เป็น Motor |
| ADC | analog pin/channel/VREF |
| Encoder | timer CH1/CH2 คู่ที่รองรับและไม่ถูกใช้เป็น timebase |
| OLED | I2C instance/ขา/pull-up/controller/address |

## เชื่อม GUI หลัง Lab03

ใช้ [protocol.md](../../Antigravity-Tkinter/protocol.md) เป็นข้อตกลงที่พัฒนาเพิ่ม ตัวอย่าง HAL snippets ยังไม่มี parser ครบ ต้องทำ HELLO/PING/ACK/ERR และ operation ของแต่ละ Lab ตามใบงาน UART ก่อน

BUTTON ใน protocol ใช้ `state=1` หมายถึงกดและ `state=0` หมายถึงปล่อย ถ้าวงจร active-low ให้แปลงจาก `GPIO_PIN_RESET` เป็น pressed=1 หลัง debounce ไม่ส่งระดับ IDR โดยถือว่าความหมายตรงกัน

Timer polling/ADC polling ใช้เป็นบทเริ่มต้นเท่านั้น เมื่อรวม Motor ต้องตรวจเวลาเลวร้ายที่สุดของทุก task, UART TX, OLED transfer และ timeout ให้ main ตรวจ STOP/watchdog ได้ตามกำหนด ใช้ queue/interrupt/DMA เมื่อผลวัดแสดงว่าจำเป็น

## ส่งงานและสรุป

ทุกโฟลเดอร์ Lab มี summary.md ที่สรุปความรู้ไว้แล้ว ให้กรอกข้อมูลทดลองจริงหลังเรียน: วันที่ บอร์ด/เครื่องมือ ค่าที่ตั้ง ผลที่คาด/วัดได้ ปัญหา วิธีแก้ และคำถามที่ยังไม่เข้าใจ อัปเดต progress.md แยกการตรวจโค้ด, build, mock และ hardware ตามหลักฐาน
