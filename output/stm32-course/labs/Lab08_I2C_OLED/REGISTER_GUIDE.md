# คู่มือ Register Lab08: I2C1 และ OLED

ตัวอย่างใช้ I2C1 ขาที่พบบ่อยคือ PB8/PB9 AF4 แต่ต้องยึด `.ioc` I2C ต้องใช้ alternate-function open-drain และ pull-up บน SDA/SCL

## Register ที่ใช้

| กลุ่ม | Register/ฟิลด์ | หน้าที่ |
|---|---|---|
| Clock | `RCC->AHB1ENR.GPIOBEN` | เปิด GPIOB |
| Clock | `RCC->APB1ENR.I2C1EN` | เปิด I2C1 |
| GPIO | `MODER=10`, `OTYPER=1`, `AFRx=4` | AF open-drain สำหรับ I2C1 |
| I2C | `CR1` | `PE`, START, STOP, ACK, software reset |
| I2C | `CR2` | ค่า PCLK1 เป็น MHz และ interrupt/DMA enable |
| I2C | `OAR1/OAR2` | own address เมื่อใช้ slave |
| I2C | `DR` | address/data byte |
| I2C | `SR1` | `SB`, `ADDR`, `BTF`, `RxNE`, `TxE`, error flags |
| I2C | `SR2` | `MSL`, `BUSY`, `TRA`; ใช้ในลำดับ clear ADDR |
| I2C | `CCR` | clock control สำหรับ Standard/Fast mode |
| I2C | `TRISE` | maximum rise-time setting |
| I2C | `FLTR` | analog/digital filter |

## ลำดับส่งแบบย่อ

`PE → START → SB → address → ADDR → data/TxE/BTF → STOP`

การ clear `ADDR` ต้องอ่าน `SR1` แล้วอ่าน `SR2` ตามลำดับ HAL จัดการ state machine นี้ให้ จึงควรดู register เพื่อ debug แต่ไม่อ่าน/เขียน `DR/SR` แทรกใน transaction ของ HAL

## ตรวจเมื่อ OLED ไม่ตอบ

1. ดู `BUSY`; ถ้าค้างให้ตรวจ pull-up, สาย, level และ STOP
2. ดู `AF` (acknowledge failure) เพื่อแยก address ผิด/อุปกรณ์ไม่อยู่
3. ยืนยัน address 7-bit กับรูปแบบที่ HAL API ต้องการ
4. ตรวจ `BERR`, `ARLO`, `OVR`, `TIMEOUT`
5. ACK ระดับ bus ไม่ยืนยันว่า command/data format ของ OLED ถูก

`CCR/TRISE/CR2.FREQ` ต้องสัมพันธ์กับ PCLK1; ใช้ CubeMX คำนวณและตรวจค่าหลัง init
