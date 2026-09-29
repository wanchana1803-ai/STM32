# สรุป Lab05_ADC — STM32

## ความรู้ที่ต้องจำ

ADC ให้ค่าดิจิทัลเทียบ reference การแปลงเป็นโวลต์ต้องรู้ VREF และความคลาดเคลื่อน การเฉลี่ยไม่แก้ calibration ผิด

**CubeMX:** เลือก ADC1 channel ที่ตรง analog pin ตั้ง 12-bit, right alignment, single conversion, software trigger และ sampling time เหมาะกับ source impedance ตรวจ ADC clock limit ใน datasheet ตั้ง GPIO analog/no pull

**รีจิสเตอร์สำคัญ:** ADC CR1/CR2 เลือก mode/start; SMPR เลือก sampling time; SQR เลือกลำดับ channel; SR/DR แสดงสถานะ/ผล

**จุดผิดพลาดที่ต้องแยกให้ออก:** ค่านิ่ง 0: channel/pin/ground; noise: source/VREF/sample time; สเกลผิด: resolution/VREF

## ก่อนถือว่าจบ Lab

- raw อยู่ 0–4095; ค่ากลางประมาณครึ่ง full scale
- timeout ไม่รายงาน raw=0 ว่าเป็นค่าที่วัดสำเร็จ
- disconnect sensor แล้วไม่อ้างค่าที่ลอยเป็นแรงดันเชื่อถือได้

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
