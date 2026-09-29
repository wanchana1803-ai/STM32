# คู่มือ Register Lab03: UART/USART2

ตัวอย่างบทเรียนใช้ `USART2` ซึ่ง NUCLEO มักต่อกับ ST-LINK Virtual COM Port ผ่าน PA2/PA3 AF7 ให้ยืนยันจาก `.ioc` และ solder bridge ของบอร์ด

## Register ที่ใช้

| กลุ่ม | Register/ฟิลด์ | หน้าที่ |
|---|---|---|
| Clock | `RCC->AHB1ENR.GPIOAEN` | เปิด clock GPIO |
| Clock | `RCC->APB1ENR.USART2EN` | เปิด clock USART2 |
| GPIO | `MODER2/3=10` | เลือก Alternate Function |
| GPIO | `AFRL2/3=7` | ผูก PA2/PA3 กับ AF7 |
| GPIO | `OSPEEDR`, `PUPDR` | slew rate และ pull ตาม CubeMX |
| USART | `SR` | flag `TXE`, `TC`, `RXNE`, `ORE`, `FE`, `NE`, `PE` |
| USART | `DR[8:0]` | ข้อมูลรับ/ส่ง |
| USART | `BRR` | ตัวหาร baud จาก PCLK1 |
| USART | `CR1` | `UE`, `TE`, `RE`, word length, parity, interrupt enable |
| USART | `CR2` | stop bits (`STOP`) |
| USART | `CR3` | flow control, DMA, error interrupt |

## ลำดับ transmit/receive แบบ register

- ส่ง: รอ `SR.TXE=1` → เขียน `DR` → ถ้าต้องการรู้ว่าส่งออกจากเส้นแล้วให้รอ `SR.TC=1`
- รับ: เมื่อ `SR.RXNE=1` ให้อ่าน `DR`
- Overrun: `ORE=1` หมายถึง byte ใหม่มาแต่ byte เก่ายังไม่ถูกอ่าน; วิธี clear ต้องทำตามลำดับอ่าน `SR` แล้วอ่าน `DR`

HAL ทำลำดับนี้ให้ใน polling/interrupt/DMA จึงไม่ควรแทรกการอ่าน `DR` เองระหว่างที่ HAL กำลังรับข้อมูล เพราะจะขโมย byte จาก state machine

## ตรวจค่า

```c
(USART2->CR1 >> 13U) & 0x1U  // UE
(USART2->CR1 >> 3U)  & 0x1U  // TE
(USART2->CR1 >> 2U)  & 0x1U  // RE
(USART2->SR  >> 7U)  & 0x1U  // TXE
(USART2->SR  >> 5U)  & 0x1U  // RXNE
```

`BRR` ต้องตีความร่วมกับ PCLK1 และ `CR1.OVER8`; อย่าเทียบกับค่าคงที่โดยไม่รู้ clock tree

## สิ่งที่ต้องพิสูจน์

ตรวจ baud/data/stop/parity ใน CubeMX, ส่ง `HELLO\n`, ดู `TXE/TC`, รับ frame ที่แบ่งหลายช่วง และทดสอบว่า `ORE/FE` ไม่ทำให้ parser ค้างถาวร
