import os
from GPIO import GPIO

class ReachLED:

    pwm_prefix = "/sys/class/pwm/pwmchip0/"

    def __init__(self):
        self.pins = [GPIO(12), GPIO(13), GPIO(182)] # green, red, blue

        # channel numbers
        self.pwm_channels = [0, 1, 2] # green, red, blue

        # first, we need to change the pin's pinmux to mode1
        for pin in self.pins:
            pin.setPinmux("mode1")

        # then, export the 3 pwn channels if needed
        for ch in self.pwm_channels:
            if not os.path.exists(self.pwm_prefix + "/pwm" + str(ch)):
                with open(self.pwm_prefix + "export", "w") as f:
                    f.write(str(ch))

        # enable all of the channels
        for ch in self.pwm_channels:
            with open(self.pwm_prefix + "pwm" + str(ch) + "/enable", "w") as f:
                f.write("1")

        # set period
        for ch in self.pwm_channels:
            with open(self.pwm_prefix + "pwm" + str(ch) + "/period", "w") as f:
                f.write("1000000")

        # set our yellowish white as default
        self.setDutyCycle(0, 100)
        self.setDutyCycle(1, 100)
        self.setDutyCycle(2, 100)

    def setDutyCycle(self, channel, percentage):
        # 0% = 1000000
        # 100% = 0

        duty_value = (100 - percentage) * 10000

        with open(self.pwm_prefix + "pwm" + str(channel) + "/duty_cycle", "w") as f:
            f.write(str(duty_value))


# led = ReachLED()