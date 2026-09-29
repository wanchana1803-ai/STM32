# Lab05_ADC: ADC วัดแรงดัน

## เป้าหมายและพื้นฐาน

**เป้าหมาย:** เปลี่ยนค่าดิจิทัลเป็นค่าประมาณแรงดันพร้อมอธิบายความคลาดเคลื่อน

ADC 12 บิตให้ raw 0–4095 การประมาณแรงดันทั่วไปคือ `V≈raw×VREF/4095` ต้องใช้ VREF ที่ทราบหรือวัดได้ Sampling time และความต้านทานของแหล่งสัญญาณมีผลต่อการอ่าน

**ขั้นตอน:** เลือกขา ADC/channel ที่มีจริง → ตั้ง analog mode → ตรวจ ADC clock และ sampling time → อ่าน single conversion → ส่ง raw ทาง UART → แปลงแรงดัน → ลองเฉลี่ย 16 ตัวอย่าง

**ตรวจผล:** ทดลองแรงดันใกล้ GND กลางช่วง และใกล้ VREF ภายในช่วงอินพุตที่อนุญาต เทียบมัลติมิเตอร์ บันทึก min/max ก่อนและหลังเฉลี่ย การเฉลี่ยลด noise บางชนิดแต่ไม่แก้ VREF ผิด

**คำถาม:** raw=2048 และ VREF=3.3 V ได้เท่าไร? ประมาณ 1.6504 V

**อ่าน:** RM0401 บท 11; หนังสือบท 12; Datasheet electrical/ADC characteristics

## ตั้งค่า STM32CubeMX

เลือก ADC1 channel ที่ตรง analog pin ตั้ง 12-bit, right alignment, single conversion, software trigger และ sampling time เหมาะกับ source impedance ตรวจ ADC clock limit ใน datasheet ตั้ง GPIO analog/no pull

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

ADC CR1/CR2 เลือก mode/start; SMPR เลือก sampling time; SQR เลือกลำดับ channel; SR/DR แสดงสถานะ/ผล

## ลงมือทีละขั้น

1. วัด VREF/ไฟ analog และตรวจขอบเขตแรงดันก่อนต่อ potentiometer
2. อ่าน raw ครั้งเดียวให้ผ่านก่อนเพิ่ม periodic sampling
3. ส่ง raw/millivolts ไม่เกิน 10 Hz เพื่อเริ่มเชื่อม GUI
4. เปรียบเทียบจุดต่ำ กลาง สูงกับมัลติมิเตอร์
5. เพิ่ม moving average และเปรียบเทียบ noise กับ response lag

## Pseudocode

ครบ sample interval → start ADC → รอแบบมี timeout → ถ้าสำเร็จแปลงหน่วย → publish; ถ้าผิดส่ง error ไม่ใช้ raw เก่าเป็นผลใหม่

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```c
/* In main/task context after ADC initialization; not ISR */
uint32_t raw = 0;
HAL_StatusTypeDef status = HAL_ADC_Start(&hadc1);
if (status == HAL_OK) {
    status = HAL_ADC_PollForConversion(&hadc1, 10U);
    if (status == HAL_OK) { raw = HAL_ADC_GetValue(&hadc1); }
    HAL_ADC_Stop(&hadc1);
}
/* Use raw only when status == HAL_OK.
   millivolts = raw * measured_vref_mV / 4095U; */
```

## ทดสอบและเกณฑ์ผ่าน

- raw อยู่ 0–4095; ค่ากลางประมาณครึ่ง full scale
- timeout ไม่รายงาน raw=0 ว่าเป็นค่าที่วัดสำเร็จ
- disconnect sensor แล้วไม่อ้างค่าที่ลอยเป็นแรงดันเชื่อถือได้

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

ค่านิ่ง 0: channel/pin/ground; noise: source/VREF/sample time; สเกลผิด: resolution/VREF

## ต่อกับ Python GUI

คู่บทคือ [Tkinter Lab05_ADC](../../../../Antigravity-Tkinter/labs/Lab05_ADC/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

ADC ให้ค่าดิจิทัลเทียบ reference การแปลงเป็นโวลต์ต้องรู้ VREF และความคลาดเคลื่อน การเฉลี่ยไม่แก้ calibration ผิด

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
