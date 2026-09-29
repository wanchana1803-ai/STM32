# Roadmap Python GUI ด้วย Tkinter: 10 Lab คู่กับ STM32F410RB

เป้าหมาย: สร้างเครื่องมือควบคุมและติดตามผล STM32 ที่หน้าต่างไม่ค้าง มี mock mode รับข้อมูล Serial ได้ถูกต้อง และอธิบายการทำงานได้

แผนเสนอ 12 สัปดาห์ สัปดาห์ละ 4 ชั่วโมง รวม 48 ชั่วโมง เป็นเวลาเพิ่มจากหลักสูตร MCU 72 ชั่วโมง ถ้าเรียนสองส่วนขนานตามแผนเดิมจะประมาณ 10 ชั่วโมงต่อสัปดาห์ ปรับความเร็วตามพื้นฐานจริง

## ลำดับและผลงาน

| สัปดาห์ | หัวข้อ | ผลงาน |
|---|---|---|
| 1 | Python function/list/dict/class/exception, venv, Tk/ttk | หน้าต่างและ callback แรก |
| 2 | Lab01 LED | ปุ่ม ON/OFF และสถานะ confirmed/pending ใน mock |
| 3 | Lab02 Button | แสดง event และตัวนับจาก mock |
| 4 | Lab03 UART | เลือก COM, Connect/Disconnect, parser และ terminal |
| 5 | Lab06 Timer | ตั้ง period และแยกเวลา GUI/MCU |
| 6 | Lab07 Interrupt | event log แบบ queue มีขอบเขต |
| 7 | Lab04 PWM | slider duty พร้อม debounce และ ACK |
| 8 | Lab05 ADC | raw/แรงดัน กราฟ Canvas และ export |
| 9 | Lab08 I2C OLED | ส่งข้อความพร้อม validation และ NACK handling |
| 10 | Lab09 Encoder | count/direction และ RPM เมื่อมีข้อมูลเพลาจริง |
| 11 | Lab10 PWM Motor | state machine, STOP, mock link loss |
| 12 | รวมแอปและทดสอบ | Notebook dashboard, log และรายงานครบ |

เลข Lab คงตามภาพต้นฉบับ ลำดับเรียนเปลี่ยนเพื่อให้ Lab03 สร้าง transport ก่อนใช้จริงกับบทอื่น Lab01–02 เรียน mock ก่อน และกลับมาทดสอบกับบอร์ดหลัง firmware UART รองรับ protocol แล้ว

## วิธีเรียนหนึ่ง Lab (4 ชั่วโมง)

ทฤษฎีและอ่านเอกสาร 40 นาที → ออกแบบหน้าจอ/state 30 นาที → เขียนและลอง mock 90 นาที → ทดลองขอบเขต/Serial ตามความพร้อม 50 นาที → สรุป 30 นาที

แต่ละ `labs/LabNN_*/lesson.md` มีเป้าหมาย widgets ขั้นตอน ตัวอย่างแกนหลักและกรณีทดสอบ ส่วน `summary.md` สรุปความรู้และเว้นผลจริงไว้ให้กรอก

## สถาปัตยกรรมที่ค่อย ๆ สร้าง

Tkinter view → application state → command queue → transport worker → STM32 UART

STM32 UART → bounded receive buffer → parser → event queue → root.after() → application state/view

Mock transport ใช้สัญญาเดียวกัน แทนเฉพาะ I/O ไม่ใช้ random response มายืนยันคำสั่งที่ไม่ได้ประมวลผลจริง

## เกณฑ์จบหลักสูตร

- สลับ mock/serial โดย view ไม่ต้องรู้รายละเอียดพอร์ต
- แต่ละ Lab ผ่านกรณีปกติ กรณีข้อมูลผิด และ disconnect ตามใบงาน
- ไม่มี serial I/O แบบรอไม่จำกัดใน UI thread และปิดหน้าต่างแล้วพอร์ตถูกคืน
- แสดงสถานะ link และข้อมูล stale แยกจากค่าล่าสุด
- Lab10 เริ่ม DISARMED และไม่กลับไปหมุนอัตโนมัติหลัง reconnect
- สรุปครบ 10 Lab พร้อมแยกผลจำลองจากผลฮาร์ดแวร์; งานที่ยังไม่มีบอร์ดให้ระบุไม่ทดสอบ

แหล่งทางการ: [Python Tkinter](https://docs.python.org/3/library/tkinter.html), [ttk](https://docs.python.org/3/library/tkinter.ttk.html), [pySerial](https://pyserial.readthedocs.io/en/stable/shortintro.html) เอกสาร Tkinter อธิบาย event loop/threading; หลักสูตรนี้เลือกให้ main thread เป็นเจ้าของ UI และแยก I/O เพื่อให้ตรวจพฤติกรรมได้ง่าย
