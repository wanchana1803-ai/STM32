# Lab01 ฉบับลงมือ: LED ด้วย GPIO Register และ SysTick

## ขอบเขต

**สำหรับผู้ใช้ STM32CubeMX:** เริ่ม Lab ด้วยการตั้ง GPIO output ใน CubeMX และใช้ HAL timebase ของ generated project ก่อน จากนั้นจึงเรียนตัวอย่าง register/polling ด้านล่างในโปรเจกต์ทดลองแยก ตัวอย่างมี main ของตัวเอง จึงไม่ใช่โค้ดสำหรับวางทับ generated main โดยตรง เมื่อต้องการเพิ่มโค้ดในโปรเจกต์ CubeMX ให้ใช้ USER CODE blocks หรือไฟล์แยก และตรวจว่า generated initialization ไม่ตั้งค่าทับส่วนที่ฝึก

ตัวอย่างเพื่อการเรียนรู้สำหรับ STM32F410RB และ CMSIS device header `stm32f4xx.h` ต้องมี startup, linker script และ device define ที่ตรงกับ STM32F410Rx จากโปรเจกต์ที่เลือก MCU STM32F410RB ตรวจ Flash 128 KB และ RAM 32 KB ในการตั้งค่าโปรเจกต์ ไม่ใช่โปรเจกต์พร้อม build และยังไม่ได้ทดสอบบนบอร์ดจริง

สมมติว่า PA5 ว่างและต่อ LED แบบ active-high ผ่านตัวต้านทานไป GND ถ้า LED ของบอร์ดอยู่ขาอื่นหรือ active-low ให้ปรับตาม schematic ก่อนใช้ ขา PA5 ในภาพต้นฉบับไม่ใช่หลักฐาน pin mapping ของบอร์ดคุณ

เลือกโปรเจกต์ฝึกที่ให้โค้ดนี้ดูแล SysTick แต่ผู้เดียว ไม่เรียก HAL_Init/HAL_Delay และไม่ใช้ HAL timeout ที่อาศัย SysTick ขณะทดลองนี้ `SystemCoreClockUpdate()` อ่าน clock configuration ปัจจุบันเพื่อปรับตัวแปร ไม่ได้สั่งเปลี่ยน clock

## แนวคิดก่อนเขียน

| สิ่งที่ต้องทำ | รีจิสเตอร์ | เหตุผล |
|---|---|---|
| เปิด clock GPIOA | RCC_AHB1ENR.GPIOAEN | ให้ peripheral รับ clock |
| กำหนดค่าขาเริ่มต้น LOW | GPIOA_BSRR bit 21 | reset output bit 5 |
| Push-pull | GPIOA_OTYPER bit 5 = 0 | ขับ HIGH และ LOW |
| Low speed | GPIOA_OSPEEDR[11:10] = 00 | เพียงพอสำหรับ LED |
| ไม่ใช้ pull | GPIOA_PUPDR[11:10] = 00 | output ไม่ต้องใช้ pull ในวงจรนี้ |
| Output | GPIOA_MODER[11:10] = 01 | เชื่อม output driver กับขา |
| ตั้งเวลารอบละ 1 ms | SysTick LOAD/VAL/CTRL | วนตรวจ COUNTFLAG |

อ้างอิง GPIO จาก RM0401 หน้า 119 และ 150–153 รายละเอียด SysTick ใช้หัวข้อ §11.4 ของหนังสือประกอบ และคู่มือ core หากต้องตรวจทุกบิต

## โค้ดตัวอย่าง

```c
#include "stm32f4xx.h"
#include <stdint.h>

#define LED_PIN  5U
#define LED_MASK (1UL << LED_PIN)

static void led_init(void)
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    (void)RCC->AHB1ENR;  // read back after clock enable

    GPIOA->BSRR = LED_MASK << 16U;
    GPIOA->OTYPER &= ~LED_MASK;
    GPIOA->OSPEEDR &= ~(3UL << (2U * LED_PIN));
    GPIOA->PUPDR &= ~(3UL << (2U * LED_PIN));
    GPIOA->MODER =
        (GPIOA->MODER & ~(3UL << (2U * LED_PIN))) |
        (1UL << (2U * LED_PIN));
}

static int systick_poll_init(void)
{
    SystemCoreClockUpdate();
    uint32_t ticks = SystemCoreClock / 1000U;
    if (ticks == 0U || (ticks - 1U) > SysTick_LOAD_RELOAD_Msk) {
        return 0;
    }
    SysTick->CTRL = 0U;
    SysTick->LOAD = ticks - 1U;
    SysTick->VAL = 0U;
    SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk |
                    SysTick_CTRL_ENABLE_Msk; // TICKINT remains 0
    return 1;
}

static void delay_ms(uint32_t ms)
{
    while (ms > 0U) {
        SysTick->VAL = 0U;
        while ((SysTick->CTRL & SysTick_CTRL_COUNTFLAG_Msk) == 0U) {
            // Busy wait: CPU cannot do useful main-loop work here.
        }
        --ms;
    }
}

int main(void)
{
    led_init();
    if (!systick_poll_init()) {
        while (1) { }
    }
    while (1) {
        GPIOA->BSRR = LED_MASK;
        delay_ms(500U);
        GPIOA->BSRR = LED_MASK << 16U;
        delay_ms(500U);
    }
}
```

`BSRR` บิต 0–15 ใช้ set ส่วน 16–31 ใช้ reset จึงเขียน `=` โดยตรง ไม่ใช้ `|=` กับรีจิสเตอร์คำสั่งนี้ ในตัวอย่างขา 5 จึง reset ด้วยบิต 21

การอ่าน CTRL มีผลต่อ COUNTFLAG และการเขียน VAL จะล้างค่าตัวนับ/COUNTFLAG ตามพฤติกรรม SysTick จึงไม่ควรเปิด debugger view ที่อ่าน CTRL ต่อเนื่องระหว่างทดสอบ polling ตัวแปร SystemCoreClock ต้องสอดคล้องกับ clock จริงด้วย

Delay นี้เป็น busy wait และมี software overhead ทุก ms เหมาะกับบทเริ่มต้น ไม่เหมาะเป็น scheduler หรือเครื่องมือวัดเวลาความแม่นยำสูง เมื่อมี interrupt อื่นกินเวลานาน polling อาจนับรอบที่ผ่านไปไม่ครบ บทต่อไปให้เปลี่ยนเป็น timebase เดินต่อเนื่องกับการตรวจ elapsed time

## ลำดับทดลองและเกณฑ์ผ่าน

1. หยุดหลัง led_init ตรวจ GPIOA clock และ MODER[11:10] ต้องเป็น 01
2. ทดลอง set/reset ด้วย BSRR และตรวจขาจริง ถ้าไม่มีไฟให้ตรวจ polarity ตัวต้านทานและ schematic
3. ตรวจ SystemCoreClock: ถ้าเป็น 16,000,000 ค่า LOAD ต้องเป็น 15,999
4. Run โดยไม่ single-step วัดคาบ LED เป้าหมายประมาณ 1 s และบันทึกค่าจริงพร้อมวิธีวัด
5. เปลี่ยน delay เป็น 100 ms ทั้งสองช่วง คาบควรประมาณ 200 ms
6. อธิบายได้ว่าทำไม `1UL<<5` ใช้กับ ODR แต่ MODER ต้องเลื่อน `2×5`

| อาการ | สิ่งที่ควรตรวจ |
|---|---|
| LED ไม่ติด | pin mapping, active-low, GPIO clock, MODER, การต่อสาย |
| ค้างใน delay | ENABLE, clock source, clock configuration, มีโค้ดอื่นแก้ SysTick หรือไม่ |
| เวลาไม่ตรง | SystemCoreClock, LOAD, optimization ของโค้ดอื่น, การหยุดด้วย debugger |
| HAL_Delay ค้างหลังดัดแปลง | SysTick interrupt/timebase ของ HAL ถูกเปลี่ยนหรือปิดหรือไม่ |

## แบบฝึกพร้อมแนวตอบ

1. PA7 ใช้ MODER บิตใด? → [15:14]
2. ทำไม MODER ต้อง clear ก่อน set? → field อาจมีค่าเดิม 10 หรือ 11 การ OR อย่างเดียวไม่รับประกัน 01
3. ถ้าใช้ clock 84 MHz ที่ตรวจสอบแล้ว LOAD ต่อ 1 ms เป็นเท่าไร? → 83,999
4. TICKINT=0 แล้วยังนับเวลาได้หรือไม่? → ได้ โดยตรวจ COUNTFLAG แต่ไม่มี interrupt
5. ต้องการรับปุ่มระหว่าง LED รอ 500 ms ควรปรับอย่างไร? → ใช้เวลาสะสมแบบไม่บล็อกและให้ main ตรวจปุ่มทุก loop

งานส่ง: ผังวงจร, ค่า clock/LOAD, ภาพหรือบันทึกรีจิสเตอร์, ตารางค่าที่วัดสำหรับ delay 100 และ 500 ms และคำอธิบายโค้ดด้วยภาษาของตนเอง
