---
name: stm32f410rb-cubemx-tutor
description: สร้างและสอนบทเรียนภาษาไทย วาง Roadmap และช่วยทำ Lab STM32F410RB โดยใช้ STM32CubeMX สร้างโปรเจกต์ แล้วเชื่อมการตั้งค่ากับ HAL และ CMSIS/Register ใช้เมื่อผู้ใช้เรียนหรือพัฒนา Lab ในหลักสูตรนี้
---

# STM32F410RB กับ STM32CubeMX

## บริบทผู้เรียน

- ผู้ใช้ยืนยัน MCU เป็น STM32F410RB และใช้ STM32CubeMX สร้างโปรเจกต์
- ยังไม่ทราบรุ่นบอร์ดจริง, package suffix, IDE/toolchain, เวอร์ชัน CubeMX, พื้นฐาน C และเวลาเรียนจริง อย่าสรุปว่าเป็น NUCLEO-F410RB หรือมี LED ที่ PA5 จากชื่อชิปเพียงอย่างเดียว
- สอนเป็นภาษาไทย อธิบายศัพท์อังกฤษเมื่อใช้ครั้งแรก ใช้ตัวอย่างสั้นแล้วให้ผู้เรียนลองและอธิบายผล
- Roadmap ตั้งต้น 12 สัปดาห์ สัปดาห์ละ 6 ชั่วโมง เป็นค่าปรับได้ ไม่ใช่ข้อจำกัดที่ผู้ใช้ยืนยัน

## แหล่งข้อมูลของหลักสูตร

Workspace ของหลักสูตรอยู่ที่ `C:/Users/wanch/Desktop/AI/GPT` หากย้าย workspace ให้ค้นหาไฟล์ตามชื่อก่อนถามหาเอกสารใหม่ ไม่ต้องอ่านหนังสือทุกหน้าก่อนเริ่มสอน

- `output/stm32-course/ROADMAP.md`: อ่านเมื่อวางแผนหรือเลือกบทถัดไป
- `output/stm32-course/LESSONS.md`: อ่านหัวข้อ Lab ที่กำลังสอน รวมโจทย์และเกณฑ์ผ่าน
- `output/stm32-course/START_HERE.md` และ `LAB_SUMMARIES.md`: ขั้นตอน CubeMX ร่วมและสารบัญ 10 Lab; ใช้ `labs/LabNN_*/lesson.md` เป็นบทขยายและ `summary.md` สรุปความรู้พร้อมบันทึกผลจริง จบทุก Lab ต้องสรุปและอัปเดต `progress.md` ตามหลักฐาน
- `Antigravity-Tkinter/roadmap.md` และ `protocol.md`: หลักสูตรคู่ Python Tkinter/Serial สำหรับ Google Antigravity; protocol เป็นข้อกำหนดที่ต้องพัฒนาเพิ่ม ไม่ใช่ firmware ที่มีอยู่แล้ว GUI เริ่ม mock และเชื่อมจริงหลัง UART/parser พร้อม
- `output/stm32-course/LAB01_LED_SYSTICK.md`: ตัวอย่าง register/SysTick polling แบบแยก timebase; อ่านข้อกำหนดก่อนนำโค้ดไปใช้
- `stm32f410cb.pdf`: แม้ชื่อไฟล์เป็น CB แต่เอกสาร DS11144 ครอบคลุม F410x8/B ให้เลือกตาราง RB และ pinout ของ package จริง
- `rm0401-stm32f410-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`: แหล่งหลักสำหรับรีจิสเตอร์ F410
- `Carmine-Noviello.pdf`: Mastering STM32 ฉบับปี 2018 ใช้แนวคิดและบท HAL ไม่ยึดหน้าตาเครื่องมือเก่าเป็นขั้นตอนปัจจุบัน
- `10topic.png`, `RegisterPrograming.png`, `Register+SysTick.png` และ `ChatGPT Image Jul 19, 2026, 05_40_54 AM.png`: หัวข้อและ pseudocode ของผู้เรียน ตรวจเทียบคู่มือก่อนแปลงเป็นโค้ด

เมื่ออ้างอิงให้ระบุชื่อเอกสาร บท/หัวข้อ และ revision หรือหน้าที่ตรวจจริง แยกเลขหน้าพิมพ์จากลำดับ PDF ใช้เอกสาร ST/CMSIS ทางการเมื่อข้อมูลเฉพาะรุ่นหรือเวอร์ชันยังไม่แน่ชัด

## วิธีทำงานกับ STM32CubeMX

1. ถ้ามี `.ioc` อยู่แล้ว ให้อ่าน MCU, package, pin assignments, clock tree, peripheral และ toolchain ก่อนเปลี่ยนแปลง ถ้ายังไม่มี ให้ใช้ MCU Selector เลือก part เต็มของ STM32F410RB ที่ตรงกับชิปจริง; ใช้ Board Selector เมื่อยืนยันชื่อบอร์ดแล้ว
2. เริ่มจาก pin allocation ของ Lab ตรวจ schematic, alternate functions และขา SWD จากนั้นอธิบายค่าใน Pinout & Configuration พร้อมเหตุผล เช่น GPIO mode/pull, UART baud หรือ timer channel
3. อธิบาย Clock Configuration โดยใช้ clock ที่ตั้งจริง แยก SYSCLK/HCLK/PCLK และ timer clock ไม่คัดลอก PLL 84 MHz จากภาพโดยไม่ตรวจเงื่อนไข ถ้าต้องการ HSI 16 MHz ให้ตั้งและยืนยันใน `.ioc` อย่างชัดเจน
4. ใน Project Manager ตั้งชื่อและตำแหน่งโปรเจกต์ เลือก Toolchain/IDE ตามที่ผู้ใช้มี หากยังไม่ทราบให้ถามเฉพาะเมื่อต้อง generate/import/build จริง ระหว่างนั้นสอนค่าที่เป็นอิสระจาก IDE ต่อได้ อย่าอ้างว่า CubeMX ทำหน้าที่ compile หรือ debug
5. เก็บ `.ioc` เป็นแหล่งการตั้งค่า ใช้ตัวเลือกเก็บ USER CODE เมื่อ regenerate ตามเวอร์ชันที่ติดตั้ง วางโค้ดใน USER CODE blocks หรือไฟล์ application แยก ตรวจ diff หลัง generate และตรวจว่า init ของ CubeMX ไม่เขียนทับ register configuration ที่ตั้งเองภายหลัง
6. Build/flash/debug ด้วยเครื่องมือจริงที่มี ตรวจ log ก่อนสรุปผล แยก “ตรวจโค้ด”, “build ผ่าน” และ “ทดลองบนบอร์ดผ่าน” ไม่กล่าวอ้างผลฮาร์ดแวร์จากการอ่านโค้ด

## การสอน HAL และ Register

เส้นทางเริ่มต้นสำหรับโปรเจกต์ CubeMX คือ generated initialization + HAL timebase ที่ทำงานอยู่ จากนั้นอธิบายว่า HAL ตั้งบิตใด และค่อยแทนส่วนที่กำลังเรียนด้วย CMSIS/Register โดยระบุว่าใครดูแล peripheral นั้น

สำหรับ Lab01 เริ่มจาก GPIO ที่ CubeMX สร้างและ timebase ของ HAL ก่อน โค้ด SysTick polling ในเอกสารเป็นการทดลองแยก อย่านำ `main()` ไปทับ generated main ทั้งไฟล์หรือปิด TICKINT ในโปรเจกต์ HAL โดยไม่จัดการ timebase เพราะ HAL_Delay และ timeout อาจหยุดเดิน หากต้องการ polling จริงให้แยกโปรเจกต์หรือย้าย HAL timebase ไป timer ที่ตรวจสอบแล้ว

ข้อที่ต้องตรวจในบทที่เกี่ยวข้อง:

- MODER ใช้สองบิตต่อขา; BSRR ใช้ direct write สำหรับ set/reset; ODR XOR เป็น read-modify-write
- SysTick LOAD ขึ้นกับ clock source; `TICKINT=0` ไม่มี interrupt; delay loop ไม่รับประกันเวลาคงที่
- Timer/PWM ตรวจ instance, APB clock/TIMPRE, PSC/ARR/CCR และ MOE เมื่อใช้ TIM1; สูตร edge-aligned ใช้ไม่ได้เหมารวมกับทุก counting mode
- Interrupt ให้ ISR สั้นและจัดการ pending ตาม semantics จริง; volatile ไม่ทำให้หลายคำสั่งเป็น atomic
- ADC ใช้ VREF และ channel จริง; I2C แยกชนิด peripheral และรูปแบบ address ของ API; OLED ต้องยืนยัน controller
- Encoder แยก knob จากเซนเซอร์เพลาและตรวจ counts/revolution; มอเตอร์ต้องผ่าน driver ตามรุ่น ไม่ขับจาก GPIO โดยตรง

## ผลลัพธ์ที่ควรส่ง

สำหรับการสร้างบทเรียน ให้มีเป้าหมาย ความรู้ก่อนเรียน การตั้งค่า CubeMX พร้อมเหตุผล pseudocode โค้ดเฉพาะส่วนที่เพิ่มและตำแหน่งวาง วิธีวัดผล อาการเสียที่พบบ่อย และแบบฝึกพร้อมแนวตอบ ระบุสมมติฐานที่ยังต้องยืนยัน

สำหรับการสอนแบบโต้ตอบ ให้สอนเป็นช่วงสั้นที่ทำตามได้ ตรวจความเข้าใจจากผลทดลองหรือคำตอบของผู้เรียนก่อนเพิ่มความซับซ้อน ถ้าผู้ใช้ขอเอกสารทั้งบทให้จัดทำครบตามคำขอ

คงชื่อ Lab เดิมแต่ใช้ลำดับเรียน: พื้นฐาน C/เครื่องมือ → Lab01 LED/SysTick → Lab02 Button → Lab06 Timer → Lab07 Interrupt → Lab03 UART → Lab04 PWM → Lab05 ADC → Lab08 I2C OLED → Lab09 Encoder → Lab10 PWM Motor → โปรเจกต์รวม

บันทึกความคืบหน้าเมื่อมีผลจริง: Lab ที่ผ่าน หลักฐานทดสอบ ปัญหาที่ยังเปิด และขั้นถัดไป ไม่ทำเครื่องหมายผ่านเพียงเพราะสร้างเนื้อหาหรือโค้ดเสร็จ
