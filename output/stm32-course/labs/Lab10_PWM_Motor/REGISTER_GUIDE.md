# คู่มือ Register Lab10: PWM Motor, Direction และ Watchdog

Lab นี้รวม PWM จาก TIM1, GPIO ของ driver และ timebase สำหรับ command watchdog ชื่อขา EN/DIR/IN1/IN2 และ polarity ต้องยึด driver กับ `.ioc` ห้ามต่อมอเตอร์เข้าขา STM32 โดยตรง

## Register ที่ใช้

| ส่วน | Register | หน้าที่ |
|---|---|---|
| Clock | `RCC->AHB1ENR`, `APB2ENR` | เปิด GPIO และ TIM1 |
| Direction/enable | `GPIOx->MODER`, `OTYPER`, `PUPDR` | กำหนด output และ safe electrical state |
| Direction/enable | `GPIOx->BSRR`, `ODR` | set/reset แบบ atomic และตรวจ output latch |
| PWM pin | `GPIOx->MODER`, `AFRx` | ผูกขากับ TIM1 channel |
| PWM timing | `TIM1->PSC`, `ARR`, `CCR1` | ความถี่และ duty |
| PWM mode | `TIM1->CCMR1`, `CCER`, `CR1`, `EGR` | mode, polarity, enable, update |
| Advanced safety | `TIM1->BDTR` | `MOE`, break input, dead-time, lock |
| Periodic work | `TIMx->DIER/SR` หรือ SysTick | ramp และ timeout check |

รายละเอียดฟิลด์ PWM ใช้หลักเดียวกับ [Lab04](../Lab04_PWM/REGISTER_GUIDE.md) และรายละเอียด interrupt ใช้ [Lab07](../Lab07_Interrupt/REGISTER_GUIDE.md)

## Safe state ที่ต้องตรวจ

1. หลัง reset/init: `CCR1=0` หรือ output state ที่ driver หยุดแน่นอน และ GPIO direction/enable อยู่ safe state
2. ก่อน ARM: driver enable ยังปิด แม้ UART รับคำสั่ง duty
3. เมื่อ ARM: ตั้ง direction ก่อน enable/PWM ตาม datasheet driver
4. STOP/timeout: ตัด enable หรือ PWM ทันทีตาม safety design แล้ว reset ramp state
5. reconnect/reset: ไม่กลับไปใช้ duty เก่าโดยอัตโนมัติ

## BDTR ของ TIM1

`MOE` เป็น gate หลักของ output; `BKE/BKP` ตั้ง break input; `DTG` กำหนด dead time; `LOCK` จำกัดการแก้ configuration จน reset ค่าเหล่านี้มีประโยชน์เมื่อขับ half-bridge/complementary outputs แต่ต้องตั้งตาม power stage จริง

Firmware watchdog ในหลักสูตรคือการตรวจเวลาตั้งแต่ command/PING ล่าสุดด้วย SysTick หรือ timer แล้วสั่ง safe state เมื่อเกินกำหนด ไม่ใช่รีจิสเตอร์ watchdog ฮาร์ดแวร์ `IWDG` เว้นแต่จะเพิ่มเป็นส่วนขยาย

## สิ่งที่วัด

วัด PWM ที่ input ของ driverก่อนต่อโหลด ตรวจ 0/10/50/90/100%, polarity และ frequency จากนั้นทดสอบ STOP, lost link, reset และ direction change ด้วยแหล่งจ่ายที่จำกัดกระแส
