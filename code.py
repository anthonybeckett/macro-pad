import time
import board
import digitalio
import usb_hid
import rotaryio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import usb_cdc
import busio
import displayio
import adafruit_displayio_ssd1306 
import terminalio
from adafruit_display_text import label

#Initalise USB Serial & clear buffer
uart = usb_cdc.data
time.sleep(0.5)
uart.reset_input_buffer()

# Clear any display data holding up pins
displayio.release_displays()

# Init I2C
i2c = busio.I2C(board.GP1, board.GP0)

# Lock the I2C device before we try to scan
while not i2c.try_lock():
    pass
# Print the addresses found once
print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])

# Unlock I2C now that we're done scanning.
i2c.unlock()

# Init display
display_bus = displayio.I2CDisplay(i2c, device_address = 0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32) 

# Draw a label
text = "Hello World"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=2, y=5)
display.show(text_area)

# Media Buttons
btnPrev = digitalio.DigitalInOut(board.GP18)
btnPrev.direction = digitalio.Direction.INPUT
btnPrev.pull = digitalio.Pull.UP

btnPlay = digitalio.DigitalInOut(board.GP17)
btnPlay.direction = digitalio.Direction.INPUT
btnPlay.pull = digitalio.Pull.UP

btnNext = digitalio.DigitalInOut(board.GP16)
btnNext.direction = digitalio.Direction.INPUT
btnNext.pull = digitalio.Pull.UP

# builtin LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# USB Device
consumer = ConsumerControl(usb_hid.devices)

delay = 0.2

def blink_led(duration):
    led.value = True
    time.sleep(duration)
    led.value = False
    time.sleep(duration)

while True:
    # poll encoder position
    # position = enc.position
    # if position != lastPosition:
    #     led.value = True
    #     if lastPosition < position:
    #         consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
    #     else:
    #         consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
    #     lastPosition = position
    #     led.value = False

    # poll encoder button
    # if encSw.value == 0:
    #     consumer.send(ConsumerControlCode.MUTE)
    #     led.value = True
    #     time.sleep(delay)
    #     led.value = False

    if btnPrev.value == 0:
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        blink_led(delay)
        
    if btnPlay.value == 0:
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
        blink_led(delay)
        
    if btnNext.value == 0:
        consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        blink_led(delay)

    if uart.in_waiting:
        #print(uart.readline());
        #time.sleep(0.2)
        #print("Data: " + data)
        #data = uart.readline()
        #print("Incoming data: " + data)
        blink_led(delay)
        blink_led(delay)
        blink_led(delay)
        blink_led(delay)
        blink_led(delay)
        uart.reset_input_buffer()

    time.sleep(0.1)    
