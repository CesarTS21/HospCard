#! /usr/bin/env python

import RPi.GPIO as GPIO
import time
 
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 7

LCD_WIDTH = 16    
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
 
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       
  GPIO.setup(LCD_E, GPIO.OUT)  
  GPIO.setup(LCD_RS, GPIO.OUT) 
  GPIO.setup(LCD_D4, GPIO.OUT) 
  GPIO.setup(LCD_D5, GPIO.OUT) 
  GPIO.setup(LCD_D6, GPIO.OUT) 
  GPIO.setup(LCD_D7, GPIO.OUT) 
 
  lcd_init()
 
  while True:
 
    # Envio de texto
    lcd_string(" - Bienvenido - ",LCD_LINE_1)
    lcd_string(" - A HospCard - ",LCD_LINE_2)
    time.sleep(5)
    
    lcd_string("Coloca tu tarjet",LCD_LINE_1)
    lcd_string("En el Escaner.  ",LCD_LINE_2)
    time.sleep(5)
 
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
      lcd_string(" Hora: " + time.strftime("%H:%M:%S"),LCD_LINE_1)
      lcd_string("Fecha: " + time.strftime("%d/%m/%y"),LCD_LINE_2)
      time.sleep(.3)
      
     
 
def lcd_init():
   #Generar dimenciones de pantalla.
  lcd_byte(0x33,LCD_CMD) 
  lcd_byte(0x32,LCD_CMD) 
  lcd_byte(0x06,LCD_CMD) 
  lcd_byte(0x0C,LCD_CMD) 
  lcd_byte(0x28,LCD_CMD) 
  lcd_byte(0x01,LCD_CMD) 
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode): 
  GPIO.output(LCD_RS, mode) 
 
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  lcd_toggle_enable()
  
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__': 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
