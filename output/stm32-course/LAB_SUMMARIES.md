# สรุปครบ 10 Lab — STM32F410RB + STM32CubeMX

นี่คือสรุปความรู้และเกณฑ์ตรวจ ไม่ใช่ผลทดลองจริง

| Lab | เนื้อหา | สรุปและบันทึกผล |
|---|---|---|
| Lab01_LED | [บทเรียน](labs/Lab01_LED/lesson.md) | [สรุป](labs/Lab01_LED/summary.md) |
| Lab02_Button | [บทเรียน](labs/Lab02_Button/lesson.md) | [สรุป](labs/Lab02_Button/summary.md) |
| Lab03_UART | [บทเรียน](labs/Lab03_UART/lesson.md) | [สรุป](labs/Lab03_UART/summary.md) |
| Lab04_PWM | [บทเรียน](labs/Lab04_PWM/lesson.md) | [สรุป](labs/Lab04_PWM/summary.md) |
| Lab05_ADC | [บทเรียน](labs/Lab05_ADC/lesson.md) | [สรุป](labs/Lab05_ADC/summary.md) |
| Lab06_Timer | [บทเรียน](labs/Lab06_Timer/lesson.md) | [สรุป](labs/Lab06_Timer/summary.md) |
| Lab07_Interrupt | [บทเรียน](labs/Lab07_Interrupt/lesson.md) | [สรุป](labs/Lab07_Interrupt/summary.md) |
| Lab08_I2C_OLED | [บทเรียน](labs/Lab08_I2C_OLED/lesson.md) | [สรุป](labs/Lab08_I2C_OLED/summary.md) |
| Lab09_Encoder | [บทเรียน](labs/Lab09_Encoder/lesson.md) | [สรุป](labs/Lab09_Encoder/summary.md) |
| Lab10_PWM_Motor | [บทเรียน](labs/Lab10_PWM_Motor/lesson.md) | [สรุป](labs/Lab10_PWM_Motor/summary.md) |

## Lab01_LED

GPIO กำหนดระดับขา ส่วน timebase กำหนดเวลา การใช้ elapsed time ทำให้ main ทำงานอื่นได้ BSRR ใช้ set/reset เฉพาะบิต ส่วน toggle ต้องระวังผู้เขียนขาร่วมกัน

หลักฐานที่ต้องส่ง: เริ่มต้นขาตรงกับ initial level ที่ตั้งและ LED ไม่กลับ polarity ผิด; 100/500/1000 ms ให้คาบประมาณ 200/1000/2000 ms โดยระบุเครื่องมือและความคลาดเคลื่อน; เพิ่มการอ่านปุ่มหรือ counter ใน main แล้วไม่ติดค้างจาก delay

## Lab02_Button

ปุ่มให้ระดับสัญญาณ แต่โปรแกรมต้องสร้างเหตุการณ์จากขอบ Debounce ลดผลหน้าสัมผัสเด้ง โดยแลกกับเวลาในการตอบสนอง

หลักฐานที่ต้องส่ง: กด 20 ครั้งต้องเพิ่ม 20 ไม่เพิ่มซ้ำตอนค้าง; เปิดเครื่องพร้อมกดค้าง: ไม่ถือเป็นขอบกดใหม่ในตัวอย่างนี้จนปล่อยและกดอีกครั้ง; ทดลองกดเร็วกว่า debounce แล้วอธิบายเหตุการณ์ที่ถูกกรอง

## Lab03_UART

UART เป็น byte stream ไม่ได้แบ่งข้อความให้อัตโนมัติ ต้องออกแบบ framing, buffer, validation และ error recovery ก่อนเชื่อม GUI

หลักฐานที่ต้องส่ง: HELLO และ PING ได้ ACK ตรง session/id; แบ่ง frame หลายส่วนและส่งหลาย frame พร้อมกันได้ผลเท่ากัน; frame ยาว/เลขผิด/op ไม่รองรับไม่ล้น bufferและรับ frame ดีถัดไปได้

## Lab04_PWM

PWM แยกความถี่ออกจาก duty ค่า compare มีความหมายตาม counting mode และ polarity จึงต้องวัดที่ขาจริง

หลักฐานที่ต้องส่ง: 10/50/90% คงความถี่ 1 kHz ตาม clock สมมติ; ค่า -1/101 ถูกปฏิเสธ ไม่ wrap; 0/100% ให้ระดับปลายช่วงถูกต้องและ CCR อยู่ในช่วง register

## Lab05_ADC

ADC ให้ค่าดิจิทัลเทียบ reference การแปลงเป็นโวลต์ต้องรู้ VREF และความคลาดเคลื่อน การเฉลี่ยไม่แก้ calibration ผิด

หลักฐานที่ต้องส่ง: raw อยู่ 0–4095; ค่ากลางประมาณครึ่ง full scale; timeout ไม่รายงาน raw=0 ว่าเป็นค่าที่วัดสำเร็จ; disconnect sensor แล้วไม่อ้างค่าที่ลอยเป็นแรงดันเชื่อถือได้

## Lab06_Timer

Timer ทำงานจาก hardware clock ส่วน main มาสังเกต flag การสังเกตช้าไม่ทำให้ได้จำนวนเหตุการณ์ครบเสมอ

หลักฐานที่ต้องส่ง: CNT เดินและ wrap ที่ ARR; คาบตรงกับสูตรภายใต้ clock ที่วัด/ยืนยัน; อธิบายได้ว่าการ polling ช้าอาจรวมหลาย update เป็นหนึ่ง

## Lab07_Interrupt

Interrupt แยกการรับเหตุการณ์จากงานหลัก ISR ที่สั้นช่วยจำกัด latency แต่ข้อมูลร่วมยังต้องออกแบบ ownership

หลักฐานที่ต้องส่ง: เพิ่มจำนวน IRQ ได้แม้ main มีงานอื่นระยะสั้น; ไม่เกิด IRQ loop จาก pending ที่ไม่เคลียร์; counter wrap หรือ snapshot race มีวิธีจัดการที่อธิบายได้

## Lab08_I2C_OLED

I2C ACK ยืนยันการสื่อสารระดับ bus ไม่ยืนยันว่าจอวาดถูก ต้องตรวจทั้ง transport และ controller driver

หลักฐานที่ต้องส่ง: probe ACK กับ address ที่ถูกและ NACK กับ address ผิด; ส่งข้อความ 1 และ 20 ตัวอักษรได้โดยไม่ล้น; จอไม่อยู่แล้ว main/UART ยังทำงานและรายงาน error

## Lab09_Encoder

Count เป็นตำแหน่งเชิงดิจิทัล การคำนวณความเร็วต้องรู้เวลา ระยะต่อ count และแก้ counter wrap

หลักฐานที่ต้องส่ง: หนึ่งรอบได้ counts/rev ที่อธิบายได้ทั้งสองทิศ; ข้าม wrap แล้วยังได้ delta ถูก; สาย A/B หลวมไม่ถูกแสดงว่าเป็น RPM เชื่อถือได้

## Lab10_PWM_Motor

การควบคุมมอเตอร์ต้องมี output state ที่แน่นอนและทางหยุดใน firmware GUI เป็นผู้ขอคำสั่ง ไม่ควรเป็นชั้นเดียวที่ดูแล link loss

หลักฐานที่ต้องส่ง: boot/reset/reconnect ไม่หมุนเองและต้อง ARM ใหม่; หยุด PING เกิน watchdog แล้ว firmware หยุดแม้ GUI ค้าง; STOP ยกเลิก ramp ไม่รอให้ duty ลดช้า ๆ; OLED/UART error ไม่ทำให้ main หยุดตรวจ watchdog
