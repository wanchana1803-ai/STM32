from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MCU = ROOT / 'output/stm32-course'
GUI = ROOT / 'Antigravity-Tkinter'

# Each record adds CubeMX-specific instruction to the existing conceptual lesson.
records = [
dict(n=1, slug='LED', title='LED และ SysTick',
 cfg='เลือกขา LED ที่ตรวจแล้วเป็น GPIO_Output และ User Label เป็น LED; Output Push Pull, No Pull, Low speed; กำหนด initial level ตาม polarity เพื่อให้เริ่มดับ ตั้ง SYS Debug เป็น Serial Wire เพื่อคงขา debug ไว้ ตรวจ clock และคง HAL timebase เดิม',
 reg='RCC AHB1ENR เปิด GPIO clock; MODER เลือก output; OTYPER/PUPDR/OSPEEDR กำหนดลักษณะขา; ODR/BSRR เขียนค่า output',
 code='''/* USER CODE BEGIN 2: after generated initialization */
uint32_t last_led = HAL_GetTick();
/* USER CODE BEGIN 3: inside while (1) */
uint32_t now = HAL_GetTick();
if ((uint32_t)(now - last_led) >= 500U) {
    last_led = now;
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}''',
 steps=['สร้างโปรเจกต์ CubeMX ตั้ง LED label และ Generate จากนั้น build โปรแกรมเดิมให้ผ่านก่อนเพิ่มโค้ด', 'เพิ่มตัวแปรและโค้ดตามตำแหน่ง USER CODE ที่ระบุ ตรวจ LED สลับทุกประมาณ 500 ms', 'เปลี่ยนเป็น 100 และ 1000 ms บันทึกคาบเต็มซึ่งเป็นสองเท่าของช่วง toggle', 'อ่านค่า register หลัง MX_GPIO_Init และอธิบายเทียบกับค่าที่ตั้งใน CubeMX', 'เมื่อผ่าน HAL แล้วค่อยทำบท SysTick polling แยกตาม LAB01_LED_SYSTICK.md'],
 pseudo='init GPIO/timebase → จำเวลา → วนอ่านเวลา → ถ้าครบ interval ให้ toggle และจำเวลาใหม่ → ทำงานอื่นต่อ',
 tests=['เริ่มต้นขาตรงกับ initial level ที่ตั้งและ LED ไม่กลับ polarity ผิด', '100/500/1000 ms ให้คาบประมาณ 200/1000/2000 ms โดยระบุเครื่องมือและความคลาดเคลื่อน', 'เพิ่มการอ่านปุ่มหรือ counter ใน main แล้วไม่ติดค้างจาก delay'],
 issues='LED ไม่ติด: ตรวจขา/polarity/clock; เวลาเพี้ยน: ตรวจ clock/timebase; regenerate แล้วโค้ดหาย: ตรวจ USER CODE blocks',
 summary='GPIO กำหนดระดับขา ส่วน timebase กำหนดเวลา การใช้ elapsed time ทำให้ main ทำงานอื่นได้ BSRR ใช้ set/reset เฉพาะบิต ส่วน toggle ต้องระวังผู้เขียนขาร่วมกัน',
 gui_goal='สร้างหน้าต่างควบคุม LED แบบ mock และแยกค่าที่ขอออกจากค่าที่อุปกรณ์ยืนยัน',
 widgets='ttk.Frame, Label, Button, StringVar และ Canvas วงกลมสถานะ',
 gui_steps=['วาดปุ่ม ON/OFF และป้าย MOCK, DISCONNECTED, confirmed=UNKNOWN', 'สร้าง callback ที่สร้าง CMD LED แล้วตั้ง pending โดยไม่แก้ confirmed ทันที', 'mock transport รับคำสั่งแล้วใช้ after จำลอง ACK หลัง 100 ms; ใช้ session/id ตาม protocol', 'เมื่อ ACK ตรง id จึงเปลี่ยนวงกลมและ confirmed; ถ้า timeout ให้ UNKNOWN', 'หลัง Lab03 เปลี่ยน transport เป็น Serial โดยไม่เปลี่ยน view'],
 gui_code='''pending_id = 2
status.set("กำลังรอยืนยัน")
# Call from a main-thread event handler after parsing a matching ACK:
def show_led_ack(value):
    confirmed.set("ON" if value == 1 else "OFF")
    status.set("ยืนยันแล้ว")''',
 gui_tests=['กด ON ได้ pending ก่อน confirmed ON', 'mock ไม่ตอบต้องขึ้น timeout ไม่ขึ้นสำเร็จ', 'ACK id เก่าไม่เปลี่ยนสถานะคำสั่งปัจจุบัน'],
 gui_summary='Tkinter callback สร้างคำสั่ง ส่วน ACK ยืนยัน state การเปลี่ยนสีปุ่มอย่างเดียวไม่พิสูจน์ว่า LED บนบอร์ดติด',
 exercise='ถ้าได้รับ ACK ของคำสั่ง OFF หลังคำสั่ง ON ล่าสุดควรทำอย่างไร?', answer='เทียบ session/id กับ pending และไม่ใช้ ACK เก่าอัปเดตคำสั่งล่าสุด'),
dict(n=2, slug='Button', title='Button และ Debounce',
 cfg='เลือก input pin ที่ว่างและตั้ง User Label เป็น BUTTON; ตัวอย่างนี้ปุ่มต่อ GND จึงใช้ Pull-up และ active-low ใช้ GPIO_Input ก่อน EXTI ขา LED ใช้ค่าจาก Lab01',
 reg='GPIO IDR อ่านค่าขา; PUPDR เลือก pull-up; MODER=00 เลือก input; debounce เป็น logic เวลาใน application',
 code='''/* USER CODE BEGIN 2 */
GPIO_PinState raw_prev = HAL_GPIO_ReadPin(BUTTON_GPIO_Port, BUTTON_Pin);
GPIO_PinState stable = raw_prev;
uint32_t changed_at = HAL_GetTick(), presses = 0;
/* USER CODE BEGIN 3 */
uint32_t now = HAL_GetTick();
GPIO_PinState raw = HAL_GPIO_ReadPin(BUTTON_GPIO_Port, BUTTON_Pin);
if (raw != raw_prev) { raw_prev = raw; changed_at = now; }
if (raw != stable && (uint32_t)(now - changed_at) >= 20U) {
    stable = raw;
    if (stable == GPIO_PIN_RESET) { ++presses; }
}''',
 steps=['ต่อปุ่ม GND และเปิด pull-up ตามวงจรที่ตรวจจริง', 'ดู raw ใน debugger ตอนปล่อย/กดก่อนเพิ่ม debounce', 'เพิ่มโค้ดกรอง stable 20 ms และดู presses', 'ทดสอบกดค้างและกดติดกันแล้วปรับ debounce ตามผลจริง', 'หลัง Lab03 ให้ main ส่ง BUTTON event เฉพาะเมื่อ stable เปลี่ยน ไม่ส่งทุก loop'],
 pseudo='raw เปลี่ยน → จำเวลา → รอ stable ครบ debounce → ยอมรับ state → นับเฉพาะขอบกด',
 tests=['กด 20 ครั้งต้องเพิ่ม 20 ไม่เพิ่มซ้ำตอนค้าง', 'เปิดเครื่องพร้อมกดค้าง: ไม่ถือเป็นขอบกดใหม่ในตัวอย่างนี้จนปล่อยและกดอีกครั้ง', 'ทดลองกดเร็วกว่า debounce แล้วอธิบายเหตุการณ์ที่ถูกกรอง'],
 issues='ค่าลอย: ตรวจ pull/GND; นับซ้ำ: นับระดับแทน edge; ไม่ตอบกดเร็ว: debounce ยาวเกิน',
 summary='ปุ่มให้ระดับสัญญาณ แต่โปรแกรมต้องสร้างเหตุการณ์จากขอบ Debounce ลดผลหน้าสัมผัสเด้ง โดยแลกกับเวลาในการตอบสนอง',
 gui_goal='แสดงสถานะและจำนวนกดที่ firmware ยืนยัน โดยไม่เดานับจากอัตรา refresh ของจอ',
 widgets='Label แสดง PRESSED/RELEASED, counter, event list และป้ายเวลาข้อมูลล่าสุด',
 gui_steps=['ทำ mock ส่ง BUTTON state/count ตามชุดเหตุการณ์ที่กำหนดไว้', 'แสดง count ที่ firmware ส่ง ไม่เพิ่มเองทุกครั้งที่ GUI refresh', 'เพิ่มเวลา received และป้าย stale เมื่อหยุดส่งเกินค่าตั้ง', 'ทดสอบ raw bounce ใน mock firmware แล้วให้ GUI รับเฉพาะ stable event', 'เชื่อมจริงและเทียบจำนวนกดกับการสังเกต 20 ครั้ง'],
 gui_code='''def render_button(state, count):
    if state not in (0, 1) or count < 0:
        raise ValueError("invalid button event")
    state_text.set("PRESSED" if state else "RELEASED")
    count_text.set(str(count))''',
 gui_tests=['ส่ง event เดิมซ้ำแล้ว count ไม่เพิ่มเอง', 'กดค้างแสดง state ค้างแต่ไม่เพิ่ม count', 'หยุด telemetry แล้วแสดง stale'],
 gui_summary='GUI ใช้ stable state และ counter จาก firmware แยกเวลาได้รับข้อมูลจากเวลาเกิดเหตุการณ์ การแสดงซ้ำไม่ใช่การกดใหม่',
 exercise='เหตุใดไม่ควรนับจำนวนกดจากจำนวนข้อความที่รับ?', answer='ข้อความอาจซ้ำ/หายและมี state refresh ต้องใช้ counter หรือ event identity ที่ firmware ส่ง'),
dict(n=3, slug='UART', title='UART และ Serial Protocol',
 cfg='เลือก USART ที่ขา TX/RX ไม่ชนอุปกรณ์อื่น ตั้ง Asynchronous, 115200, 8 data bits, no parity, 1 stop bit, no flow control ตรวจ AF และ bus clock เปิด NVIC ของ USART เมื่อพัฒนา interrupt reception',
 reg='RCC เปิด USART clock; GPIO AFR/MODER เลือก AF; USART BRR กำหนด baud; CR1 เปิด transmitter/receiver; SR/DR ใช้ status/data ตาม RM0401',
 code='''/* USER CODE BEGIN 2; replace huart2 with generated handle */
static const uint8_t greeting[] = "STM32 ready\\n";
HAL_StatusTypeDef result = HAL_UART_Transmit(
    &huart2, (uint8_t *)greeting, sizeof greeting - 1U, 100U);
if (result != HAL_OK) { Error_Handler(); }
/* Greeting is a bring-up test, not a protocol ACK. */''',
 steps=['เชื่อม TX/RX ไขว้และ GND ด้วย interface ที่เข้ากันได้ ปิด serial monitor อื่นก่อนเปิดพอร์ต', 'ส่ง greeting ครั้งเดียวและตรวจตัวอักษรใน terminal', 'ทำ receive ring buffer แบบมีขอบเขตใน ISR และ parse line ใน main; ห้าม parse/printf ยาวใน ISR', 'ใช้ LF จบ frame และเก็บ partial line; ถ้าเกิน 128 bytes ทิ้งจน LF', 'ทำ HELLO/PING/ACK/ERR ก่อน operation ของ Lab อื่นตาม protocol.md', 'ทดสอบสายหลุดและ UART error แล้วกำหนดวิธี reset/re-arm receive ที่ตรวจได้'],
 pseudo='ISR รับ byte เข้า ring buffer → main ประกอบ line → validate session/id/op/args → execute → enqueue ACK/ERR → TX เมื่อพร้อม',
 tests=['HELLO และ PING ได้ ACK ตรง session/id', 'แบ่ง frame หลายส่วนและส่งหลาย frame พร้อมกันได้ผลเท่ากัน', 'frame ยาว/เลขผิด/op ไม่รองรับไม่ล้น bufferและรับ frame ดีถัดไปได้'],
 issues='อักขระเพี้ยน: baud/clock; ไม่มีข้อมูล: TX-RX/GND/AF/port; รับครั้งเดียว: ไม่ re-arm interrupt; GUI เปิด port ไม่ได้: มีโปรแกรมอื่นครอบครอง',
 summary='UART เป็น byte stream ไม่ได้แบ่งข้อความให้อัตโนมัติ ต้องออกแบบ framing, buffer, validation และ error recovery ก่อนเชื่อม GUI',
 gui_goal='สร้าง transport Serial และ parser ที่ทดสอบได้โดยไม่มีหน้าต่าง',
 widgets='Combobox รายชื่อพอร์ต, baud display, Connect/Disconnect, Text log จำกัดขนาด',
 gui_steps=['ใช้ serial.tools.list_ports.comports แสดงพอร์ตและให้เลือกเอง ไม่ hardcode COM3', 'ให้ worker เปิด Serial(timeout=0.1, write_timeout=0.2) และเป็นเจ้าของทั้ง read/write', 'worker รับคำสั่งผ่าน bounded queue อ่าน bytes แล้วแยก LF ด้วย buffer มีขอบเขต', 'ส่ง parsed event เข้า queue; UI ใช้ after ดึงทีละ batch โดยไม่แตะ widget จาก worker', 'Connect ทำ HELLO; Disconnect ปิด session และ pending; ปิดหน้าต่างคืนพอร์ต', 'ตรวจตาม protocol ทั้ง ACK/ERR และ frame ผิดก่อนเชื่อม Lab อื่น'],
 gui_code='''import queue
events = queue.Queue(maxsize=200)

def poll_events():
    for _ in range(50):
        try:
            event = events.get_nowait()
        except queue.Empty:
            break
        handle_event(event)  # Parse/validate earlier; render here.
    root.after(20, poll_events)
''',
 gui_tests=['partial/multiple/oversized frames กู้คืนได้', 'พอร์ตไม่อยู่/ถูกใช้แสดง error และ UI ยังปิดได้', 'connect-disconnect 10 ครั้งไม่มี worker หรือพอร์ตค้าง'],
 gui_summary='แยก transport/parser/UI และใช้ queue เป็นขอบเขต thread timeout ช่วยให้ shutdown ได้ แต่ไม่ใช่ตัวจบ frame',
 exercise='read timeout คืน b"ACK,ab" มาแล้วควร parse ทันทีหรือไม่?', answer='ไม่ เก็บ bytes ต่อจนเจอ LF หรือเกินขอบเขต ห้ามตีความ timeout เป็นจบ frame'),
dict(n=4, slug='PWM', title='PWM ควบคุม Duty',
 cfg='เลือก timer/channel ที่มี AF pin ว่าง ตั้ง Internal Clock, upcount, PWM Generation CHx และ PWM mode 1, active-high ตัวอย่าง f_TIM=16 MHz ใช้ PSC=15 ARR=999 Pulse=0 ได้ 1 kHz เปิด preload ตามที่จำเป็นและตรวจ pin output',
 reg='TIM PSC/ARR คุมความถี่; CCRx คุม compare; CCMRx เลือก PWM; CCER เปิด channel; CR1 เปิด timer; TIM1 ต้องเปิด BDTR.MOE',
 code='''/* USER CODE BEGIN 2: example TIM1 CH1, adapt to .ioc */
if (HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1) != HAL_OK) {
    Error_Handler();
}
/* ARR=999 in this example; 250/1000 = 25% */
__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 250U);''',
 steps=['คำนวณ f_TIM จาก clock tree ไม่ใช้ SYSCLK แทนโดยไม่ตรวจ', 'เริ่ม PWM 0% แล้วทดลอง 10/50/90% กับ LED', 'วัด period/high time และเทียบสูตร', 'เขียน function รับ percent ตรวจ 0–100 แล้วแปลง CCR โดยไม่ล้น', 'รับ operation PWM จาก UART และ ACK ค่าที่ใช้จริงหลังตรวจช่วง'],
 pseudo='validate percent → CCR=(ARR+1)×percent/100 → เขียน preload → timer latch ตาม update → ACK accepted duty',
 tests=['10/50/90% คงความถี่ 1 kHz ตาม clock สมมติ', 'ค่า -1/101 ถูกปฏิเสธ ไม่ wrap', '0/100% ให้ระดับปลายช่วงถูกต้องและ CCR อยู่ในช่วง register'],
 issues='ไม่มี output: channel/AF/MOE; duty ไม่ตรง: ARR+1 หรือ polarity; สะดุดเมื่อปรับ: preload/update timing',
 summary='PWM แยกความถี่ออกจาก duty ค่า compare มีความหมายตาม counting mode และ polarity จึงต้องวัดที่ขาจริง',
 gui_goal='สร้าง slider ที่ไม่ยิงคำสั่งถี่เกินและแสดง requested/applied แยกกัน',
 widgets='ttk.Scale, Spinbox, Label percent, ป้าย pending/error',
 gui_steps=['สร้างค่ากลาง duty 0–100 และ validate ช่องกรอก', 'slider เปลี่ยนเฉพาะ requested แล้ว debounce ก่อนส่ง 100 ms', 'ถ้ามีคำสั่ง pending เก็บเพียงค่าล่าสุดหนึ่งค่า ไม่สะสมทุกตำแหน่ง', 'ACK ตรง id จึงแก้ applied; disconnect ให้ applied UNKNOWN', 'วัดสัญญาณจริงเทียบค่าที่ GUI แสดง'],
 gui_code='''scheduled = None
def on_slider(value):
    global scheduled
    duty = max(0, min(100, round(float(value))))
    requested.set(duty)
    if scheduled is not None:
        root.after_cancel(scheduled)
    scheduled = root.after(100, lambda: request_pwm(duty))
''',
 gui_tests=['ลากเร็วแล้ว queue ไม่โตไม่จำกัด', 'กรอกข้อความ/101 แล้วไม่ส่ง', 'ACK ช้าทำให้ requested ต่าง applied ได้โดย UI ไม่หลอก'],
 gui_summary='Slider เป็นแหล่งคำขอ ไม่ใช่ผลวัด ต้องจำกัดอัตราส่งและแสดงค่าที่ firmware ยืนยันแยกกัน',
 exercise='เหตุใดไม่ส่งทุกครั้งที่ slider callback ถูกเรียก?', answer='ทำให้ UART/command queue ล้นและ ACK ล่าช้า ควร debounce/coalesce ค่าล่าสุด'),
dict(n=5, slug='ADC', title='ADC วัดแรงดัน',
 cfg='เลือก ADC1 channel ที่ตรง analog pin ตั้ง 12-bit, right alignment, single conversion, software trigger และ sampling time เหมาะกับ source impedance ตรวจ ADC clock limit ใน datasheet ตั้ง GPIO analog/no pull',
 reg='ADC CR1/CR2 เลือก mode/start; SMPR เลือก sampling time; SQR เลือกลำดับ channel; SR/DR แสดงสถานะ/ผล',
 code='''/* In main/task context after ADC initialization; not ISR */
uint32_t raw = 0;
HAL_StatusTypeDef status = HAL_ADC_Start(&hadc1);
if (status == HAL_OK) {
    status = HAL_ADC_PollForConversion(&hadc1, 10U);
    if (status == HAL_OK) { raw = HAL_ADC_GetValue(&hadc1); }
    HAL_ADC_Stop(&hadc1);
}
/* Use raw only when status == HAL_OK.
   millivolts = raw * measured_vref_mV / 4095U; */''',
 steps=['วัด VREF/ไฟ analog และตรวจขอบเขตแรงดันก่อนต่อ potentiometer', 'อ่าน raw ครั้งเดียวให้ผ่านก่อนเพิ่ม periodic sampling', 'ส่ง raw/millivolts ไม่เกิน 10 Hz เพื่อเริ่มเชื่อม GUI', 'เปรียบเทียบจุดต่ำ กลาง สูงกับมัลติมิเตอร์', 'เพิ่ม moving average และเปรียบเทียบ noise กับ response lag'],
 pseudo='ครบ sample interval → start ADC → รอแบบมี timeout → ถ้าสำเร็จแปลงหน่วย → publish; ถ้าผิดส่ง error ไม่ใช้ raw เก่าเป็นผลใหม่',
 tests=['raw อยู่ 0–4095; ค่ากลางประมาณครึ่ง full scale', 'timeout ไม่รายงาน raw=0 ว่าเป็นค่าที่วัดสำเร็จ', 'disconnect sensor แล้วไม่อ้างค่าที่ลอยเป็นแรงดันเชื่อถือได้'],
 issues='ค่านิ่ง 0: channel/pin/ground; noise: source/VREF/sample time; สเกลผิด: resolution/VREF',
 summary='ADC ให้ค่าดิจิทัลเทียบ reference การแปลงเป็นโวลต์ต้องรู้ VREF และความคลาดเคลื่อน การเฉลี่ยไม่แก้ calibration ผิด',
 gui_goal='แสดงตัวเลขและกราฟ bounded history พร้อม export CSV',
 widgets='Label raw/mV, Canvas graph, Pause/Resume, Export button',
 gui_steps=['รับ ADC telemetry และ validate raw กับหน่วย', 'เก็บข้อมูลไม่เกิน 600 samples ด้วย deque', 'วาดกราฟด้วย Canvas ทุก 100 ms แยกจากความถี่รับข้อมูล', 'Pause หยุดการแสดงผลตามนิยามที่ประกาศ ไม่อ้างว่าหยุด ADC บน MCU', 'Export ด้วย csv module มี timestamp, raw, millivolts, mode และบันทึก VREF ที่ใช้'],
 gui_code='''from collections import deque
samples = deque(maxlen=600)
def accept_adc(t_ms, raw, mv):
    if not (0 <= raw <= 4095 and mv >= 0):
        raise ValueError("invalid ADC")
    samples.append((t_ms, raw, mv))
# A separate root.after callback renders the latest samples.
''',
 gui_tests=['raw=0/2048/4095 แสดงถูก ไม่หารด้วยศูนย์ตอนกราฟมี sample เดียว', 'รับ 10000 samples แล้ว history ไม่เกิน 600', 'export เปิดอ่านกลับแล้วจำนวนแถว/หน่วยตรง'],
 gui_summary='การเก็บ sample และวาดจอมีอัตราต่างกันได้ ต้องจำกัดหน่วยความจำและบันทึกหน่วย/ที่มาของข้อมูล',
 exercise='ทำไมเวลา PC รับข้อมูลไม่เท่ากับเวลาที่ ADC sample?', answer='มีคิวและเวลาเดินทาง Serial ควรใช้ timestamp MCU เพื่อดูช่วง sampling และเก็บ received time แยก'),
dict(n=6, slug='Timer', title='Timer และ Period',
 cfg='Lab เดี่ยวใช้ TIM5 Internal Clock, Counter Up; ตัวอย่าง f_TIM=16 MHz ตั้ง PSC=15999 ARR=999 ได้ update ทุก 1000 ms เริ่ม polling ก่อน; คง HAL timebase แยกไว้ และอย่าใช้ TIM5 ร่วม encoder ในโปรเจกต์รวมโดยไม่จัดสรรใหม่',
 reg='PSC แบ่ง clock; ARR กำหนดปลาย count; CNT ค่าปัจจุบัน; EGR โหลดค่าผ่าน update; SR.UIF ระบุ update',
 code='''/* USER CODE BEGIN 2 */
if (HAL_TIM_Base_Start(&htim5) != HAL_OK) { Error_Handler(); }
__HAL_TIM_CLEAR_FLAG(&htim5, TIM_FLAG_UPDATE);
/* USER CODE BEGIN 3: polling-only experiment */
if (__HAL_TIM_GET_FLAG(&htim5, TIM_FLAG_UPDATE) != RESET) {
    __HAL_TIM_CLEAR_FLAG(&htim5, TIM_FLAG_UPDATE);
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}''',
 steps=['เขียนสูตร PSC/ARR และตรวจ clock tree ก่อน generate', 'เริ่ม timer และตรวจ CNT เดิน', 'ใช้ polling UIF ทดลอง 100/1000 ms โดย main ไม่มีงานบล็อก', 'จงใจเพิ่มงานช้าแล้วสังเกต UIF ไม่ใช่ counter จำนวน event', 'ถ้ารับ PERIOD จาก GUI ให้หยุด timer/reload/update/clear flag/restart ตามลำดับที่ตรวจแล้ว จึง ACK'],
 pseudo='clock → prescaler → counter → update flag → application; เปลี่ยน period ต้องจัดการค่า buffered และ pending',
 tests=['CNT เดินและ wrap ที่ ARR', 'คาบตรงกับสูตรภายใต้ clock ที่วัด/ยืนยัน', 'อธิบายได้ว่าการ polling ช้าอาจรวมหลาย update เป็นหนึ่ง'],
 issues='CNT ไม่เดิน: CEN/clock; คาบสองเท่า: สับสน toggle กับ cycle; เปลี่ยน PSC แล้วไม่ทันที: ค่า buffered ยังไม่ latch',
 summary='Timer ทำงานจาก hardware clock ส่วน main มาสังเกต flag การสังเกตช้าไม่ทำให้ได้จำนวนเหตุการณ์ครบเสมอ',
 gui_goal='ตั้ง period และเปรียบเทียบ timestamp MCU กับ callback UI',
 widgets='Spinbox 10–5000 ms, Apply, labels requested/confirmed, ตาราง timestamp',
 gui_steps=['validate period เป็นจำนวนเต็มและส่งเฉพาะกด Apply', 'รอ ACK ก่อนยืนยันค่าใหม่', 'รับ TIMER telemetry ที่มี MCU ms/update_count', 'คำนวณ delta ด้วย unsigned wrap สำหรับ tick MCU แยกจาก received time ฝั่ง PC', 'ทำ UI tick ด้วย after แล้วทดลองลากหน้าต่าง/งานอื่นเพื่อดู jitter'],
 gui_code='''def tick_delta_ms(new, old):
    return (new - old) & 0xFFFFFFFF

def ui_heartbeat():
    ui_tick.set(ui_tick.get() + 1)
    root.after(100, ui_heartbeat)
# 100 ms is a scheduling request, not a precise hardware period.
''',
 gui_tests=['10/1000/5000 ส่งได้และ 0/5001 ไม่ส่ง', 'old=0xFFFFFFF0,new=0x10 ได้ delta=32', 'UI delay ไม่ถูกบันทึกเป็น timer error ฝั่ง MCU โดยอัตโนมัติ'],
 gui_summary='after จัดตาราง UI ไม่ได้แทน hardware timer การวิเคราะห์เวลาต้องรู้ว่า timestamp มาจากฝั่งใด',
 exercise='ถ้า UART รวม 10 timer updates เป็น telemetry เดียวควรคำนวณ period อย่างไร?', answer='ใช้ delta MCU time และ delta update_count ที่สอดคล้องกัน ไม่ถือว่าช่องว่างระหว่าง frame คือ period หนึ่งรอบ'),
dict(n=7, slug='Interrupt', title='Interrupt และ Event',
 cfg='ใช้ timer จาก Lab06 เปิด NVIC timer interrupt ที่ตรง instance และตรวจ generated handler เรียก HAL_TIM_IRQHandler; สำหรับ EXTI เพิ่ม GPIO_EXTI ตาม edge/pull จริงและเลือก NVIC IRQ ที่ครอบคลุม pin',
 reg='TIM DIER.UIE เปิด update interrupt; SR.UIF pending; NVIC enable/priority; EXTI/SYSCFG route และ edge สำหรับขาภายนอก',
 code='''/* USER CODE BEGIN PV */
static volatile uint32_t irq_count = 0;
/* USER CODE BEGIN 4: do not duplicate an existing callback */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM5) { ++irq_count; }
}
/* USER CODE BEGIN 2 */
if (HAL_TIM_Base_Start_IT(&htim5) != HAL_OK) { Error_Handler(); }
/* Main may snapshot irq_count; do not reset it concurrently. */''',
 steps=['ตรวจ generated IRQ handler และ breakpoint ใน callback ชั่วคราว', 'ISR เพิ่ม counter อย่างเดียว ไม่ส่ง UART/วาด OLED', 'main อ่าน snapshot ของ aligned uint32_t ที่ ISR เป็นผู้เขียนคนเดียว และส่งอัตราจำกัด', 'ถ้าต้อง reset/read-modify-write counter ให้ทำ critical section ที่เก็บคืน interrupt mask เดิม', 'เพิ่ม EXTI แล้วนำ edge ไป debounce ใน main ไม่ใช้ HAL_Delay ใน ISR'],
 pseudo='hardware event → pending → NVIC → IRQ handler → HAL dispatcher → callback สั้น → main consume snapshot/event',
 tests=['เพิ่มจำนวน IRQ ได้แม้ main มีงานอื่นระยะสั้น', 'ไม่เกิด IRQ loop จาก pending ที่ไม่เคลียร์', 'counter wrap หรือ snapshot race มีวิธีจัดการที่อธิบายได้'],
 issues='callback ไม่เข้า: NVIC/DIER/handler; ค้าง ISR: delay/printf; count หาย: reset แข่งกับ ISR',
 summary='Interrupt แยกการรับเหตุการณ์จากงานหลัก ISR ที่สั้นช่วยจำกัด latency แต่ข้อมูลร่วมยังต้องออกแบบ ownership',
 gui_goal='แสดง interrupt counters และ event stream โดยไม่ redraw จน UI ค้าง',
 widgets='Treeview event log, counter, dropped-frame label, Clear View',
 gui_steps=['mock burst telemetry 1000 frame แล้วให้ UI drain ครั้งละจำกัด', 'เก็บ Treeview ไม่เกิน 500 rows และ queue มีขอบเขต', 'Clear View ล้างเฉพาะจอ ไม่ส่ง reset counter ถ้า protocol ไม่มีคำสั่ง', 'แสดง irq_count สะสมกับจำนวน frame ที่รับแยกกัน', 'ตรวจ missing seq และนับ dropped ไม่แต่ง event ขึ้นมา'],
 gui_code='''MAX_ROWS = 500
def append_event(values):
    tree.insert("", "end", values=values)
    rows = tree.get_children()
    if len(rows) > MAX_ROWS:
        tree.delete(*rows[:len(rows) - MAX_ROWS])
''',
 gui_tests=['burst แล้วปุ่ม/ปิดหน้าต่างยังตอบสนอง', 'Clear View ไม่ทำให้ MCU counter เป็นศูนย์', 'frame drop แสดงตัวนับและค่าล่าสุดได้'],
 gui_summary='จำนวน interrupt จำนวน telemetry frame และจำนวนแถวบนจอเป็นคนละสิ่ง ต้องแยก counters และจำกัดคิว',
 exercise='ถ้า irq_count เพิ่ม 100 แต่ GUI รับ 10 frame แปลว่าหาย 90 interrupt หรือไม่?', answer='ไม่จำเป็น firmware อาจรายงาน counter แบบ batch ต้องดู protocol/seq และความถี่ publish'),
dict(n=8, slug='I2C_OLED', title='I2C และ OLED',
 cfg='ยืนยัน OLED controller, ขนาด, address และแรงดันก่อน เลือก I2C instance ที่ใช้งานได้พร้อม SCL/SDA AF open-drain ตรวจ pull-up จริง เริ่ม Standard mode 100 kHz และ timing ตาม clock อย่านำ register ของ FMPI2C ปนกับ I2C ปกติ',
 reg='GPIO AF/open-drain; I2C CR/SR/DR และ timing ของ instance; controller OLED มีคำสั่งอีกชุดแยกจาก peripheral MCU',
 code='''/* Helper after hi2c1 initialization. Call only with a verified address. */
HAL_StatusTypeDef oled_probe(uint8_t address7)
{
    if (address7 < 0x08U || address7 > 0x77U) { return HAL_ERROR; }
    return HAL_I2C_IsDeviceReady(&hi2c1,
        (uint16_t)address7 << 1U, 2U, 20U);
}
/* Display initialization/drawing must come from the actual controller driver. */''',
 steps=['บันทึกรุ่นจอ/controller/address จากเอกสารหรือการตรวจที่มีหลักฐาน', 'probe address แบบจำกัดเวลา ตรวจว่า API รับ address shifted', 'เลือก driver ที่ตรง controller และทดสอบข้อความคงที่', 'แยก draw buffer กับ transfer ไม่ส่งทั้งจอทุก main loop', 'รับ OLED,text จาก UART validate ASCII/ความยาวและ ACK หลัง driver คืนสำเร็จ ถ้า NACK ให้ ERR HW'],
 pseudo='validate text → update display buffer → transfer with timeout → ACK OK หรือ ERR HW; งานอื่นต้องเดินต่อเมื่อจอไม่ตอบ',
 tests=['probe ACK กับ address ที่ถูกและ NACK กับ address ผิด', 'ส่งข้อความ 1 และ 20 ตัวอักษรได้โดยไม่ล้น', 'จอไม่อยู่แล้ว main/UART ยังทำงานและรายงาน error'],
 issues='ACK แต่จอมืด: init/controller/contrast; bus busy: pull-up/wiring; อักษรผิด: framebuffer/font/offset',
 summary='I2C ACK ยืนยันการสื่อสารระดับ bus ไม่ยืนยันว่าจอวาดถูก ต้องตรวจทั้ง transport และ controller driver',
 gui_goal='ส่งข้อความพร้อม validation และแสดงผลตอบจากการอัปเดตจอ',
 widgets='Entry, character counter, Send, status และ mock preview',
 gui_steps=['จำกัดรุ่นแรกเป็น ASCII 1–20 ตัวอักษร ไม่มี comma/newline ตาม protocol', 'preview แสดงสิ่งที่ขอส่งและติดป้ายว่าไม่ใช่ภาพจากจอจริง', 'ส่งแล้วรอ ACK/ERR ไม่แก้ status เป็นสำเร็จก่อนตอบ', 'mock จำลอง NACK/timeout เพื่อฝึก error state', 'เทียบข้อความบน OLED จริงกับคำขอเมื่อ driver พร้อม'],
 gui_code='''def validate_oled(text):
    if not (1 <= len(text) <= 20):
        raise ValueError("ใช้ 1-20 ตัวอักษร")
    if any(ord(c) < 32 or ord(c) > 126 or c == "," for c in text):
        raise ValueError("ใช้ ASCII ที่พิมพ์ได้ ยกเว้น comma")
    return text
''',
 gui_tests=['ข้อความปกติส่งได้; ภาษาไทย/comma/newline ถูกปฏิเสธตามรุ่น protocol', 'ERR HW แสดง error ไม่แสดง success', 'preview ไม่ถูกนำไปอ้างว่าฮาร์ดแวร์แสดงแล้ว'],
 gui_summary='Validate ให้ตรงกับความสามารถ firmware/font การมี preview ไม่แทนการตรวจจอจริงและ ACK ไม่รับรองคุณภาพภาพ',
 exercise='ทำไม GUI พิมพ์ภาษาไทยได้แต่ยังไม่ส่งในรุ่นแรก?', answer='Tkinter รองรับไม่ได้หมายความว่า protocol/font/controller path พร้อม รุ่นแรกกำหนด ASCII ต้องขยายทั้งระบบก่อน'),
dict(n=9, slug='Encoder', title='Encoder และการวัดรอบ',
 cfg='ใช้ timer รองรับ encoder เช่น TIM5 ตั้ง Encoder Mode TI1 and TI2 ตรวจ CH1/CH2 AF คู่จริง, polarity, input filter และ period ตามความกว้าง counter ย้าย timer งานอื่นถ้าซ้ำ เริ่ม PSC=0',
 reg='SMCR encoder mode; CCMR input mapping/filter; CCER polarity; CNT count/direction; ARR wrap range',
 code='''/* USER CODE BEGIN 2 */
if (HAL_TIM_Encoder_Start(&htim5, TIM_CHANNEL_ALL) != HAL_OK) {
    Error_Handler();
}
uint32_t previous = __HAL_TIM_GET_COUNTER(&htim5);
/* Main sample task; assumes a 32-bit full-range TIM5 counter */
uint32_t current = __HAL_TIM_GET_COUNTER(&htim5);
uint32_t modular = current - previous;
int64_t delta = (modular <= 0x7FFFFFFFU)
    ? (int64_t)modular : (int64_t)modular - 4294967296LL;
previous = current;
/* Valid only if travel per sample is less than half the counter range. */''',
 steps=['ยืนยันชนิด encoder และแรงดัน output ก่อนต่อ A/B', 'หมุนหนึ่งรอบช้า ๆ บันทึก counts จริงในโหมด decoding ที่เลือก', 'สลับทิศทางและตรวจ signed delta', 'แก้ wrap ของ counter ก่อนสะสมตำแหน่งในชนิดข้อมูลที่พอ', 'คำนวณ RPM เฉพาะเมื่อ encoder ผูกกับเพลาและรู้ counts/rev/gear ratio'],
 pseudo='sample CNT ตามช่วงเวลา → modular delta → unwrap → accumulate position → ถ้าข้อมูล calibration พร้อมจึงคำนวณ RPM',
 tests=['หนึ่งรอบได้ counts/rev ที่อธิบายได้ทั้งสองทิศ', 'ข้าม wrap แล้วยังได้ delta ถูก', 'สาย A/B หลวมไม่ถูกแสดงว่าเป็น RPM เชื่อถือได้'],
 issues='count กลับด้าน: A/B/polarity; count สั่น: noise/filter; RPM ผิด 4 เท่า: decoding multiplier',
 summary='Count เป็นตำแหน่งเชิงดิจิทัล การคำนวณความเร็วต้องรู้เวลา ระยะต่อ count และแก้ counter wrap',
 gui_goal='แสดงตำแหน่งทิศทางและความเร็วที่มีเงื่อนไข calibration ชัดเจน',
 widgets='count label, direction indicator, counts/rev input, RPM label และ calibration status',
 gui_steps=['ใช้ signed_count ที่ firmware unwrap แล้ว ไม่แก้ timer wrap ซ้ำใน GUI', 'วัด delta position/delta MCU timestamp แล้วคำนวณ RPM เมื่อเป็น shaft sensor', 'ถ้าเป็น rotary knob แสดง count/direction อย่างเดียว', 'ถ้า delta_t=0 หรือข้อมูลเก่าแสดง unavailable ไม่หาร', 'reconnect ล้าง baseline และไม่ใช้ delta ข้าม session'],
 gui_code='''def rpm_from_delta(delta_count, dt_ms, counts_per_rev):
    if dt_ms <= 0 or counts_per_rev <= 0:
        return None
    return 60000.0 * delta_count / (counts_per_rev * dt_ms)
''',
 gui_tests=['100 counts ใน 500 ms ที่ 400 counts/rev ได้ 30 RPM', 'delta_t=0 คืน unavailable', 'session ใหม่ต้องรอ sample ที่สองก่อนคำนวณ'],
 gui_summary='RPM ต้องมี calibration และเวลาอ้างอิง ไม่ใช่เพียงนำ counter ไปใส่กราฟ การ reconnect ทำให้ baseline เดิมใช้ไม่ได้',
 exercise='encoder knob หมุนด้วยมือใช้แสดง RPM มอเตอร์ได้หรือไม่?', answer='ไม่ได้ ถ้าไม่ได้วัดเพลามอเตอร์นั้น ต้องแยกเป็น input knob และ shaft feedback'),
dict(n=10, slug='PWM_Motor', title='PWM Motor และการรวมระบบ',
 cfg='ยืนยัน motor DC brushed/driver/แหล่งจ่ายและ stop truth table ก่อน กำหนด PWM channel, enable pin และ initial output ให้หยุดตั้งแต่ boot คง SWD/UART และจัด timer ของ encoder/timebase ไม่ให้ชน เลือก PWM frequency ตาม driver จริง',
 reg='TIM PWM/CCR/MOE และ GPIO driver enable; firmware state/watchdog เป็นอีกชั้น ไม่ได้เกิดเองจาก CubeMX',
 code='''/* Pseudocode only: implement driver_* for the actual driver. */
on_boot_or_new_session:
    driver_stop(); state = DISARMED; target = applied = 0;
on_ARM_if_no_fault:
    target = applied = 0; state = ARMED;
on_MOTOR_if_armed_and_percent_valid:
    target = requested;
on_STOP_or_watchdog_or_fault:
    driver_stop(); state = DISARMED; target = applied = 0;
periodic_nonblocking_task:
    if state == ARMED: ramp_applied_toward_target();''',
 steps=['ทดสอบช่อง PWM ด้วย LED/logic analyzer ก่อนต่อภาคกำลัง', 'ทำ state machine และ watchdog แล้วจำลอง timeout บน firmware', 'ตรวจ boot/reset/new session/STOP ทั้งหมดกลับ output หยุด', 'ต่อ driver ที่ยืนยันแล้วและเริ่ม duty ต่ำภายใต้เงื่อนไขอุปกรณ์จริง', 'เพิ่ม ramp และ telemetry applied duty; command ACK หมายถึงรับ target ไม่ใช่ RPM ถึงเป้า', 'รวม ADC/OLED/encoder โดยใช้ resource allocation ที่ตรวจ pin/timer conflict'],
 pseudo='ทุก loop: จัดการ STOP/fault/watchdog ก่อน → parse control → update ramp ตามเวลา → sample/report แบบมีขอบเขต',
 tests=['boot/reset/reconnect ไม่หมุนเองและต้อง ARM ใหม่', 'หยุด PING เกิน watchdog แล้ว firmware หยุดแม้ GUI ค้าง', 'STOP ยกเลิก ramp ไม่รอให้ duty ลดช้า ๆ', 'OLED/UART error ไม่ทำให้ main หยุดตรวจ watchdog'],
 issues='boot กระตุก: pin default/driver enable; STOP ช้า: blocking loop/TX queue; duty เปลี่ยนแต่ RPM ไม่ตาม: โหลด/ไฟ/feedback',
 summary='การควบคุมมอเตอร์ต้องมี output state ที่แน่นอนและทางหยุดใน firmware GUI เป็นผู้ขอคำสั่ง ไม่ควรเป็นชั้นเดียวที่ดูแล link loss',
 gui_goal='สร้างหน้าควบคุมมอเตอร์ที่ state ชัดและไม่ replay คำสั่งหลังต่อใหม่',
 widgets='ARM, STOP เด่น, duty slider, requested/applied labels, link/fault state และ heartbeat indicator',
 gui_steps=['เริ่ม DISARMED และ disable slider จน HELLO และ ARM ACK สำเร็จ', 'ส่ง target ผ่าน MOTOR และแสดง applied จาก MOTOR telemetry แยกกัน', 'ขณะ ARMED จัด PING ทุก 200 ms ตาม protocol แต่ยอมรับว่า scheduling อาจช้า', 'STOP แซง TX queue และยกเลิก pending target; firmware watchdog ยังเป็นตัวคุมเมื่อส่งไม่ได้', 'disconnect/timeout/fault ล้างคำสั่งเก่าและแสดง UNKNOWN หรือ FAULT ไม่ยืนยันหยุดหากไม่มีหลักฐาน', 'ทดสอบ mock fault/link loss ก่อนเชื่อม driver จริง'],
 gui_code='''# State transition sketch; transport and widgets are implemented in this Lab.
def on_link_lost():
    pending_controls.clear()
    motor_state.set("UNKNOWN - link lost")
    arm_button.state(["disabled"])
    duty_slider.state(["disabled"])
    # Do not claim physical stop; firmware watchdog must handle loss.
''',
 gui_tests=['เปิด GUI/reconnect แล้วไม่มี MOTOR command อัตโนมัติ', 'slider backlog ไม่ขวาง STOP', 'ปิดโปรแกรมหรือ mock link loss แล้วไม่แสดง false stopped', 'บนบอร์ดจริงพิสูจน์ watchdog ด้วยการหยุด heartbeatและวัด output'],
 gui_summary='State ที่ GUI แสดงต้องตรงกับหลักฐาน การสูญเสีย link ทำให้ผลทางกายภาพไม่ทราบ และ firmware ต้องหยุดเองตาม watchdog',
 exercise='เมื่อ port หลุดควรตั้งข้อความ STOPPED ทันทีไหม?', answer='ไม่ ให้ UNKNOWN/link lost จนมีหลักฐาน Firmware watchdog เป็นผู้สั่งหยุดโดยไม่พึ่ง GUI'),
]

source=(MCU/'LESSONS.md').read_text(encoding='utf-8')
parts={int(m.group(1)):m.group(0) for m in re.finditer(r'^## Lab(\d{2}):.*?(?=^## |\Z)',source,re.M|re.S)}
def write(path, text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.strip()+'\n',encoding='utf-8')
def numbered(items): return '\n'.join(f'{i}. {x}' for i,x in enumerate(items,1))
def bullets(items): return '\n'.join(f'- {x}' for x in items)

for r in records:
    name=f"Lab{r['n']:02d}_{r['slug']}"
    md=MCU/'labs'/name
    gd=GUI/'labs'/name
    base=parts[r['n']].split('\n',1)[1].strip()
    language='text' if r['n']==10 else 'c'
    write(md/'lesson.md', f'''# {name}: {r['title']}

## เป้าหมายและพื้นฐาน

{base}

## ตั้งค่า STM32CubeMX

{r['cfg']}

ใช้ MCU STM32F410RB ที่ตรง package ของบอร์ด บันทึก `.ioc`, CubeMX/firmware package version และเลือก toolchain ที่ติดตั้งจริง ก่อน generate ให้เก็บ USER CODE และตรวจ diff หลัง generate ชื่อ handle ในตัวอย่างเป็นตัวอย่าง ต้องเทียบกับไฟล์ที่ CubeMX สร้าง

## เชื่อมกับรีจิสเตอร์

{r['reg']}

## ลงมือทีละขั้น

{numbered(r['steps'])}

## Pseudocode

{r['pseudo']}

## ตัวอย่างแกนหลักและตำแหน่งเพิ่ม

ตัวอย่างประกอบแนวคิด ไม่ใช่ firmware เต็มหรือโปรเจกต์พร้อม flash ให้เพิ่มใน USER CODE ตามที่ระบุหรือไฟล์ application แยกหลัง generated init ห้ามคัด main ทับทั้งไฟล์ ยังไม่ได้ build กับ `.ioc` หรือทดสอบบอร์ดจริง

```{language}
{r['code']}
```

## ทดสอบและเกณฑ์ผ่าน

{bullets(r['tests'])}

ทุกข้อข้างต้นต้องมี expected/actual และเครื่องมือที่ใช้ หากไม่มีเครื่องมือวัดเวลาให้ระบุข้อจำกัดแทนการสรุปความแม่นยำ

## Debug จากอาการ

{r['issues']}

## ต่อกับ Python GUI

คู่บทคือ [Tkinter {name}](../../../../Antigravity-Tkinter/labs/{name}/lesson.md) ใช้ [protocol](../../../../Antigravity-Tkinter/protocol.md) ที่ออกแบบสำหรับหลักสูตรนี้ ต้องเพิ่ม UART/parser หลัง Lab03 ก่อนเชื่อมจริง; GUI เรียน mock ก่อนได้

## สรุปท้าย Lab

{r['summary']}

งานส่ง: `.ioc`, source ที่เพิ่ม, pin map, clock calculation, ตาราง expected/actual และคำอธิบายรีจิสเตอร์ อ่าน [summary.md](summary.md) เพื่อทบทวนและกรอกผลจริง
''')
    write(md/'summary.md',f'''# สรุป {name} — STM32

## ความรู้ที่ต้องจำ

{r['summary']}

**CubeMX:** {r['cfg']}

**รีจิสเตอร์สำคัญ:** {r['reg']}

**จุดผิดพลาดที่ต้องแยกให้ออก:** {r['issues']}

## ก่อนถือว่าจบ Lab

{bullets(r['tests'])}

## ผลการเรียนจริง

สถานะ: ยังไม่ได้ทดลอง — สรุปความรู้นี้ไม่ใช่รายงานผลทดสอบ

- วันที่ / รุ่นบอร์ด / toolchain:
- ค่าที่ตั้งและเหตุผล:
- หลักฐานและผล expected เทียบ actual:
- ปัญหาที่พบและวิธีแก้:
- สิ่งที่ยังไม่เข้าใจ:
- ผ่านเกณฑ์ข้อใดแล้ว / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
''')
    write(gd/'lesson.md',f'''# {name} — Python Tkinter

## เป้าหมาย

{r['gui_goal']}

เรียนพื้นฐาน Python/Tkinter จาก roadmap ก่อน บทก่อน Lab03 ใช้ mock; การเชื่อมบอร์ดจริงทุกบทต้องผ่าน Lab03 GUI และ Lab03 firmware รวมทั้ง HELLO/PING ตาม [protocol.md](../../protocol.md)

## แนวคิดที่ใช้

{r['gui_summary']}

Widgets: {r['widgets']}

แยก requested, pending และ confirmed ตามความจำเป็น ใช้ StringVar/IntVar เป็นค่าของ view; protocol parser ตรวจข้อมูลก่อนให้ application state อัปเดต GUI

## ขั้นตอนปฏิบัติ

{numbered(r['gui_steps'])}

## ตัวอย่างแกนหลัก

Snippet เพื่อใช้ระหว่างเรียน ไม่ใช่แอปเต็ม ชื่อ widget/state เช่น root/status และฟังก์ชัน application ที่เรียกต้องสร้างในขั้นตอนก่อนหน้า ในบทนี้ให้ Antigravity ช่วยเติมทีละส่วนและอธิบายเหตุผล

```python
{r['gui_code']}
```

ให้ main thread เป็นผู้เรียกโค้ดที่เปลี่ยน widget ใช้ worker เฉพาะ transport; ห้ามเรียก serial read แบบรอไม่จำกัดจาก button callback Mock ต้องคืน response ตามคำสั่งและ session/id จริง ไม่เปลี่ยน GUI ให้ success โดยข้าม parser

## กรณีทดสอบ

{bullets(r['gui_tests'])}

ทดสอบเพิ่มทุกบท: ปิดหน้าต่างขณะมี pending, ส่งข้อมูลผิดชนิด, reconnect และยืนยันว่าไม่มี callback/worker เก่ามาแก้ state ของ session ใหม่

## แบบฝึกหัด

{r['exercise']}

แนวตอบ: {r['answer']}

## งานส่งและการประเมิน

ส่งโค้ด Python พร้อมวิธีรัน, ภาพหน้าจอ mock/serial ที่แยกชัด, ตัวอย่าง frame ที่รับส่ง และตารางทดสอบ ไม่ใช้ mock เป็นหลักฐานฮาร์ดแวร์

เกณฑ์: อธิบาย flow 2 คะแนน, UI/state 2, function ตามโจทย์ 3, edge cases 2, สรุป 1; ผ่านอย่างน้อย 8/10 และกรณีทดสอบหลักครบ

## สรุปท้าย Lab

{r['gui_summary']}

อ่าน [summary.md](summary.md) แล้วให้ผู้เรียนอธิบายด้วยตนเองก่อนกรอกผลจริง คู่บท MCU: [บทเรียน STM32](../../../output/stm32-course/labs/{name}/lesson.md)
''')
    # The GUI lesson is three directories below GPT, so the sibling course needs three '..'.
    write(gd/'summary.md',f'''# สรุป {name} — Tkinter

## สิ่งที่เรียนและสิ่งที่สร้าง

{r['gui_goal']}

{r['gui_summary']}

**Widgets/เครื่องมือ:** {r['widgets']}

**คำถามทบทวน:** {r['exercise']}

**แนวตอบ:** {r['answer']}

## Checklist ก่อนจบ

{bullets(r['gui_tests'])}

## บันทึกหลังลงมือจริง

สถานะ: ยังไม่ได้ทดลอง ไม่มีการรับรองว่า GUI หรือบอร์ดผ่านการทดสอบแล้ว

- วันที่ / Python version / pySerial version:
- สิ่งที่เขียนและเข้าใจด้วยตนเอง:
- ผล mock พร้อมหลักฐาน:
- ผล Serial/บอร์ดจริง หรือระบุยังไม่ทดสอบ:
- กรณีผิดพลาดที่ทดสอบ:
- ปัญหาคงค้าง / วิธีแก้ / ขั้นถัดไป:

[กลับบทเรียน](lesson.md)
''')

for folder, key, title in [(MCU,'summary','STM32F410RB + STM32CubeMX'),(GUI,'gui_summary','Python Tkinter + Serial')]:
    rows=[]
    sections=[]
    for r in records:
        name=f"Lab{r['n']:02d}_{r['slug']}"
        rows.append(f"| {name} | [บทเรียน](labs/{name}/lesson.md) | [สรุป](labs/{name}/summary.md) |")
        sections.append(f"## {name}\n\n{r[key]}\n\nหลักฐานที่ต้องส่ง: "+'; '.join(r['tests'] if folder==MCU else r['gui_tests']))
    write(folder/'LAB_SUMMARIES.md',f'# สรุปครบ 10 Lab — {title}\n\nนี่คือสรุปความรู้และเกณฑ์ตรวจ ไม่ใช่ผลทดลองจริง\n\n| Lab | เนื้อหา | สรุปและบันทึกผล |\n|---|---|---|\n'+'\n'.join(rows)+'\n\n'+'\n\n'.join(sections))
    write(folder/'progress.md','# ความคืบหน้าการเรียน\n\nทุก Lab เริ่มที่ยังไม่ได้ทดลอง อัปเดตเมื่อมีหลักฐานจริง เก็บ mock/build/hardware แยกกัน\n\n| Lab | เนื้อหา | Mock/ตรวจโค้ด | Hardware | หลักฐาน/ปัญหา |\n|---|---|---|---|---|\n'+'\n'.join(f"| Lab{r['n']:02d}_{r['slug']} | พร้อมเรียน | ยังไม่ทดสอบ | ยังไม่ทดสอบ | — |" for r in records))

print('Created 10 MCU lessons + 10 summaries; 10 GUI lessons + 10 summaries; indexes and progress files.')
