<h1>Raspberry Pi Pico - Simple RS485 Circle Network</h1>

<h2>Description</h2>

   *	Simple protocol to send data via RS485 channel between multiple Raspberry Pi Pico devices.

<h2>Usage</h2>

   * Connect Rpi Pico devices using RS485 channel.

   * Connect DS18 sensor to slave device, then upload RS485_slave.py as main.py to it.

   *  Connect LCD to master device, upload lcd_api.py and pico_i2c_lcd.py to the device. Then upload RS485_master.py as main.py

<h2>Required hardware</h2>

   * 2x Raspberry Pi Pico

   * 2x Waveshare Pico-2CH-RS485

   * I2C LCD

   * DS18B20

   * connecting cables