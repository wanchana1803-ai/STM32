# สรุป Lab03_UART — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

สร้าง transport Serial และ parser ที่ทดสอบได้โดยไม่มีหน้าต่าง

แยก transport/parser/UI และใช้ queue เป็นขอบเขต thread timeout ช่วยให้ shutdown ได้ แต่ไม่ใช่ตัวจบ frame

**Widgets/เครื่องมือ:** Combobox รายชื่อพอร์ต, baud display, Connect/Disconnect, Text log จำกัดขนาด

**คำถามทบทวน:** read timeout คืน b"ACK,ab" มาแล้วควร parse ทันทีหรือไม่?

**แนวตอบ:** ไม่ เก็บ bytes ต่อจนเจอ LF หรือเกินขอบเขต ห้ามตีความ timeout เป็นจบ frame

## Checklist ก่อนจบ

- partial/multiple/oversized frames กู้คืนได้
- พอร์ตไม่อยู่/ถูกใช้แสดง error และ UI ยังปิดได้
- connect-disconnect 10 ครั้งไม่มี worker หรือพอร์ตค้าง

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
