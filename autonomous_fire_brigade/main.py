import time
import logging
from smbus2 import SMBus
from gpiozero import Motor, PWMOutputDevice, OutputDevice, Servo

# Initialize Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- PIN DEFINITIONS (BCM) ---
PIN_PUMP = 21
PIN_PAN = 22
PIN_TILT = 23

# --- THRESHOLDS ---
FIRE_TEMP_THRESHOLD_C = 50.0  # Temperature trigger level
SAFE_TEMP_THRESHOLD_C = 35.0  # Temperature safe level
I2C_ADDR = 0x5A               # MLX90614 SMBus address

class MLX90614:
    """Reads object temperatures via I2C using SMBus2."""
    def __init__(self, bus_num=1, address=I2C_ADDR):
        self.bus_num = bus_num
        self.address = address

    def read_object_temp(self):
        try:
            with SMBus(self.bus_num) as bus:
                # Read 3 bytes from register 0x07 (RAM Object 1 Temp)
                data = bus.read_i2c_block_data(self.address, 0x07, 3)
                raw_temp = (data[1] << 8) | data[0]
                temp_c = (raw_temp * 0.02) - 273.15
                return temp_c
        except Exception as e:
            logging.error(f"I2C Read Error: {e}")
            return 0.0

class AutonomousFireBrigade:
    def __init__(self):
        # Motors (L298N Differential Drive)
        self.left_motor = Motor(forward=5, backward=6, enable=12)
        self.right_motor = Motor(forward=13, backward=19, enable=18)
        
        # Actuators
        self.pump = OutputDevice(PIN_PUMP, active_high=True, initial_value=False)
        self.pan_servo = Servo(PIN_PAN)
        self.tilt_servo = Servo(PIN_TILT)
        
        # Thermal Sensor
        self.sensor = MLX90614()
        
        # Initial State
        self.pan_servo.mid()
        self.tilt_servo.mid()

    def set_chassis_speed(self, left_speed, right_speed):
        """Controls left and right track speeds (-1.0 to 1.0)."""
        if left_speed >= 0:
            self.left_motor.forward(left_speed)
        else:
            self.left_motor.backward(abs(left_speed))

        if right_speed >= 0:
            self.right_motor.forward(right_speed)
        else:
            self.right_motor.backward(abs(right_speed))

    def stop_chassis(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def run(self):
        logging.info("Starting Autonomous Fire Detection Loop...")
        try:
            while True:
                # 1. Sweep and Search
                for angle in range(-10, 11, 2):
                    servo_val = angle / 10.0  # Normalize -1.0 to 1.0
                    self.pan_servo.value = servo_val
                    time.sleep(0.05)

                    temp = self.sensor.read_object_temp()
                    logging.info(f"Scanning... Pan: {servo_val:.1f} | Temp: {temp:.2f}°C")

                    # 2. Trigger Suppression State
                    if temp >= FIRE_TEMP_THRESHOLD_C:
                        logging.warning(f"FIRE DETECTED ({temp:.2f}°C)! Halting chassis and deploying suppression...")
                        self.stop_chassis()
                        self.suppress_fire()
                        break

                # Drive forward slightly to scout area if clear
                self.set_chassis_speed(0.3, 0.3)
                time.sleep(0.5)
                self.stop_chassis()

        except KeyboardInterrupt:
            logging.info("Shutting down autonomous system safely...")
        finally:
            self.cleanup()

    def suppress_fire(self):
        """Engages water pump and sweeps nozzle until target cools down."""
        self.pump.on()
        while True:
            # Oscillation sweep to cover fire region
            for offset in [-0.2, 0.0, 0.2]:
                self.pan_servo.value = offset
                time.sleep(0.2)
                
            current_temp = self.sensor.read_object_temp()
            logging.info(f"Suppressing... Target Temp: {current_temp:.2f}°C")
            
            if current_temp < SAFE_TEMP_THRESHOLD_C:
                logging.info("Target temperature stabilized below threshold. Extinguished!")
                break

        self.pump.off()
        self.pan_servo.mid()

    def cleanup(self):
        self.stop_chassis()
        self.pump.off()
        self.pan_servo.detach()
        self.tilt_servo.detach()

if __name__ == "__main__":
    bot = AutonomousFireBrigade()
    bot.run()
