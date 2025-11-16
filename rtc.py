from machine import I2C, Pin
import time

# Initialize I2C with slower speed and delay
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=100000)
time.sleep(0.1)  # Critical for clone modules!

DS3231_ADDR = 0x68

def bcd_to_decimal(bcd):
    """Convert Binary-Coded Decimal to normal decimal"""
    return (bcd >> 4) * 10 + (bcd & 0x0F)

def decimal_to_bcd(decimal):
    """Convert normal decimal to Binary-Coded Decimal"""
    return ((decimal // 10) << 4) | (decimal % 10)

def set_time(year, month, day, hour, minute, second):
    """Set the RTC time - only need to do this once"""
    data = bytearray(7)
    data[0] = decimal_to_bcd(second)
    data[1] = decimal_to_bcd(minute)
    data[2] = decimal_to_bcd(hour)
    data[3] = decimal_to_bcd(1)  # day of week (1-7)
    data[4] = decimal_to_bcd(day)
    data[5] = decimal_to_bcd(month)
    data[6] = decimal_to_bcd(year - 2000)
    i2c.writeto_mem(DS3231_ADDR, 0x00, data)
    print("Time set successfully!")

def read_time():
    """Read time from the RTC"""
    data = i2c.readfrom_mem(DS3231_ADDR, 0x00, 7)
    second = bcd_to_decimal(data[0] & 0x7F)  # Mask oscillator bit
    minute = bcd_to_decimal(data[1])
    hour = bcd_to_decimal(data[2] & 0x3F)    # Mask 12/24 hour bits
    day = bcd_to_decimal(data[4])
    month = bcd_to_decimal(data[5] & 0x1F)   # Mask century bit
    year = bcd_to_decimal(data[6]) + 2000
    return (year, month, day, hour, minute, second)

# Set the current time (only need to run once)
set_time(2025, 11, 15, 18, 45, 0)

# Main loop - display time every second
while True:
    year, month, day, hour, minute, second = read_time()
    print(f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
    time.sleep(1)


