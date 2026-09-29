# สัญญาการสื่อสารสำหรับบทเรียน รุ่น 1

นี่คือ protocol ที่ออกแบบเพิ่มสำหรับหลักสูตร ไม่ใช่ความสามารถที่มีอยู่แล้วใน STM32 หรือไฟล์ต้นฉบับ ต้องสร้าง firmware parser และ mock transport ตามข้อตกลงเดียวกันก่อนเชื่อม GUI จริง

## การส่งข้อความ

UART 115200, 8 data bits, no parity, 1 stop bit, no flow control ตามการต่อสายที่ยืนยัน PC ใช้ Serial port ที่เลือก ไม่สมมติว่าชิปมี USB CDC ใช้งานอยู่ อาจใช้ ST-LINK VCP หรือ USB-UART ระดับลอจิกที่เข้ากันได้ตามบอร์ดจริง

UTF-8 แต่คำสั่ง/ค่าของรุ่นแรกจำกัด ASCII เท่านั้น แต่ละ frame จบ LF (`\n`) รับ CRLF ได้โดยตัด CR ที่ท้าย ความยาวสูงสุด 128 bytes รวม LF เกินแล้วทิ้งจน LF ถัดไป ห้ามตีความเศษข้อความเป็นคำสั่งใหม่ read timeout ไม่ได้แปลว่าจบ frame ต้องเก็บ partial bytes ต่อ

รูปแบบตัวเลขเป็นเลขฐานสิบจำนวนเต็ม session เป็นตัวอักษร hex 8 ตัวที่ GUI สุ่มใหม่ทุกครั้งที่เชื่อม id เป็นจำนวน 1–2147483647 เพิ่มทุกคำสั่ง ไม่ใช้ซ้ำใน session

```text
CMD,a1b2c3d4,1,HELLO
ACK,a1b2c3d4,1,HELLO,1
CMD,a1b2c3d4,2,LED,1
ACK,a1b2c3d4,2,LED,1
CMD,a1b2c3d4,3,PWM,101
ERR,a1b2c3d4,3,RANGE
EVT,a1b2c3d4,1,1234,BUTTON,1,1
```

HELLO ตั้ง session ใหม่และทำให้ motor DISARMED ยกเลิก pending/queued controls เก่าทั้งสองฝั่ง GUI รอ ACK HELLO ก่อนเปิดปุ่มควบคุม ACK ยืนยันคำสั่งถูกตรวจและนำไปใช้กับ state/output แล้ว ไม่รับประกันว่าค่าทางกายภาพเกิดขึ้น เช่น ACK LED ไม่พิสูจน์ว่า LED ต่อถูก

GUI มี command in flight ได้หนึ่งรายการเพื่อสอนให้ง่าย รอ ACK/ERR สูงสุด 1 s ตามค่าตั้งต้น ถ้าหมดเวลาให้สถานะ UNKNOWN/TIMEOUT ไม่ retry control อัตโนมัติ STOP เป็นข้อยกเว้นที่แซงคิวและส่งได้แม้มี pending; ACK ทุกตัวต้อง match session/id/op ก่อนอัปเดต state

## คำสั่งและผลตอบ

| Lab | CMD operation และ args | ACK operation และ values |
|---|---|---|
| 01 | LED,0 หรือ LED,1 | LED,ค่าที่ใช้ |
| 02 | BUTTON_GET | BUTTON_GET,stable_state,press_count |
| 03 | PING | PING,1 |
| 04 | PWM,percent ช่วง 0–100 | PWM,percent ที่ใช้ |
| 05 | ADC_GET | ADC_GET,raw,millivolts |
| 06 | PERIOD,ms ช่วง 10–5000 | PERIOD,ms ที่ใช้ |
| 07 | EVENT_GET | EVENT_GET,irq_count |
| 08 | OLED,text ASCII 1–20 ตัวอักษร ไม่มี comma/CR/LF | OLED,OK |
| 09 | ENCODER_GET | ENCODER_GET,signed_count |
| 10 | MOTOR_ARM; MOTOR,percent ช่วง 0–100; MOTOR_STOP | MOTOR_ARM,0; MOTOR,requested_percent; MOTOR_STOP,0 |

ทุก Lab ที่รองรับคำสั่งใช้ HELLO/PING ได้ firmware ที่ยังไม่ทำ operation ตอบ ERR ด้วย UNSUPPORTED ไม่ ACK สำเร็จทิ้ง ๆ ERR code อื่น: FORMAT, RANGE, SESSION, BUSY, HW, DISARMED

`PWM` ควบคุมช่องทดลอง LED เท่านั้น ห้ามใช้เป็นทางลัดขับมอเตอร์โดยข้าม ARM/watchdog การรวมระบบต้องจัดสรร peripheral แยก หรือปิด operation PWM เมื่อช่องนั้นถูกใช้ขับมอเตอร์

## Event telemetry

`EVT,session,seq,ms,topic,values...` โดย seq เพิ่มต่อ frame (uint32 wrap) และ ms เป็น HAL tick ฝั่ง MCU (uint32 wrap) เริ่ม seq ใหม่เมื่อ HELLO Topic และ values:

| Topic | values | ความหมาย |
|---|---|---|
| BUTTON | state,count | stable state 0/1 และจำนวนกดหลัง debounce |
| ADC | raw,millivolts | raw 0–4095 และค่าจาก VREF ที่ firmware ใช้ |
| TIMER | update_count | จำนวน update สะสม |
| IRQ | irq_count | จำนวน interrupt สะสม ไม่ใช่หนึ่ง frame ต่อ interrupt เสมอ |
| ENCODER | signed_count | ตำแหน่งสะสมที่ firmware แก้ wrap ของ timer แล้ว |
| MOTOR | applied_percent,armed,fault | duty หลัง ramp, armed 0/1, fault 0/1 |

เริ่มส่ง telemetry ไม่เกิน 10 Hz และลดอัตราถ้า TX ใกล้เต็ม ปุ่มอาจส่งทันทีหลัง stable แต่ยังต้องมีขอบเขต GUI แสดง data stale เมื่อไม่มีข้อมูล topic นานกว่า 2 s (ค่าตั้งต้นสำหรับ stream 10 Hz) seq ที่กระโดดใช้แสดง dropped frames ไม่สร้างข้อมูลชดเชยขึ้นเอง

## Motor watchdog

MOTOR_ARM ตั้ง target/applied=0 ก่อนเปิดการรับคำสั่ง MOTOR ต้อง ARM ใหม่หลัง boot/reconnect/STOP/fault GUI ส่ง PING ทุก 200 ms เมื่อ ARMED; firmware ต้องหยุดและ DISARM ถ้าไม่รับ PING ที่ session ถูกต้องนาน 1000 ms ระยะเหล่านี้เป็นค่าทดลอง ต้องตรวจความเหมาะสมกับระบบจริง

MOTOR_STOP ยกเลิก ramp และตั้ง output ตาม stop state ของ driver ทันทีใน application loop ที่ไม่บล็อกไม่จำกัด จากนั้นตอบ ACK ไม่มีการเปลี่ยนทิศทางใน protocol รุ่นแรก GUI ปุ่ม STOP ไม่แทนปุ่มหยุดฮาร์ดแวร์

## กรณี parser ที่ต้องทดสอบ

รับ frame แบ่งหลาย read; หลาย frame ใน read เดียว; CRLF; byte ที่ไม่ใช่ ASCII; frame เกิน 128; id ไม่ใช่เลข; argument เกินช่วง; operation ไม่รองรับ; ACK จาก session เก่า; reconnect แล้วมี telemetry เก่าค้าง ต้องฟื้นกลับมารับ frame ถูกต้องถัดไปได้
