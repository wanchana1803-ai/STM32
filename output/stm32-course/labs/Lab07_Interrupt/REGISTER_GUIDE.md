# คู่มือ Register Lab07: Timer Interrupt และ EXTI

Lab นี้มีสองชั้น: peripheral สร้างเหตุการณ์ แล้ว NVIC อนุญาตและจัดลำดับการเข้า ISR

## Timer interrupt

| Register | ฟิลด์ | หน้าที่ |
|---|---|---|
| `TIMx->DIER` | `UIE` | ส่ง update event ไปเป็น interrupt request |
| `TIMx->SR` | `UIF` | pending ที่ฝั่ง timer; ISR ต้อง clear ถูกวิธี |
| `TIMx->PSC/ARR/CR1` | timing, `CEN` | กำหนดความถี่และเปิด counter |

## External interrupt จาก GPIO

| Register | ฟิลด์ | หน้าที่ |
|---|---|---|
| `RCC->APB2ENR` | `SYSCFGEN` | เปิด clock SYSCFG |
| `SYSCFG->EXTICR[n]` | EXTI line source | เลือก GPIO port ให้ line 0–15 |
| `EXTI->IMR` | `MRx` | unmask interrupt line |
| `EXTI->RTSR` | `TRx` | trigger ขอบขาขึ้น |
| `EXTI->FTSR` | `TRx` | trigger ขอบขาลง |
| `EXTI->PR` | `PRx` | pending; STM32 รุ่นนี้ล้างโดยเขียน 1 ที่บิตนั้น |

## NVIC ของ Cortex-M4

| Register | หน้าที่ |
|---|---|
| `NVIC->ISER[]` | enable IRQ |
| `NVIC->ICER[]` | disable IRQ |
| `NVIC->ISPR[]` / `ICPR[]` | set/clear pending |
| `NVIC->IP[]` | priority |

CubeMX สร้าง `HAL_NVIC_SetPriority()` และ `HAL_NVIC_EnableIRQ()` รวมถึง handler ใน `stm32f4xx_it.c`

## เส้นทาง debug

`event → peripheral flag → interrupt enable → NVIC pending/enable → IRQHandler → HAL callback`

หากไม่เข้า callback ให้ไล่ตามเส้นทางนี้ทีละจุด หากเข้า ISR วนซ้ำให้ตรวจว่า peripheral pending flag ถูก clear แล้ว ไม่ใช่ดูเฉพาะ NVIC

ตัวแปรที่ ISR และ main ใช้ร่วมกันควรเป็น `volatile` เพื่อบังคับการอ่าน/เขียนจริง แต่ `volatile` ไม่รับประกัน atomicity หรือแก้ race condition ใช้ critical section หรือ snapshot ตามขนาดข้อมูลและรูปแบบการใช้งาน
