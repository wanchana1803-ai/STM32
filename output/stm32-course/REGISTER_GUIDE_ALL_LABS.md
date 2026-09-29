# คู่มือ Register ครบ 10 Lab — STM32F410RB

คู่มือนี้เป็นแผนที่รวมสำหรับ NUCLEO-F410RB ที่สร้างโปรเจกต์ด้วย STM32CubeMX และพัฒนาด้วย STM32CubeIDE รายละเอียดของแต่ละ Lab อยู่ในลิงก์ท้ายตาราง

> **หลักการสำคัญ:** ชื่อพอร์ต ขา Alternate Function และหมายเลข peripheral ต้องยึดไฟล์ `.ioc` ของโปรเจกต์จริง ตัวอย่างในคู่มือนี้ใช้ peripheral ตามบทเรียน หากเลือกต่างออกไป ให้เปลี่ยนชื่อ block ให้ตรงกับ `.ioc`

## วิธีใช้คู่มือ

1. เปิด Debug แล้วหยุดที่ `while (1)` หลังฟังก์ชัน `MX_*_Init()` ทำงานแล้ว
2. เปิด `Window > Show View > SFRs`
3. ขยาย `STM32F410 > RCC` และ peripheral ของ Lab
4. ตรวจบิตด้วย `(REGISTER >> bit) & mask` ใน Expressions
5. เปลี่ยน input/output จริง แล้วกด Resume/Pause เพื่อเปรียบเทียบค่า

`& mask` ใช้ตัดบิตอื่นทิ้ง เช่น `(GPIOA->ODR >> 5) & 0x1U` เหลือเพียงสถานะ PA5 ส่วน suffix `U` ระบุว่าเป็นจำนวนเต็ม unsigned

## แผนที่ Register

| Lab | Peripheral | Register หลัก | คู่มือ |
|---|---|---|---|
| 01 LED/SysTick | RCC, GPIOA, SysTick | `AHB1ENR`, `MODER`, `ODR`, `BSRR`, `CTRL`, `LOAD`, `VAL` | [เปิด](labs/Lab01_LED/REGISTER_GUIDE.md) |
| 02 Button | RCC, GPIO input, SysTick | `AHB1ENR`, `MODER`, `PUPDR`, `IDR`, SysTick | [เปิด](labs/Lab02_Button/REGISTER_GUIDE.md) |
| 03 UART | RCC, GPIO AF, USART2 | `APB1ENR`, `MODER`, `AFRL`, `SR`, `DR`, `BRR`, `CR1–3` | [เปิด](labs/Lab03_UART/REGISTER_GUIDE.md) |
| 04 PWM | RCC, GPIO AF, TIM1 | `PSC`, `ARR`, `CCR1`, `CCMR1`, `CCER`, `BDTR` | [เปิด](labs/Lab04_PWM/REGISTER_GUIDE.md) |
| 05 ADC | RCC, GPIO analog, ADC1 | `SR`, `CR1`, `CR2`, `SMPRx`, `SQRx`, `DR`, `CCR` | [เปิด](labs/Lab05_ADC/REGISTER_GUIDE.md) |
| 06 Timer | RCC, TIM5 | `CR1`, `PSC`, `ARR`, `CNT`, `EGR`, `SR`, `DIER` | [เปิด](labs/Lab06_Timer/REGISTER_GUIDE.md) |
| 07 Interrupt | EXTI, SYSCFG, NVIC, TIM | `EXTICR`, `IMR`, `RTSR`, `FTSR`, `PR`, `ISER`, `IPR`, `DIER`, `SR` | [เปิด](labs/Lab07_Interrupt/REGISTER_GUIDE.md) |
| 08 I2C OLED | RCC, GPIO AF, I2C1 | `CR1`, `CR2`, `SR1`, `SR2`, `DR`, `CCR`, `TRISE` | [เปิด](labs/Lab08_I2C_OLED/REGISTER_GUIDE.md) |
| 09 Encoder | RCC, GPIO AF, TIM5 | `SMCR`, `CCMR1`, `CCER`, `ARR`, `CNT`, `CR1` | [เปิด](labs/Lab09_Encoder/REGISTER_GUIDE.md) |
| 10 PWM Motor | GPIO, TIM1, SysTick/Timer | PWM registers, `BSRR`, `BDTR`, timebase registers | [เปิด](labs/Lab10_PWM_Motor/REGISTER_GUIDE.md) |

## Base address ที่ใช้บ่อย

| Block | Base address |
|---|---:|
| GPIOA / GPIOB / GPIOC | `0x40020000` / `0x40020400` / `0x40020800` |
| RCC | `0x40023800` |
| TIM5 / USART2 / I2C1 | `0x40000C00` / `0x40004400` / `0x40005400` |
| TIM1 / ADC1 / SYSCFG / EXTI | `0x40010000` / `0x40012000` / `0x40013800` / `0x40013C00` |
| SysTick / NVIC ISER / NVIC IPR | `0xE000E010` / `0xE000E100` / `0xE000E400` |

## กฎการแก้ Register โดยไม่ชนกับ HAL

- ใช้ HAL สำหรับลำดับ initialization และ protocol state machine ตามที่ CubeMX สร้าง
- อ่าน register เพื่อเรียนรู้และ debug ได้ตลอด
- ถ้าจะเขียน register เอง ให้หยุด peripheral ก่อนและรู้ว่า HAL อาจเขียนทับค่าในครั้งถัดไป
- ใช้ `BSRR` เมื่อต้อง set/reset GPIO แบบ atomic; การ toggle ด้วยการอ่าน `ODR` แล้วเขียนกลับไม่ atomic
- Flag หลายตัวมีวิธี clear เฉพาะ ห้ามเดาว่าเขียน 0 หรือ 1 แล้วจะล้างได้ ต้องตรวจ Reference Manual
- ค่าใน SFRs ขณะ CPU วิ่งอาจเปลี่ยนตลอด ให้ Pause ที่ตำแหน่งเดิมก่อนเปรียบเทียบ

เอกสารอ้างอิงหลัก: STM32F410 Reference Manual RM0401, datasheet ของ STM32F410xB และ user manual/schematic ของ NUCLEO-F410RB
