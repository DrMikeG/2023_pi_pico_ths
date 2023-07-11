# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht
from adafruit_onewire.bus import OneWireBus
import adafruit_ds18x20




# Initial the dht device, with data pin connected to:
print("Creating Temp and Humidity sensor DHT11")
dhtDevice = adafruit_dht.DHT11(board.GP16)
print("Done")

print("Creating OW bus")
ow_bus = OneWireBus(board.GP26)
print("Created")

print("Scanning bus")
devices = ow_bus.scan()
print("Scan complete. {} device(s) found".format( len(devices) ))

# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
#for device in devices:
#    print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))

ds18b20Defined = False

if len(devices) > 0:
    print("Defining DS18x20 using device[0]")
    ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])
    ds18b20Defined = True
    print("Done");

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        if ds18b20Defined:
            print('Temperature: {0:0.3f} °C'.format(ds18b20.temperature))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)





