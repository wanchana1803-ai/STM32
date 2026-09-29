# สรุปครบ 10 Lab — Python Tkinter + Serial

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

Tkinter callback สร้างคำสั่ง ส่วน ACK ยืนยัน state การเปลี่ยนสีปุ่มอย่างเดียวไม่พิสูจน์ว่า LED บนบอร์ดติด

หลักฐานที่ต้องส่ง: กด ON ได้ pending ก่อน confirmed ON; mock ไม่ตอบต้องขึ้น timeout ไม่ขึ้นสำเร็จ; ACK id เก่าไม่เปลี่ยนสถานะคำสั่งปัจจุบัน

## Lab02_Button

GUI ใช้ stable state และ counter จาก firmware แยกเวลาได้รับข้อมูลจากเวลาเกิดเหตุการณ์ การแสดงซ้ำไม่ใช่การกดใหม่

หลักฐานที่ต้องส่ง: ส่ง event เดิมซ้ำแล้ว count ไม่เพิ่มเอง; กดค้างแสดง state ค้างแต่ไม่เพิ่ม count; หยุด telemetry แล้วแสดง stale

## Lab03_UART

แยก transport/parser/UI และใช้ queue เป็นขอบเขต thread timeout ช่วยให้ shutdown ได้ แต่ไม่ใช่ตัวจบ frame

หลักฐานที่ต้องส่ง: partial/multiple/oversized frames กู้คืนได้; พอร์ตไม่อยู่/ถูกใช้แสดง error และ UI ยังปิดได้; connect-disconnect 10 ครั้งไม่มี worker หรือพอร์ตค้าง

## Lab04_PWM

Slider เป็นแหล่งคำขอ ไม่ใช่ผลวัด ต้องจำกัดอัตราส่งและแสดงค่าที่ firmware ยืนยันแยกกัน

หลักฐานที่ต้องส่ง: ลากเร็วแล้ว queue ไม่โตไม่จำกัด; กรอกข้อความ/101 แล้วไม่ส่ง; ACK ช้าทำให้ requested ต่าง applied ได้โดย UI ไม่หลอก

## Lab05_ADC

การเก็บ sample และวาดจอมีอัตราต่างกันได้ ต้องจำกัดหน่วยความจำและบันทึกหน่วย/ที่มาของข้อมูล

หลักฐานที่ต้องส่ง: raw=0/2048/4095 แสดงถูก ไม่หารด้วยศูนย์ตอนกราฟมี sample เดียว; รับ 10000 samples แล้ว history ไม่เกิน 600; export เปิดอ่านกลับแล้วจำนวนแถว/หน่วยตรง

## Lab06_Timer

after จัดตาราง UI ไม่ได้แทน hardware timer การวิเคราะห์เวลาต้องรู้ว่า timestamp มาจากฝั่งใด

หลักฐานที่ต้องส่ง: 10/1000/5000 ส่งได้และ 0/5001 ไม่ส่ง; old=0xFFFFFFF0,new=0x10 ได้ delta=32; UI delay ไม่ถูกบันทึกเป็น timer error ฝั่ง MCU โดยอัตโนมัติ

## Lab07_Interrupt

จำนวน interrupt จำนวน telemetry frame และจำนวนแถวบนจอเป็นคนละสิ่ง ต้องแยก counters และจำกัดคิว

หลักฐานที่ต้องส่ง: burst แล้วปุ่ม/ปิดหน้าต่างยังตอบสนอง; Clear View ไม่ทำให้ MCU counter เป็นศูนย์; frame drop แสดงตัวนับและค่าล่าสุดได้

## Lab08_I2C_OLED

Validate ให้ตรงกับความสามารถ firmware/font การมี preview ไม่แทนการตรวจจอจริงและ ACK ไม่รับรองคุณภาพภาพ

หลักฐานที่ต้องส่ง: ข้อความปกติส่งได้; ภาษาไทย/comma/newline ถูกปฏิเสธตามรุ่น protocol; ERR HW แสดง error ไม่แสดง success; preview ไม่ถูกนำไปอ้างว่าฮาร์ดแวร์แสดงแล้ว

## Lab09_Encoder

RPM ต้องมี calibration และเวลาอ้างอิง ไม่ใช่เพียงนำ counter ไปใส่กราฟ การ reconnect ทำให้ baseline เดิมใช้ไม่ได้

หลักฐานที่ต้องส่ง: 100 counts ใน 500 ms ที่ 400 counts/rev ได้ 30 RPM; delta_t=0 คืน unavailable; session ใหม่ต้องรอ sample ที่สองก่อนคำนวณ

## Lab10_PWM_Motor

State ที่ GUI แสดงต้องตรงกับหลักฐาน การสูญเสีย link ทำให้ผลทางกายภาพไม่ทราบ และ firmware ต้องหยุดเองตาม watchdog

หลักฐานที่ต้องส่ง: เปิด GUI/reconnect แล้วไม่มี MOTOR command อัตโนมัติ; slider backlog ไม่ขวาง STOP; ปิดโปรแกรมหรือ mock link loss แล้วไม่แสดง false stopped; บนบอร์ดจริงพิสูจน์ watchdog ด้วยการหยุด heartbeatและวัด output
