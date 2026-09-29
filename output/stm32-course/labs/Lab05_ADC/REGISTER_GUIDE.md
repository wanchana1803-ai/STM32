# คู่มือ Register Lab05: ADC1

ตัวอย่างใช้ ADC1 แบบ polling หนึ่ง channel ขาและ channel number ต้องยึด `.ioc`

## Register ที่ใช้

| Register | ฟิลด์หลัก | หน้าที่ |
|---|---|---|
| `RCC->AHB1ENR` | `GPIOxEN` | เปิด clock พอร์ต analog |
| `GPIOx->MODER` | `11` ของขา | analog mode |
| `GPIOx->PUPDR` | `00` | ไม่มี pull สำหรับ analog โดยทั่วไป |
| `RCC->APB2ENR` | `ADC1EN` | เปิด clock ADC1 |
| `ADC1->SR` | `EOC`, `STRT`, `OVR` | conversion complete/start/overrun |
| `ADC1->CR1` | resolution, scan, interrupt | รูปแบบ conversion |
| `ADC1->CR2` | `ADON`, `SWSTART`, trigger, alignment, continuous | เปิดและเริ่ม ADC |
| `ADC1->SMPR1/2` | sample time ราย channel | เวลาที่วงจร sample ต่อ input |
| `ADC1->SQR1/2/3` | sequence length/order | เลือก channel และลำดับ conversion |
| `ADC1->DR` | conversion data | ผลแปลงตาม alignment/resolution |
| `ADC->CCR` | prescaler/common config | clock ADC และ common mode |

## ลำดับ polling

`ADON=1 → start trigger/SWSTART → รอ EOC → อ่าน DR`

HAL ที่สอดคล้องคือ `HAL_ADC_Start()`, `HAL_ADC_PollForConversion()`, `HAL_ADC_GetValue()` และ `HAL_ADC_Stop()` การอ่าน `DR` อาจเปลี่ยนสถานะ flag จึงอย่าอ่านแทรกระหว่าง HAL polling โดยไม่มีแผน

## ตรวจค่า

- `MODERn=11`, `PUPDRn=00`
- channel ใน `SQR3.SQ1` ตรงกับขาจริง
- sample time เหมาะกับ impedance ของแหล่งสัญญาณ
- 12-bit right-aligned ให้ `DR` อยู่ 0–4095

```text
Vin ≈ raw × VREF / 4095
```

VREF ต้องเป็นค่าที่วัดหรือสมมติอย่างชัดเจน ค่า raw เฉลี่ยลด noise แต่ไม่แก้ VREF/calibration error
