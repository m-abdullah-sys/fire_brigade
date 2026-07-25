================================================================================
                    AUTONOMOUS FIRE BRIGADE SYSTEM SCHEMATIC
================================================================================

                         +-------------------------+
                         |      BATTERY PACK       |
                         |  (12V DC High Current)  |
                         +------------+------------+
                                      |
                     +----------------+----------------+
                     | (+)                             | (-)
                     v                                 v
          +---------------------+            +-------------------+
          |  L298N Motor Driver |            |    GND BUS BAR    |
          |  12V Power Terminal |            +---------+---------+
          +----------+----------+                      |
                     | 5V Output                       |
                     v                                 v
          +---------------------+            +-------------------+
          |     5V Buck / Pi    |            |   Raspberry Pi    |
          |  Power Input Port   |            |    GND (Pin 6)    |
          +----------+----------+            +---------+---------+
                     | 5V DC                           |
                     v                                 |
          +---------------------+                      |
          |   Raspberry Pi      |                      |
          |   5V Rail (Pin 2)   |                      |
          +---------------------+                      |
                                                       |
 ------------------------------------------------------                   

                 RASPBERRY PI BCM GPIO CONNECTION MAP
                 
    MLX90614 IR Sensor (I2C)
    [3.3V]  <---------------------------- Raspberry Pi Pin 1 (3.3V)
    [GND]   <---------------------------- Raspberry Pi Pin 6 (GND)
    [SDA]   <---------------------------- Raspberry Pi Pin 3 (GPIO 2)
    [SCL]   <---------------------------- Raspberry Pi Pin 5 (GPIO 3)

    L298N Dual H-Bridge Driver
    [ENA]   <---------------------------- Raspberry Pi Pin 32 (GPIO 12 - PWM)
    [IN1]   <---------------------------- Raspberry Pi Pin 29 (GPIO 5)
    [IN2]   <---------------------------- Raspberry Pi Pin 31 (GPIO 6)
    [IN3]   <---------------------------- Raspberry Pi Pin 33 (GPIO 13)
    [IN4]   <---------------------------- Raspberry Pi Pin 35 (GPIO 19)
    [ENB]   <---------------------------- Raspberry Pi Pin 12 (GPIO 18 - PWM)
    [OUT1/OUT2] ------------------------> Left Track DC Motors
    [OUT3/OUT4] ------------------------> Right Track DC Motors

    Pan / Tilt Servo Gimbal
    [Pan Signal]  <---------------------- Raspberry Pi Pin 15 (GPIO 22 - PWM)
    [Tilt Signal] <---------------------- Raspberry Pi Pin 16 (GPIO 23 - PWM)
    [VCC / GND]   <---------------------- External 5V Power Rail / Common GND

    5V Relay Module (Water Pump Control)
    [VCC]   <---------------------------- Raspberry Pi Pin 2 (5V)
    [GND]   <---------------------------- Raspberry Pi Pin 6 (GND)
    [IN]    <---------------------------- Raspberry Pi Pin 40 (GPIO 21)
    [NO / COM Contacts] ----------------> High-Flow Water Pump & 12V Supply
================================================================================
