import time
from waveshare_esp32s2_lcd import LCD

# Color in BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

lcd = LCD()
lcd.fill(BLACK)
lcd.text("Test", 5, 5, WHITE)
lcd.display()
time.sleep(3)
lcd.off()
