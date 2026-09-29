# รายงานสรุปการทดลอง Lab01: LED และ SysTick

คู่มือรีจิสเตอร์ประกอบการทดลอง: [REGISTER_GUIDE.md](REGISTER_GUIDE.md)

## ข้อมูลการทดลอง

- วันที่: 29 กันยายน 2026
- บอร์ด: NUCLEO-F410RB
- MCU: STM32F410RB
- เครื่องมือสร้างการตั้งค่า: STM32CubeMX
- IDE / Debugger: STM32CubeIDE / ST-LINK บนบอร์ด
- อุปกรณ์แสดงผล: LD2 สีเขียวบนบอร์ด เชื่อมกับ PA5 แบบ active-high

## วัตถุประสงค์

1. ตั้ง PA5 เป็น GPIO output และควบคุม LD2
2. เปรียบเทียบ HAL กับการเขียน GPIO register
3. สร้างการกระพริบแบบไม่บล็อกด้วย `HAL_GetTick()`
4. ตรวจการตั้งค่า GPIO และ SysTick ผ่าน SFRs/Expressions

## การตั้งค่า GPIO

| รายการ | ค่า |
|---|---|
| Pin | PA5 / LD2 |
| Mode | GPIO Output |
| Output type | Push-pull |
| Pull | No pull-up / no pull-down |
| Speed | Low |
| Initial output | Low / LED ดับ |

CubeMX สร้าง initialization และ HAL timebase ส่วน application ทดลองควบคุม LED ผ่าน HAL, `ODR` และ `BSRR`

## วิธีทดลอง

1. กระพริบ LED ด้วย `HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5)` และ `HAL_Delay(500)`
2. เปลี่ยนเป็น elapsed-time scheduling ด้วย `HAL_GetTick()` เพื่อลดการบล็อก main loop
3. เปลี่ยนคำสั่งสลับเป็น `GPIOA->ODR ^= (1UL << 5)` และตรวจ `ODR5`
4. เปลี่ยนเป็นการ set/reset แบบเจาะจงด้วย `GPIOA->BSRR` บิต 5 และบิต 21
5. ตรวจ `MODER5` และ bit field ใน SFRs พร้อมใช้ shift/mask ใน Expressions
6. ตรวจ `SystemCoreClock`, `SysTick->LOAD` และ `SysTick->CTRL`
7. ทดลอง interval 100, 500 และ 1000 ms

## ผลการทดลอง

| รายการตรวจ | ผลที่คาด | ผลที่รายงาน | สถานะ |
|---|---|---|---|
| HAL GPIO | LD2 กระพริบ | กระพริบ | ผ่าน |
| ODR/BSRR | PA5 เปลี่ยน LOW/HIGH | LED ทำงานและ ODR5 เปลี่ยน | ผ่าน |
| MODER5 | `1` หรือฐานสอง `01` | `0x1` | ผ่าน |
| SystemCoreClock | ตาม Clock Configuration | 84,000,000 Hz | ผ่าน |
| SysTick LOAD | 84,000 - 1 | 83,999 | ผ่าน |
| CTRL bits 2:0 | ENABLE/TICKINT/CLKSOURCE = `111` | `7` | ผ่าน |
| Interval 100 ms | คาบเต็มประมาณ 200 ms | ลักษณะการกระพริบตรงตามคาดด้วยสายตา | ผ่านแบบสังเกต |
| Interval 500 ms | คาบเต็มประมาณ 1 s | ลักษณะการกระพริบตรงตามคาดด้วยสายตา | ผ่านแบบสังเกต |
| Interval 1000 ms | คาบเต็มประมาณ 2 s | ลักษณะการกระพริบตรงตามคาดด้วยสายตา | ผ่านแบบสังเกต |

ค่าของ SysTick สอดคล้องกับสูตร:

```text
LOAD = SystemCoreClock / 1000 - 1
     = 84,000,000 / 1000 - 1
     = 83,999
```

## ความรู้ที่ได้

- PA5 ใช้ `MODER[11:10]`; ค่า `01` หมายถึง output
- `ODR5` แสดงสถานะ output latch ของ PA5
- `ODR ^= mask` เป็น read-modify-write ส่วน `BSRR` สั่ง set/reset เฉพาะบิตได้โดยตรง
- CubeIDE แสดง `[10:2]` ว่าเริ่มที่บิต 10 และ field กว้าง 2 บิต ไม่ใช่ช่วงบิต 10 ถึง 2
- การอ่าน field ใช้ `(register >> position) & mask`
- `HAL_GetTick()` อาศัย SysTick interrupt ที่เพิ่ม tick ทุก 1 ms
- การตรวจ elapsed time ทำให้ main loop ทำงานอื่นระหว่างรอได้

## ข้อจำกัดของผล

การตรวจช่วงเวลา 100/500/1000 ms ใช้การสังเกต LED ด้วยสายตา จึงยืนยันเพียงพฤติกรรมโดยประมาณ ยังไม่ได้วัดคาบและ duty cycle ด้วย oscilloscope หรือ logic analyzer

## สรุป

Lab01 ผ่านตามขอบเขตการเรียนหลัก: ตั้งและควบคุม GPIO, ใช้ HAL และ register, อ่าน bit field, ใช้ `BSRR`, สร้าง timing แบบไม่บล็อก และตรวจ SysTick ที่ clock 84 MHz ขั้นต่อไปคือ Lab02 Button และ software debounce
