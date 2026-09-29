# สรุป Lab07_Interrupt — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

แสดง interrupt counters และ event stream โดยไม่ redraw จน UI ค้าง

จำนวน interrupt จำนวน telemetry frame และจำนวนแถวบนจอเป็นคนละสิ่ง ต้องแยก counters และจำกัดคิว

**Widgets/เครื่องมือ:** Treeview event log, counter, dropped-frame label, Clear View

**คำถามทบทวน:** ถ้า irq_count เพิ่ม 100 แต่ GUI รับ 10 frame แปลว่าหาย 90 interrupt หรือไม่?

**แนวตอบ:** ไม่จำเป็น firmware อาจรายงาน counter แบบ batch ต้องดู protocol/seq และความถี่ publish

## Checklist ก่อนจบ

- burst แล้วปุ่ม/ปิดหน้าต่างยังตอบสนอง
- Clear View ไม่ทำให้ MCU counter เป็นศูนย์
- frame drop แสดงตัวนับและค่าล่าสุดได้

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
