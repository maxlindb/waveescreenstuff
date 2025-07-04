# *****************************************************************************
# * | File        :	  epd3in7g.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2025-04-17
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from . import epdconfig

import PIL
from PIL import Image
import io

# Display resolution
EPD_WIDTH       = 240
EPD_HEIGHT      = 416

logger = logging.getLogger(__name__)

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.BLACK  = 0x000000   #   00  BGR
        self.WHITE  = 0xffffff   #   01
        self.YELLOW = 0x00ffff   #   10
        self.RED    = 0x0000ff   #   11

        
    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, 0)         # module reset
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    # send a lot of data   
    def send_data2(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        logger.debug("e-Paper busy H")
        epdconfig.delay_ms(100)
        while(epdconfig.digital_read(self.busy_pin) == 0):      # 0: idle, 1: busy
            epdconfig.delay_ms(5)
        logger.debug("e-Paper busy release")
        
    def TurnOnDisplay(self):
        self.send_command(0x12) # DISPLAY_REFRESH
        self.send_data(0X00)
        self.ReadBusy()
        
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start

        self.reset()
        self.ReadBusy()

        self.send_command(0x00)
        self.send_data(0x0F)	
        self.send_data(0x29)	

        self.send_command(0x01)
        self.send_data(0x07)
        self.send_data(0x00)
        self.send_data(0x22)
        self.send_data(0x78)
        self.send_data(0x0A)
        self.send_data(0x22) 	

        self.send_command(0x03)
        self.send_data(0x10)	
        self.send_data(0x54)	
        self.send_data(0x44)	

        self.send_command(0x06)
        self.send_data(0xC0)	
        self.send_data(0xC0)	
        self.send_data(0xC0)	

        self.send_command(0x30)
        self.send_data(0x08)	

        self.send_command(0x41)
        self.send_data(0x00)	

        self.send_command(0x50)
        self.send_data(0x37)	

        self.send_command(0x60)
        self.send_data(0x02)	
        self.send_data(0x02)	

        self.send_command(0x61)
        self.send_data(self.width//256)	
        self.send_data(self.width%256)	
        self.send_data(self.height//256)	
        self.send_data(self.height%256)	

        self.send_command(0x65)
        self.send_data(0x00)	
        self.send_data(0x00)	
        self.send_data(0x00)	
        self.send_data(0x00)	


        self.send_command(0xE7)
        self.send_data(0x1C)	

        self.send_command(0xE3)
        self.send_data(0x22)	

        self.send_command(0xFF)
        self.send_data(0xA5)

        self.send_command(0xEF)
        self.send_data(0x01)	
        self.send_data(0x1E)	
        self.send_data(0x0A)	
        self.send_data(0x1B)	
        self.send_data(0x0B)	
        self.send_data(0x17)	

        self.send_command(0xC3)
        self.send_data(0xFD)	
        self.send_command(0xDC)
        self.send_data(0x01)	
        self.send_command(0xDD)	
        self.send_data(0x08)	
        self.send_command(0xDE)	
        self.send_data(0x41)	

        self.send_command(0xFD)
        self.send_data(0x01)	
        self.send_command(0xE8)	
        self.send_data(0x03)	

        self.send_command(0xDA)
        self.send_data(0x07)	

        self.send_command(0xC9)
        self.send_data(0x00)	

        self.send_command(0xA8)
        self.send_data(0x0F)	

        self.send_command(0xFF)	
        self.send_data(0xE3)

        self.send_command(0xE9)	
        self.send_data(0x01)
        
        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0xFF)
        self.send_data(0xA5)

        self.send_command(0xEF)   
        self.send_data(0x03)
        self.send_data(0x1E)
        self.send_data(0x0A)
        self.send_data(0x1B)
        self.send_data(0x0E)
        self.send_data(0x15)

        self.send_command(0xDC) 	 
        self.send_data(0x01)

        self.send_command(0xDD) 	 
        self.send_data(0x08)

        self.send_command(0xDE)
        self.send_data(0x41)

        self.send_command(0xFF)
        self.send_data(0xE3)
        return 0

    def init_Fast(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start

        self.reset()
        self.ReadBusy()

        self.send_command(0x00)
        self.send_data(0x0F)	
        self.send_data(0x29)	

        self.send_command(0x01)
        self.send_data(0x07)
        self.send_data(0x00)
        self.send_data(0x22)
        self.send_data(0x78)
        self.send_data(0x0A)
        self.send_data(0x22)

        self.send_command(0x03)
        self.send_data(0x10)	
        self.send_data(0x54)	
        self.send_data(0x44)	

        self.send_command(0x06)
        self.send_data(0xC0)	
        self.send_data(0xC0)	
        self.send_data(0xC0)	

        self.send_command(0x30)
        self.send_data(0x08)	

        self.send_command(0x41)
        self.send_data(0x00)	

        self.send_command(0x50)
        self.send_data(0x37)	

        self.send_command(0x60)
        self.send_data(0x02)	
        self.send_data(0x02)	

        self.send_command(0x61)
        self.send_data(self.width//256)	
        self.send_data(self.width%256)	
        self.send_data(self.height//256)	
        self.send_data(self.height%256)		

        self.send_command(0x65)
        self.send_data(0x00)	
        self.send_data(0x00)	
        self.send_data(0x00)	
        self.send_data(0x00)	


        self.send_command(0xE7)
        self.send_data(0x1C)	

        self.send_command(0xE3)
        self.send_data(0x22)	

        self.send_command(0xFF)
        self.send_data(0xA5)

        self.send_command(0xEF)
        self.send_data(0x01)	
        self.send_data(0x1E)	
        self.send_data(0x0A)	
        self.send_data(0x1B)	
        self.send_data(0x0B)	
        self.send_data(0x17)	

        self.send_command(0xC3)
        self.send_data(0xFD)	
        self.send_command(0xDC)
        self.send_data(0x01)	
        self.send_command(0xDD)	
        self.send_data(0x08)	
        self.send_command(0xDE)	
        self.send_data(0x41)	

        self.send_command(0xFD)
        self.send_data(0x01)	
        self.send_command(0xE8)	
        self.send_data(0x03)	

        self.send_command(0xDA)
        self.send_data(0x07)	

        self.send_command(0xC9)
        self.send_data(0x00)	

        self.send_command(0xA8)
        self.send_data(0x0F)	

        self.send_command(0xFF)	
        self.send_data(0xE3)

        self.send_command(0xE9)	
        self.send_data(0x01)
        
        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0xFF)
        self.send_data(0xA5)

        self.send_command(0xEF)   
        self.send_data(0x03)
        self.send_data(0x1E)
        self.send_data(0x0A)
        self.send_data(0x1B)
        self.send_data(0x0E)
        self.send_data(0x15)

        self.send_command(0xDC) 	 
        self.send_data(0x01)

        self.send_command(0xDD) 	 
        self.send_data(0x08)

        self.send_command(0xDE)
        self.send_data(0x41)

        self.send_command(0xFF)
        self.send_data(0xE3)

        self.send_command(0xE0)
        self.send_data(0x02)
            
        self.send_command(0xE6)
        self.send_data(0x5B)
        
        self.send_command(0xA5)
        self.send_data(0x00)
        self.ReadBusy() 
        return 0

    def getbuffer(self, image):
        # Create a pallette with the 4 colors supported by the panel
        pal_image = Image.new("P", (1,1))
        pal_image.putpalette( (0,0,0,  255,255,255,  255,255,0,   255,0,0) + (0,0,0)*252)

        # Check if we need to rotate the image
        imwidth, imheight = image.size
        if(imwidth == self.width and imheight == self.height):
            image_temp = image
        elif(imwidth == self.height and imheight == self.width):
            image_temp = image.rotate(90, expand=True)
        else:
            logger.warning("Invalid image dimensions: %d x %d, expected %d x %d" % (imwidth, imheight, self.width, self.height))

        # Convert the soruce image to the 4 colors, dithering if needed
        image_4color = image_temp.convert("RGB").quantize(palette=pal_image)
        buf_4color = bytearray(image_4color.tobytes('raw'))

        # into a single byte to transfer to the panel
        if self.width % 4 == 0 :
            Width = self.width // 4
        else :
            Width = self.width // 4 + 1
        Height = self.height 
        buf = [0x00] * int(Width * Height)
        idx = 0
        for j in range(0, Height):
            for i in range(0, Width):
                    buf[i + j * Width] = (buf_4color[idx] << 6) + (buf_4color[idx+1] << 4) + (buf_4color[idx+2] << 2) + buf_4color[idx+3]
                    idx = idx + 4
        return buf

    def display(self, image):
        self.send_command(0x10)
        self.send_data2(image)
                    
        self.TurnOnDisplay()
        
    def Clear(self, color=0x55):
        if self.width % 4 == 0 :
            Width = self.width // 4
        else :
            Width = self.width // 4 + 1
        Height = self.height

        self.send_command(0x10)
        for j in range(0, Height):
            for i in range(0, Width):
                    self.send_data(color)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x02) # POWER_OFF
        self.send_data(0X00)
        epdconfig.delay_ms(100)
        
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)
        
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
### END OF FILE ###

