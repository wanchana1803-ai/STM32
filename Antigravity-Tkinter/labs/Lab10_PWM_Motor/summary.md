# สรุป Lab10_PWM_Motor — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

สร้างหน้าควบคุมมอเตอร์ที่ state ชัดและไม่ replay คำสั่งหลังต่อใหม่

State ที่ GUI แสดงต้องตรงกับหลักฐาน การสูญเสีย link ทำให้ผลทางกายภาพไม่ทราบ และ firmware ต้องหยุดเองตาม watchdog

**Widgets/เครื่องมือ:** ARM, STOP เด่น, duty slider, requested/applied labels, link/fault state และ heartbeat indicator

**คำถามทบทวน:** เมื่อ port หลุดควรตั้งข้อความ STOPPED ทันทีไหม?

**แนวตอบ:** ไม่ ให้ UNKNOWN/link lost จนมีหลักฐาน Firmware watchdog เป็นผู้สั่งหยุดโดยไม่พึ่ง GUI

## Checklist ก่อนจบ

- เปิด GUI/reconnect แล้วไม่มี MOTOR command อัตโนมัติ
- slider backlog ไม่ขวาง STOP
- ปิดโปรแกรมหรือ mock link loss แล้วไม่แสดง false stopped
- บนบอร์ดจริงพิสูจน์ watchdog ด้วยการหยุด heartbeatและวัด output

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
