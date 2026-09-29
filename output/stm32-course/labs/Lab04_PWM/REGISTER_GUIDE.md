# คู่มือ Register Lab04: PWM ด้วย TIM1

บทเรียนใช้ตัวอย่าง TIM1 Channel 1 ขาจริงขึ้นกับ AF mapping ใน `.ioc` สูตรด้านล่างใช้ edge-aligned up-counting

## Register ที่ใช้

| Register | ฟิลด์หลัก | หน้าที่ |
|---|---|---|
| `RCC->APB2ENR` | `TIM1EN` | เปิด clock TIM1 |
| `GPIOx->MODER/AFRx` | mode `10`, AF ของ TIM1_CH1 | ส่งสัญญาณ timer ออกขา |
| `TIM1->CR1` | `CEN`, `DIR`, `CMS`, `ARPE` | เริ่มนับ รูปแบบนับ และ preload ARR |
| `TIM1->PSC` | `PSC[15:0]` | หาร timer clock ด้วย `PSC+1` |
| `TIM1->ARR` | auto-reload | กำหนดจำนวน count ต่อคาบ |
| `TIM1->CCR1` | compare | กำหนดตำแหน่งเปลี่ยนระดับของ CH1 |
| `TIM1->CCMR1` | `CC1S`, `OC1M`, `OC1PE` | output compare, PWM mode, preload |
| `TIM1->CCER` | `CC1E`, `CC1P` | เปิด output และเลือก polarity |
| `TIM1->EGR` | `UG` | โหลดค่า prescaler/preload ด้วย update event |
| `TIM1->SR` | `UIF`, `CC1IF` | status update/compare |
| `TIM1->BDTR` | `MOE`, dead-time/break | TIM1 ต้องมี `MOE=1` จึงส่ง main output |

## สูตร

```text
fPWM = fTIM / ((PSC + 1) × (ARR + 1))
duty ≈ CCR1 / (ARR + 1) × 100%
```

เมื่อ APB prescaler มากกว่า 1 timer clock โดยทั่วไปเป็น 2 เท่าของ PCLK ของ bus นั้น ต้องอ่าน clock tree/CubeMX ก่อนคำนวณ

## ตรวจใน SFRs

1. `TIM1EN=1`, GPIO เป็น AF ที่ตรงกับ CH1
2. `CC1S=00` และ `OC1M=110` สำหรับ PWM mode 1
3. `CC1E=1`, `BDTR.MOE=1`, `CR1.CEN=1`
4. ดู `CNT` วิ่ง 0 ถึง `ARR` และวัดขาจริงด้วย oscilloscope/logic analyzer
5. เปลี่ยน duty 10/50/90% แล้วตรวจ `CCR1` โดยความถี่ต้องไม่เปลี่ยน

`CCR1` ที่มากกว่า `ARR+1` ทำให้ output ค้างในสถานะ active ตาม mode/polarity จึงต้องจำกัด input ก่อนเขียน
