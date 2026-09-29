# สรุป Lab09_Encoder — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

แสดงตำแหน่งทิศทางและความเร็วที่มีเงื่อนไข calibration ชัดเจน

RPM ต้องมี calibration และเวลาอ้างอิง ไม่ใช่เพียงนำ counter ไปใส่กราฟ การ reconnect ทำให้ baseline เดิมใช้ไม่ได้

**Widgets/เครื่องมือ:** count label, direction indicator, counts/rev input, RPM label และ calibration status

**คำถามทบทวน:** encoder knob หมุนด้วยมือใช้แสดง RPM มอเตอร์ได้หรือไม่?

**แนวตอบ:** ไม่ได้ ถ้าไม่ได้วัดเพลามอเตอร์นั้น ต้องแยกเป็น input knob และ shaft feedback

## Checklist ก่อนจบ

- 100 counts ใน 500 ms ที่ 400 counts/rev ได้ 30 RPM
- delta_t=0 คืน unavailable
- session ใหม่ต้องรอ sample ที่สองก่อนคำนวณ

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
