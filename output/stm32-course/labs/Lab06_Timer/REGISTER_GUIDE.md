# คู่มือ Register Lab06: Basic Timebase ด้วย TIM5

ตัวอย่างใช้ TIM5 internal clock และ polling update flag

## Register ที่ใช้

| Register | ฟิลด์หลัก | หน้าที่ |
|---|---|---|
| `RCC->APB1ENR` | `TIM5EN` | เปิด clock TIM5 |
| `TIM5->CR1` | `CEN`, `DIR`, `OPM`, `ARPE` | เปิด counter และเลือกรูปแบบ |
| `TIM5->PSC` | prescaler | หาร clock ด้วย `PSC+1` |
| `TIM5->ARR` | auto-reload | จุด wrap/เกิด update |
| `TIM5->CNT` | counter | ค่า count ปัจจุบัน; TIM5 เป็น 32-bit |
| `TIM5->EGR` | `UG` | บังคับ update/load prescaler |
| `TIM5->SR` | `UIF` | update event เกิดแล้ว |
| `TIM5->DIER` | `UIE` | อนุญาต update interrupt; polling ปกติเป็น 0 |
| `TIM5->SMCR` | `SMS`, `TS` | internal clock ปกติใช้ slave mode disabled |

## สูตรคาบ

```text
Tupdate = (PSC + 1) × (ARR + 1) / fTIM
```

ถ้า APB1 prescaler มากกว่า 1 ให้ตรวจกฎ timer clock x2 ใน clock tree

## ทดลองดูค่า

1. หลัง init ตรวจ `TIM5EN=1`, `PSC`, `ARR`
2. หลัง `HAL_TIM_Base_Start()` ตรวจ `CEN=1`
3. Resume สั้น ๆ แล้ว Pause หลายครั้ง ค่า `CNT` ควรเปลี่ยน
4. เมื่อ wrap `UIF=1`; ล้างด้วยวิธีที่ HAL/Reference Manual กำหนด

Flag เป็นเพียงหลักฐานว่าเคยเกิด event อย่างน้อยหนึ่งครั้ง หาก main polling ช้าและเกิดหลายรอบก่อนอ่าน `UIF` โปรแกรมจะไม่ทราบจำนวนรอบที่หายไป
