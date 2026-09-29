# คู่มือ Register Lab09: Quadrature Encoder ด้วย TIM5

TIM encoder mode ต่อสัญญาณ A/B เข้าช่อง CH1/CH2 แล้ว hardware เพิ่มหรือลด `CNT` ตาม phase ขาตัวอย่างที่เป็นไปได้คือ PA0/PA1 AF2 แต่ต้องตรวจ `.ioc`

## Register ที่ใช้

| Register | ฟิลด์หลัก | หน้าที่ |
|---|---|---|
| `RCC->APB1ENR` | `TIM5EN` | เปิด clock TIM5 |
| `GPIOx->MODER/AFRx` | AF ของ TIM5_CH1/CH2 | ต่อขา A/B เข้าตัว timer |
| `TIM5->SMCR` | `SMS[2:0]` | encoder mode 1/2/3 |
| `TIM5->CCMR1` | `CC1S`, `CC2S`, `IC1F`, `IC2F`, prescaler | map input และ digital filter |
| `TIM5->CCER` | `CC1P/NP`, `CC2P/NP` | polarity ของ input |
| `TIM5->PSC` | prescaler | ปกติไม่ใช่ตัวกำหนด RPM แบบ timebase |
| `TIM5->ARR` | counter top | ช่วงและ wrap ของ position counter |
| `TIM5->CNT` | position count | เพิ่ม/ลดตามทิศทาง |
| `TIM5->CR1` | `CEN`, `DIR` | เปิด counter; `DIR` แสดงทิศทางปัจจุบัน |
| `TIM5->SR` | `UIF`, capture flags | wrap/update และสถานะช่อง |

## ตรวจค่า

1. `SMS` ต้องเป็น encoder mode ที่เลือกใน CubeMX
2. `CC1S/CC2S` ต้อง map เป็น TI1/TI2 และ GPIO AF ถูกต้อง
3. หมุนช้าไปข้างหน้า/ย้อนกลับ แล้วดู `CNT` เปลี่ยนคนละทิศ
4. หาก count กระโดด ให้เพิ่ม input filter อย่างมีเหตุผลและตรวจสัญญาณด้วย logic analyzer

## คำนวณ delta แบบผ่าน wrap

เก็บค่า `CNT` เป็นชนิด unsigned ที่กว้างเท่าตัว counter แล้วหาผลต่างด้วย arithmetic แบบ modulo หรือกำหนด `ARR` และชนิดข้อมูลให้สอดคล้อง อย่าลบด้วย signed type แบบไม่กำหนดพฤติกรรมที่ขอบ

```text
RPM = delta_count × 60 / (counts_per_revolution × delta_time_seconds)
```

ต้องระบุว่า counts/revolution นับแบบ x1, x2 หรือ x4 ตาม encoder mode
