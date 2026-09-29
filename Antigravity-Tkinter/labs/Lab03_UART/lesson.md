# Lab03_UART — Python Tkinter

## เป้าหมาย

สร้าง transport Serial และ parser ที่ทดสอบได้โดยไม่มีหน้าต่าง

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

แยก transport/parser/UI และใช้ queue เป็นขอบเขต thread timeout ช่วยให้ shutdown ได้ แต่ไม่ใช่ตัวจบ frame

Widgets: Combobox รายชื่อพอร์ต, baud display, Connect/Disconnect, Text log จำกัดขนาด

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

1. ใช้ serial.tools.list_ports.comports แสดงพอร์ตและให้เลือกเอง ไม่ hardcode COM3
2. ให้ worker เปิด Serial(timeout=0.1, write_timeout=0.2) และเป็นเจ้าของทั้ง read/write
3. worker รับคำสั่งผ่าน bounded queue อ่าน bytes แล้วแยก LF ด้วย buffer มีขอบเขต
4. ส่ง parsed event เข้า queue; UI ใช้ after ดึงทีละ batch โดยไม่แตะ widget จาก worker
5. Connect ทำ HELLO; Disconnect ปิด session และ pending; ปิดหน้าต่างคืนพอร์ต
6. ตรวจตาม protocol ทั้ง ACK/ERR และ frame ผิดก่อนเชื่อม Lab อื่น

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
import queue
events = queue.Queue(maxsize=200)

def poll_events():
    for _ in range(50):
        try:
            event = events.get_nowait()
        except queue.Empty:
            break
        handle_event(event)  # Parse/validate earlier; render here.
    root.after(20, poll_events)

```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

- partial/multiple/oversized frames กู้คืนได้
- พอร์ตไม่อยู่/ถูกใช้แสดง error และ UI ยังปิดได้
- connect-disconnect 10 ครั้งไม่มี worker หรือพอร์ตค้าง

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

read timeout คืน b"ACK,ab" มาแล้วควร parse ทันทีหรือไม่?

แนวตอบ: ไม่ เก็บ bytes ต่อจนเจอ LF หรือเกินขอบเขต ห้ามตีความ timeout เป็นจบ frame

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

แยก transport/parser/UI และใช้ queue เป็นขอบเขต thread timeout ช่วยให้ shutdown ได้ แต่ไม่ใช่ตัวจบ frame

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/Lab03_UART/lesson.md)
