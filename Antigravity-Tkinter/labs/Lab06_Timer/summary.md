# สรุป Lab06_Timer — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

ตั้ง period และเปรียบเทียบ timestamp MCU กับ callback UI

after จัดตาราง UI ไม่ได้แทน hardware timer การวิเคราะห์เวลาต้องรู้ว่า timestamp มาจากฝั่งใด

**Widgets/เครื่องมือ:** Spinbox 10–5000 ms, Apply, labels requested/confirmed, ตาราง timestamp

**คำถามทบทวน:** ถ้า UART รวม 10 timer updates เป็น telemetry เดียวควรคำนวณ period อย่างไร?

**แนวตอบ:** ใช้ delta MCU time และ delta update_count ที่สอดคล้องกัน ไม่ถือว่าช่องว่างระหว่าง frame คือ period หนึ่งรอบ

## Checklist ก่อนจบ

- 10/1000/5000 ส่งได้และ 0/5001 ไม่ส่ง
- old=0xFFFFFFF0,new=0x10 ได้ delta=32
- UI delay ไม่ถูกบันทึกเป็น timer error ฝั่ง MCU โดยอัตโนมัติ

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
