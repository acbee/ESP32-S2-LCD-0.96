from machine import Pin, SPI, PWM
import framebuf
import time

# Color in BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

class LCD(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 80
        self.cs = Pin(9, Pin.OUT)
        self.rst = Pin(21, Pin.OUT)
        self.bl = Pin(45, Pin.OUT)
        self.cs(0)
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(1, 10000_000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
        self.dc = Pin(18, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.Init()
        self.SetWindows(0, 0, self.width - 1, self.height - 1)
        
    def reset(self):
        self.rst(1)
        time.sleep(0.2) 
        self.rst(0)
        time.sleep(0.2)         
        self.rst(1)
        time.sleep(0.2)
        
    def off(self):
        pwm = PWM(Pin(45)) # BL
        pwm.freq(1)
        pwm.duty_u16(0)
        
    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def backlight(self, value): # 0-1000
        pwm = PWM(Pin(45)) # BL
        pwm.freq(1000)
        if value <= 0:
            value = 1
        if value >= 1000:
            value = 1000
        data = int((value*65536/1000) - 1)
        pwm.duty_u16(data)

    def Init(self):
        self.reset()
        self.backlight(1000)
        
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x21) 
        self.write_cmd(0x21) 

        self.write_cmd(0xB1) 
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB2)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB3) 
        self.write_data(0x05)  
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)

        self.write_cmd(0xB4)
        self.write_data(0x03)

        self.write_cmd(0xC0)
        self.write_data(0x62)
        self.write_data(0x02)
        self.write_data(0x04)

        self.write_cmd(0xC1)
        self.write_data(0xC0)

        self.write_cmd(0xC2)
        self.write_data(0x0D)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8D)
        self.write_data(0x6A)   

        self.write_cmd(0xC4)
        self.write_data(0x8D) 
        self.write_data(0xEE) 

        self.write_cmd(0xC5)
        self.write_data(0x0E)    

        self.write_cmd(0xE0)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x02)
        self.write_data(0x03)
        self.write_data(0x0E)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x12)
        self.write_data(0x27)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)
        
        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x03)
        self.write_data(0x03)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x02)
        self.write_data(0x08)
        self.write_data(0x0A)
        self.write_data(0x13)
        self.write_data(0x26)
        self.write_data(0x36)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)
        
        self.write_cmd(0x3A)
        self.write_data(0x05)
        
        self.write_cmd(0x36)
        self.write_data(0xA8)
        
        self.write_cmd(0x29)
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend): # 0, 0, 159, 79
        Xstart = Xstart + 1
        Xend = Xend + 1
        Ystart = Ystart + 26
        Yend = Yend + 26
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend)
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)
        self.write_cmd(0x2C) 
        
    def display(self):
        self.SetWindows(0, 0, self.width - 1, self.height - 1)       
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

if __name__=='__main__':
    lcd = LCD()
    lcd.fill(BLACK)
    lcd.text("Test", 1, 1, WHITE)
    #lcd.text("Hello Beautiful!", 18, 15, WHITE)
    #lcd.text("Ripe Bananas", 18, 35, GREEN)    
    #lcd.text("Smoothies!", 18, 55, RED)
    lcd.display()
    time.sleep(3)
    lcd.off()
