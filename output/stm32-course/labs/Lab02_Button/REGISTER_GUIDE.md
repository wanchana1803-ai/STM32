# คู่มือ Register Lab02: Button และ Debounce

Lab นี้อ่าน GPIO input แล้วใช้เวลาเพื่อแปลงสัญญาณที่เด้งให้เป็นเหตุการณ์กดหนึ่งครั้ง บน NUCLEO-F410RB ปุ่ม B1 มักถูกกำหนดเป็น PC13 แต่ให้ยืนยันชื่อขาและ polarity จาก Board Selector และไฟล์ `.ioc`

## เส้นทางสัญญาณ

`RCC clock → GPIOx configuration → IDR → debounce state machine → LED BSRR/ODR`

## Register ที่ใช้

| Register | ช่องสำคัญ | หน้าที่/ค่าที่ควรตรวจ |
|---|---|---|
| `RCC->AHB1ENR` | `GPIOxEN` | ต้องเป็น 1 สำหรับพอร์ตของปุ่มและ LED |
| `GPIOx->MODER` | `MODERn[1:0]` | `00` = input สำหรับปุ่ม |
| `GPIOx->PUPDR` | `PUPDRn[1:0]` | `00` none, `01` pull-up, `10` pull-down; ต้องตรงวงจร |
| `GPIOx->IDR` | `IDRn` | ระดับไฟฟ้าที่ขา ณ ขณะอ่าน |
| `GPIOA->ODR` | `ODR5` | สถานะ latch ของ LD2 |
| `GPIOA->BSRR` | `BS5`, `BR5` | set/reset LD2 แบบ atomic |
| `SysTick->CTRL/LOAD/VAL` | clock, reload, current | timebase ที่ `HAL_GetTick()` ใช้ทำ debounce |

ตำแหน่งฟิลด์ GPIO ขา `n`: `MODER/PUPDR` เริ่มที่บิต `2n`, ส่วน `IDR/ODR` ใช้บิต `n`

```c
uint32_t raw = (GPIOC->IDR >> 13U) & 0x1U; // ตัวอย่าง PC13
```

ค่า `raw` ยังไม่ใช่ “กดแล้ว” จนกว่าจะตีความ polarity เช่น active-low ใช้ `pressed = (raw == 0U)`

## ขั้นตรวจใน SFRs

1. หลัง `MX_GPIO_Init()` ตรวจ `GPIOxEN=1`, `MODERn=0`
2. ดู `PUPDRn` เทียบกับ CubeMX และวงจรบนบอร์ด
3. Pause ตอนปล่อยและตอนกด แล้วบันทึก `IDRn` ทั้งสองค่า
4. ตรวจว่า counter เพิ่มที่ขอบกดหลังผ่าน debounce และไม่เพิ่มซ้ำเมื่อกดค้าง

## จุดที่มักสับสน

- `IDR` คือระดับขาจริง ส่วน `ODR` คือ output latch จึงอย่าอ่าน `ODR` เพื่อดูปุ่ม
- Internal pull อาจถูกแทนที่ด้วยตัวต้านทานบนบอร์ด การรู้ active-high/low ต้องดู schematic
- Debounce เป็นตรรกะซอฟต์แวร์ ไม่มี “debounce register”; SysTick ให้เพียงฐานเวลา
