# คู่มือรีจิสเตอร์ Lab01: LED, GPIOA และ SysTick

คู่มือนี้อธิบายรีจิสเตอร์ที่เกี่ยวข้องกับการทดลอง LD2 บน NUCLEO-F410RB โดย LD2 เชื่อมกับ PA5 แบบ active-high การทดลองใช้ STM32CubeMX สร้าง initialization, STM32CubeIDE สำหรับ build/debug และตรวจค่าจริงด้วย SFRs/Expressions

ผลที่ตรวจได้จากบอร์ด:

```text
SystemCoreClock = 84,000,000 Hz
SysTick->LOAD   = 83,999
SysTick CTRL[2:0] = 0b111
GPIOA MODER5   = 0b01
GPIOA ODR5     = 0 หรือ 1 ตามสถานะ LD2
```

## 1. ภาพรวมเส้นทางการทำงาน

```text
RCC เปิด clock ให้ GPIOA
        ↓
GPIOA MODER/OTYPER/OSPEEDR/PUPDR กำหนดคุณสมบัติ PA5
        ↓
GPIOA BSRR หรือ ODR เปลี่ยนสถานะ output
        ↓
PA5 HIGH/LOW ทำให้ LD2 ติด/ดับ

Processor clock 84 MHz
        ↓
SysTick LOAD = 83,999
        ↓ ทุก 1 ms
SysTick exception → HAL_IncTick() → uwTick เพิ่ม 1
        ↓
HAL_GetTick() ใช้จัดเวลาเปลี่ยน LED
```

## 2. Memory-mapped registers และ CMSIS

Peripheral registers อยู่ใน memory map ของ MCU จึงอ่านหรือเขียนด้วย C pointer ได้ Device header สร้างชื่อให้ เช่น:

```c
RCC->AHB1ENR
GPIOA->MODER
GPIOA->BSRR
SysTick->LOAD
```

ชื่อเหล่านี้มีชนิด `volatile` เพื่อให้ compiler ทำการเข้าถึงฮาร์ดแวร์ตามที่โปรแกรมระบุ แต่ `volatile` ไม่ได้ทำให้คำสั่ง read-modify-write เป็น atomic

Base address และ offset ที่ใช้ใน Lab01:

| Block | Base address | Register | Offset | Address |
|---|---:|---|---:|---:|
| RCC | `0x40023800` | AHB1ENR | `0x30` | `0x40023830` |
| GPIOA | `0x40020000` | MODER | `0x00` | `0x40020000` |
| GPIOA | `0x40020000` | OTYPER | `0x04` | `0x40020004` |
| GPIOA | `0x40020000` | OSPEEDR | `0x08` | `0x40020008` |
| GPIOA | `0x40020000` | PUPDR | `0x0C` | `0x4002000C` |
| GPIOA | `0x40020000` | ODR | `0x14` | `0x40020014` |
| GPIOA | `0x40020000` | BSRR | `0x18` | `0x40020018` |
| SysTick | `0xE000E010` | CTRL | `0x00` | `0xE000E010` |
| SysTick | `0xE000E010` | LOAD | `0x04` | `0xE000E014` |
| SysTick | `0xE000E010` | VAL | `0x08` | `0xE000E018` |

อ้างอิง GPIO/RCC จาก RM0401 Rev 4 §5.3.8 และ §6.4 หน้าเอกสาร 119, 150–153 ส่วน SysTick เป็น peripheral ของ Cortex-M4 core ให้ใช้คู่มือ Cortex-M4/CMSIS ประกอบ

## 3. RCC_AHB1ENR: เปิด clock ให้ GPIOA

ชื่อเต็ม: RCC AHB1 peripheral clock enable register

```text
Bit 0 GPIOAEN
0 = GPIOA clock disabled
1 = GPIOA clock enabled
```

ก่อนเข้าถึง GPIOA ต้องเปิด clock:

```c
RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
(void)RCC->AHB1ENR;  // read-back ให้ clock enable เสร็จก่อนคำสั่งถัดไป
```

CubeMX สร้างการเปิด clockไว้ใน `MX_GPIO_Init()` ผ่าน macro ลักษณะนี้:

```c
__HAL_RCC_GPIOA_CLK_ENABLE();
```

ตรวจใน Expressions:

```c
(RCC->AHB1ENR >> 0) & 0x1U
```

ค่าที่คาดคือ `1`

ถ้า GPIOAEN เป็น 0 การอ่าน/เขียน GPIOA จะไม่ทำให้ขาทำงานตามต้องการ แม้ค่า configuration ใน source code จะดูถูกต้อง

## 4. GPIOA_MODER: เลือกโหมดของ PA5

MODER ใช้ 2 บิตต่อขา สูตรตำแหน่งเริ่มต้นของขา `n` คือ `2 × n`

```text
PA5 → 2 × 5 = bit 10
field กว้าง 2 บิต → MODER[11:10]
```

ความหมาย:

| MODER5[1:0] | Mode |
|---|---|
| `00` | Input |
| `01` | General-purpose output |
| `10` | Alternate function |
| `11` | Analog |

ตั้ง PA5 เป็น output โดย clear field ก่อน แล้วเขียน `01`:

```c
GPIOA->MODER =
    (GPIOA->MODER & ~(0x3UL << 10)) |
    (0x1UL << 10);
```

เหตุผลที่ต้อง clear ก่อน: หากค่าเดิมเป็น `10` หรือ `11` การ OR `01` อย่างเดียวจะไม่รับประกันว่าจะได้ `01`

อ่าน field:

```c
(GPIOA->MODER >> 10) & 0x3U
```

ค่าที่ตรวจได้คือ `1` หรือฐานสอง `01`

ใน SFRs CubeIDE อาจแสดง `MODER5 [10:2]` ซึ่งหมายถึง “เริ่มที่บิต 10 ขนาด 2 บิต” จึงตรงกับบิต `[11:10]` ใน Reference Manual

## 5. GPIOA_OTYPER: เลือก Push-pull/Open-drain

OTYPER ใช้ 1 บิตต่อขา:

```text
Bit 5 OT5
0 = Push-pull
1 = Open-drain
```

ตั้ง PA5 เป็น push-pull:

```c
GPIOA->OTYPER &= ~(1UL << 5);
```

อ่าน field:

```c
(GPIOA->OTYPER >> 5) & 0x1U
```

ค่าที่คาดคือ `0`

Push-pull ขับได้ทั้ง HIGH และ LOW เหมาะกับ LD2 บนบอร์ด ส่วน open-drain ต้องอาศัย pull-up และใช้กับงานอย่าง I2C หรือวงจรที่ออกแบบรองรับ

## 6. GPIOA_OSPEEDR: ความเร็วขอบสัญญาณ

OSPEEDR ใช้ 2 บิตต่อขา PA5 จึงใช้บิต `[11:10]`

| OSPEEDR5[1:0] | Output speed |
|---|---|
| `00` | Low |
| `01` | Medium |
| `10` | High |
| `11` | Very high |

ตั้ง Low speed:

```c
GPIOA->OSPEEDR &= ~(0x3UL << 10);
```

อ่าน field:

```c
(GPIOA->OSPEEDR >> 10) & 0x3U
```

ค่าที่คาดคือ `0`

Output speed ควบคุม slew rate/ความเร็วของขอบสัญญาณ ไม่ใช่ความถี่กระพริบ LED ความถี่กระพริบมาจาก timing ในโปรแกรม

## 7. GPIOA_PUPDR: ตัวต้านทานดึงระดับภายใน

PUPDR ใช้ 2 บิตต่อขา PA5 จึงใช้บิต `[11:10]`

| PUPDR5[1:0] | Pull configuration |
|---|---|
| `00` | No pull-up / pull-down |
| `01` | Pull-up |
| `10` | Pull-down |
| `11` | Reserved |

ตั้ง No pull:

```c
GPIOA->PUPDR &= ~(0x3UL << 10);
```

อ่าน field:

```c
(GPIOA->PUPDR >> 10) & 0x3U
```

ค่าที่คาดคือ `0`

Lab01 ใช้ output push-pull จึงไม่ต้องใช้ pull ภายใน สำหรับ input ใน Lab02 ต้องเลือก pull ให้สอดคล้องกับการต่อปุ่มจริง

## 8. GPIOA_ODR: Output Data Register

ODR ใช้ 1 บิตต่อขา:

```text
ODR5 = 0 → PA5 LOW  → LD2 ดับ
ODR5 = 1 → PA5 HIGH → LD2 ติด
```

อ่านค่า PA5:

```c
uint32_t led_level = (GPIOA->ODR >> 5) & 0x1U;
```

สลับค่า:

```c
GPIOA->ODR ^= (1UL << 5);
```

ตัวอย่างนี้เป็น read-modify-write:

```text
อ่าน ODR → XOR bit 5 → เขียน ODR ทั้ง word กลับ
```

หาก interrupt หรือส่วนอื่นเขียน ODR ระหว่างขั้นตอน อาจเกิด lost update ได้ จึงเหมาะสำหรับเรียนรู้และกรณีที่ ownership ชัดเจน แต่การ set/reset ขาเฉพาะควรใช้ BSRR

## 9. GPIOA_BSRR: Set/Reset แบบเจาะจงบิต

BSRR เป็นรีจิสเตอร์คำสั่งแบบ write-only:

```text
Bits 0–15   BSy: เขียน 1 เพื่อ set ODRy
Bits 16–31  BRy: เขียน 1 เพื่อ reset ODRy
```

สำหรับ PA5:

```c
GPIOA->BSRR = (1UL << 5);   // BS5: PA5 HIGH, LD2 ติด
GPIOA->BSRR = (1UL << 21);  // BR5: PA5 LOW,  LD2 ดับ
```

เพราะ reset position คือ:

```text
5 + 16 = 21
```

ใช้ `=` ไม่ใช้ `|=` เพราะ BSRR ไม่ใช่ storage register ที่ต้องเก็บค่าเดิม การอ่านกลับมักได้ศูนย์และการใช้ `|=` ทำ read-modify-write โดยไม่เกิดประโยชน์

หากเขียน set และ reset ของขาเดียวกันพร้อมกัน คู่มือ RM0401 ระบุว่า set มี priority แต่โปรแกรมปกติควรหลีกเลี่ยงคำสั่งกำกวมนี้

ตรวจผลของ BSRR จาก `ODR5` หรือสถานะขา ไม่ตรวจค่าค้างใน BSRR

## 10. SysTick_LOAD: กำหนดจำนวน clock ต่อหนึ่ง tick

SysTick เป็น down-counter 24 บิต ค่า LOAD ที่ใช้ได้อยู่ในช่วง `0x000000` ถึง `0xFFFFFF`

เมื่อใช้ processor clock และต้องการ tick 1 ms:

```text
LOAD = SystemCoreClock / 1000 - 1
```

ค่าจริงของการทดลอง:

```text
LOAD = 84,000,000 / 1,000 - 1
     = 83,999
```

ตรวจใน Expressions:

```c
SysTick->LOAD
```

หรือใช้เงื่อนไข:

```c
(SysTick->LOAD + 1U) == (SystemCoreClock / 1000U)
```

ผลควรเป็น `1`

เหตุผลที่ลบ 1: ตัวนับนับรวมค่าศูนย์ เช่น LOAD=3 ให้ลำดับ 3, 2, 1, 0 รวม 4 clock

## 11. SysTick_VAL: ค่าตัวนับปัจจุบัน

VAL แสดงค่าที่ SysTick กำลังนับถอยหลัง:

```text
LOAD → ... → 2 → 1 → 0 → โหลด LOAD ใหม่
```

ขณะ Pause ค่า VAL จะแตกต่างกันได้ทุกครั้ง เพราะหยุด MCU คนละจังหวะ การเขียนค่าใด ๆ ลง VAL จะล้าง current value และ COUNTFLAG จึงไม่ควรแก้จาก SFRs ระหว่างการทดลอง

```c
uint32_t current = SysTick->VAL;
```

ค่า VAL ใช้ดูพฤติกรรมตัวนับ แต่ Lab01 ใช้ `HAL_GetTick()` สำหรับเวลาระดับมิลลิวินาที ไม่ใช้ VAL วัดช่วงเวลายาวโดยตรง

## 12. SysTick_CTRL: เปิด counter, interrupt และเลือก clock

บิตสำคัญ:

| Bit | Name | ค่าในการทดลอง | ความหมาย |
|---:|---|---:|---|
| 0 | ENABLE | 1 | เปิดตัวนับ |
| 1 | TICKINT | 1 | ขอ SysTick exception เมื่อนับถึงศูนย์ |
| 2 | CLKSOURCE | 1 | ใช้ processor clock |
| 16 | COUNTFLAG | เปลี่ยนตามเหตุการณ์ | เป็น 1 เมื่อนับผ่านศูนย์หลังการอ่าน CTRL ครั้งก่อน |

อ่านสามบิตล่าง:

```c
SysTick->CTRL & 0x7U
```

ค่าที่ตรวจได้คือ `7` หรือฐานสอง `111`

อย่าอ่าน `CTRL` ซ้ำจาก debugger ระหว่างทดลอง polling COUNTFLAG เพราะการอ่าน CTRL มีผลล้าง COUNTFLAG และทำให้โปรแกรมพลาดเหตุการณ์ที่กำลังรอ

ในโปรเจกต์ HAL นี้ต้องคง TICKINT=1 เพราะ SysTick exception ใช้เพิ่ม `uwTick` ถ้าปิด interrupt แล้ว `HAL_GetTick()`, `HAL_Delay()` และ timeout หลายส่วนของ HAL จะหยุดเดิน

## 13. จาก SysTick ถึง HAL_GetTick

ลำดับการทำงานโดยย่อ:

```text
SysTick นับถึง 0
    ↓
SysTick_Handler()
    ↓
HAL_IncTick()
    ↓
uwTick เพิ่ม 1
    ↓
HAL_GetTick() คืนค่า uwTick
```

`SystemCoreClock` และ `uwTick` เป็นตัวแปรในซอฟต์แวร์ ไม่ใช่ hardware registers:

| ชื่อ | ประเภท | หน้าที่ |
|---|---|---|
| `SystemCoreClock` | ตัวแปร CMSIS | เก็บความถี่ core ที่ซอฟต์แวร์รับรู้ |
| `uwTick` | ตัวแปร HAL | นับจำนวน HAL ticks โดยทั่วไปหน่วย ms |
| `HAL_GetTick()` | ฟังก์ชัน HAL | อ่าน `uwTick` |

การตรวจ elapsed time แบบรองรับ unsigned wrap:

```c
uint32_t now = HAL_GetTick();

if ((uint32_t)(now - last_led_tick) >= 500U)
{
    last_led_tick = now;
    /* เปลี่ยน LED */
}
```

## 14. Shift และ mask สำหรับอ่าน field

สูตรทั่วไป:

```c
field = (register_value >> start_bit) & mask;
```

Mask สำหรับความกว้างต่าง ๆ:

| Width | Mask |
|---:|---:|
| 1 bit | `0x1U` |
| 2 bits | `0x3U` |
| 3 bits | `0x7U` |
| 4 bits | `0xFU` |

Expressions ที่ใช้ตรวจ Lab01:

```c
(RCC->AHB1ENR >> 0) & 0x1U
(GPIOA->MODER >> 10) & 0x3U
(GPIOA->OTYPER >> 5) & 0x1U
(GPIOA->OSPEEDR >> 10) & 0x3U
(GPIOA->PUPDR >> 10) & 0x3U
(GPIOA->ODR >> 5) & 0x1U
SysTick->LOAD
SysTick->VAL
SysTick->CTRL & 0x7U
```

## 15. โค้ด Register ฉบับรวมสำหรับ GPIOA PA5

ส่วนนี้แสดงการตั้งค่า GPIO ด้วย register ทั้งหมด ห้ามวางซ้ำหลัง `MX_GPIO_Init()` โดยไม่ตั้งใจ เพราะจะเกิดเจ้าของ configuration สองชุด เลือกใช้เป็นโปรเจกต์ทดลองแยกหรือแทน initialization ของ CubeMX อย่างชัดเจน

```c
#include "stm32f4xx.h"
#include <stdint.h>

#define LED_PIN   5U
#define LED_MASK  (1UL << LED_PIN)

static void led_register_init(void)
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    (void)RCC->AHB1ENR;

    /* Establish safe initial output level before enabling output mode. */
    GPIOA->BSRR = LED_MASK << 16U;

    GPIOA->OTYPER &= ~LED_MASK;
    GPIOA->OSPEEDR &= ~(0x3UL << (2U * LED_PIN));
    GPIOA->PUPDR &= ~(0x3UL << (2U * LED_PIN));
    GPIOA->MODER =
        (GPIOA->MODER & ~(0x3UL << (2U * LED_PIN))) |
        (0x1UL << (2U * LED_PIN));
}

static void led_on(void)
{
    GPIOA->BSRR = LED_MASK;
}

static void led_off(void)
{
    GPIOA->BSRR = LED_MASK << 16U;
}
```

## 16. รีจิสเตอร์ Clock ที่เกี่ยวข้องทางอ้อม

ผลการทดลองยืนยัน `SystemCoreClock = 84 MHz` แต่ยังไม่ได้ตรวจค่าภายใน `SystemClock_Config()` หรือไฟล์ `.ioc` ใน workspace นี้ จึงไม่ควรเดาค่า PLL divider/multiplier คู่มือ Lab01 ระบุเพียงบทบาทของรีจิสเตอร์ต่อไปนี้:

| Register | บทบาท |
|---|---|
| `RCC_CR` | เปิด/ตรวจพร้อมของ HSI, HSE และ PLL |
| `RCC_PLLCFGR` | กำหนด PLL source และตัวหาร/ตัวคูณ |
| `RCC_CFGR` | เลือก system clock และ AHB/APB prescalers |
| `FLASH_ACR` | กำหนด Flash latency/cache/prefetch ให้เหมาะกับ clock |
| `PWR_CR` | กำหนด voltage scaling ที่รองรับความถี่เป้าหมาย |

หากต้องทำคู่มือ Clock Tree แบบลงค่าจริง ให้เปิด `SystemClock_Config()` และ `.ioc` แล้วบันทึก HSI/HSE, PLLM, PLLN, PLLP, SYSCLK, HCLK, PCLK1, PCLK2, Flash latency และ voltage scale ก่อนคำนวณ ค่า 84 MHz เพียงค่าเดียวไม่พอจะระบุว่าตั้ง PLL ด้วยชุดใด

## 17. ตารางสรุปรีจิสเตอร์ที่ต้องจำ

| Register | Field ที่ใช้ | ค่าของ Lab01 | หน้าที่ |
|---|---|---:|---|
| `RCC_AHB1ENR` | GPIOAEN bit 0 | 1 | เปิด clock GPIOA |
| `GPIOA_MODER` | MODER5 bits 11:10 | `01` | PA5 output |
| `GPIOA_OTYPER` | OT5 bit 5 | 0 | Push-pull |
| `GPIOA_OSPEEDR` | OSPEEDR5 bits 11:10 | `00` | Low speed |
| `GPIOA_PUPDR` | PUPDR5 bits 11:10 | `00` | No pull |
| `GPIOA_ODR` | ODR5 bit 5 | 0/1 | Output latch LOW/HIGH |
| `GPIOA_BSRR` | BS5/BR5 bits 5/21 | write 1 | Set/reset PA5 |
| `SysTick_LOAD` | RELOAD bits 23:0 | 83,999 | 84,000 clocks/tick |
| `SysTick_VAL` | CURRENT bits 23:0 | เปลี่ยนตลอด | Current down-counter |
| `SysTick_CTRL` | bits 2:0 | `111` | Enable/interrupt/core clock |

## 18. ข้อผิดพลาดที่พบบ่อย

| อาการ | จุดที่ควรตรวจ |
|---|---|
| LED ไม่ติด | GPIOAEN, MODER5, ODR5, polarity และการเลือก PA5 |
| ค่า MODER ดูไม่ตรง | CubeIDE `[10:2]` หมายถึง start=10, width=2 |
| BSRR อ่านเป็น 0 | ปกติ เพราะเป็น write-only command register ให้ดู ODR5 |
| OSPEEDR/PUPDR ค่าเต็มไม่เป็น 0 | ค่าเต็มรวมขาอื่น ให้ mask เฉพาะ field ของ PA5 |
| LED กระพริบแต่เวลาไม่ตรง | SystemCoreClock, LOAD, HAL timebase และวิธีวัด |
| HAL_Delay/HAL_GetTick หยุด | SysTick ENABLE/TICKINT หรือ handler/timebase ถูกเปลี่ยน |
| ใช้ ODR แล้วขาอื่นเปลี่ยนผิด | ตรวจ mask และปัญหา read-modify-write; ใช้ BSRR สำหรับ set/reset |

## 19. คำถามทบทวน

1. ทำไม MODER5 อยู่บิต `[11:10]`? เพราะแต่ละขาใช้ 2 บิต และ PA5 เริ่มที่ `2 × 5 = 10`
2. ทำไมอ่าน MODER5 ต้อง mask `0x3U`? เพราะ field กว้าง 2 บิต
3. ทำไม ODR5 ใช้ mask `0x1U`? เพราะ field กว้าง 1 บิต
4. ทำไม reset PA5 ใน BSRR ใช้บิต 21? เพราะ reset half เริ่มบิต 16 จึงเป็น `16 + 5`
5. ทำไม LOAD เป็น 83,999 ไม่ใช่ 84,000? เพราะ SysTick นับรวมศูนย์
6. ถ้าปิด TICKINT จะเกิดอะไร? Counter ยังนับได้ถ้า ENABLE เปิด แต่ HAL tick interrupt ไม่เพิ่ม `uwTick`
7. `SystemCoreClock` เป็น register หรือไม่? ไม่ เป็นตัวแปร CMSIS ที่ต้องตรงกับ clock จริง
8. ทำไมไม่อ่าน BSRR เพื่อดูสถานะ LED? เพราะ BSRR เป็นคำสั่งเขียน ให้ดู ODR หรือขาจริง

## 20. ขอบเขตและแหล่งอ้างอิง

- RM0401 Rev 4: RCC §5.3.8 และ GPIO §6.4
- STM32F410x8/B Datasheet DS11144 Rev 8: pinout/electrical characteristics
- UM1724 Nucleo-64 board manual: LD2/PA5 และ active-high
- CMSIS Cortex-M4 definitions: SysTick register layout

คู่มือนี้บันทึกเฉพาะสิ่งที่ใช้และตรวจใน Lab01 ค่า clock configuration เชิงลึกต้องอ้าง `.ioc` และ generated source ของโปรเจกต์จริงก่อนระบุค่าเฉพาะ
