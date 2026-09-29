# Lab08_I2C_OLED: I2C และ OLED

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** เข้าใจ ACK และแยกปัญหา bus ออกจากคำสั่งควบคุมจอ

I2C ใช้ SCL/SDA แบบ open-drain พร้อม pull-up ตามแรงดันและโหลดที่เหมาะสม MCU ส่ง address แล้วตรวจ ACK ส่วนการวาดตัวอักษรต้องใช้ protocol ของ controller จออีกชั้นหนึ่ง ไฟล์ที่ให้มายังไม่ระบุ OLED controller หรือขนาดจอ จึงยังไม่กำหนด driver เฉพาะรุ่น

**ขั้นตอน:** ยืนยันรุ่นจอและแรงดัน → ตรวจ pull-up บนโมดูล → เลือก I2C instance/AF → ทดลอง transaction พร้อม timeout → ยืนยัน address แบบ 7 บิต → init ตาม datasheet จอ → แสดงข้อความ → แสดงค่า ADC

**ตรวจผล:** address ผิดต้องจบด้วย error/timeout ไม่ค้าง ถอดจอแล้วงานอื่นต้องเดินต่อ อธิบายว่าฟังก์ชันที่ใช้รับ address แบบ 7 บิตหรือแบบเลื่อนซ้าย ห้ามนำค่าของสองรูปแบบปนกัน

**คำถาม:** เห็น ACK แล้วจอว่างหมายความว่าอย่างไร? bus อาจสื่อสารได้ แต่ยังต้องตรวจ init, controller, framebuffer และคำสั่งส่งข้อมูล

**อ่าน:** RM0401 บท I2C ของ instance ที่ใช้ ซึ่งต้องแยกจาก FMPI2C; หนังสือบท 14; เพิ่ม datasheet จอเมื่อทราบรุ่น

## ตั้งค่า STM32CubeMX

ยืนยัน OLED controller, ขนาด, address และแรงดันก่อน เลือก I2C instance ที่ใช้งานได้พร้อม SCL/SDA AF open-drain ตรวจ pull-up จริง เริ่ม Standard mode 100 kHz และ timing ตาม clock อย่านำ register ของ FMPI2C ปนกับ I2C ปกติ

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

GPIO AF/open-drain; I2C CR/SR/DR และ timing ของ instance; controller OLED มีคำสั่งอีกชุดแยกจาก peripheral MCU

ดูลำดับ START/address/data/STOP และ error flags ใน [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ลงมือทีละขั้น

1. บันทึกรุ่นจอ/controller/address จากเอกสารหรือการตรวจที่มีหลักฐาน
2. probe address แบบจำกัดเวลา ตรวจว่า API รับ address shifted
3. เลือก driver ที่ตรง controller และทดสอบข้อความคงที่
4. แยก draw buffer กับ transfer ไม่ส่งทั้งจอทุก main loop
5. รับ OLED,text จาก UART validate ASCII/ความยาวและ ACK หลัง driver คืนสำเร็จ ถ้า NACK ให้ ERR HW

## Pseudocode

validate text → update display buffer → transfer with timeout → ACK OK หรือ ERR HW; งานอื่นต้องเดินต่อเมื่อจอไม่ตอบ

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* Helper after hi2c1 initialization. Call only with a verified address. */
HAL_StatusTypeDef oled_probe(uint8_t address7)
{
    if (address7 < 0x08U || address7 > 0x77U) { return HAL_ERROR; }
    return HAL_I2C_IsDeviceReady(&hi2c1,
        (uint16_t)address7 << 1U, 2U, 20U);
}
/* Display initialization/drawing must come from the actual controller driver. */
```

## ทดสอบและเกณฑ์ผ่าน

- probe ACK กับ address ที่ถูกและ NACK กับ address ผิด
- ส่งข้อความ 1 และ 20 ตัวอักษรได้โดยไม่ล้น
- จอไม่อยู่แล้ว main/UART ยังทำงานและรายงาน error

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

ACK แต่จอมืด: init/controller/contrast; bus busy: pull-up/wiring; อักษรผิด: framebuffer/font/offset

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab08_I2C_OLED](../../../../Antigravity-Tkinter/labs/Lab08_I2C_OLED/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

I2C ACK ยืนยันการสื่อสารระดับ bus ไม่ยืนยันว่าจอวาดถูก ต้องตรวจทั้ง transport และ controller driver

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
