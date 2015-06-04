import time

class GPIO:

    gpio_prefix_short = "/sys/class/gpio/"
    gpio_prefix = "/sys/kernel/debug/gpio_debug/"

    def __init__(self, pin):
        self.pin = pin

    def access(self, property):
        return self.gpio_prefix + "gpio" + str(self.pin) + "/current_" + property

    def writeProperty(self, property, value):
        f = open(self.access(property), "wb")
        f.write(str(value))
        f.close()

    def readProperty(self, property, length):
        f = open(self.access(property), "r")
        st = f.read(length)
        f.close()
        return st

    def enable(self, export):
        # check if export or unexport:
        v = "" if export else "un"
        f = open(self.gpio_prefix_short + v + "export", "wb")
        f.write(str(self.pin))
        f.close()

    def export(self):
        self.enable(1)

    def unexport(self):
        self.enable(0)

    def setDir(self, output):
        direction = "out" if output else "in"
        self.writeProperty("direction", direction)

    def setValue(self, value):
        val = "high" if value else "low"
        self.writeProperty("value", val)

    def getValue(self):
        return self.readProperty("value", 3)

    def setPinmux(self, mode):
        self.writeProperty("pinmux", mode) # use string for mode, like "mode0"

    def setPullmode(self, mode):
        self.writeProperty("pullmode", mode)

    def enableOverrideOutDir(self, en):
        direction = "override-enable" if en else "override-disable"
        self.writeProperty("override_outdir", direction)

    def enableOverrideOutVal(self, en, value = 0):
        if en:
            if value:
                val = "override-high"
            else:
                val = "override-low"
        else:
            val = "no-override"

        self.writeProperty("override_outval", val)

    def toggleValue(self):
        current_value = True if self.getValue() == "hig" else False
        self.setValue(not current_value)
        self.setValue(current_value)

    def initCS(self):
        #self.unexport() # unexport
        #self.export() # export
        self.setDir(1)
        self.setPinmux("mode0")
        self.setPullmode("nopull")
        self.enableOverrideOutVal(0)
        self.enableOverrideOutDir(1)
        #self.enableOverrideOutVal(1)


pin1 = GPIO(12)
pin2 = GPIO(13)
pin3 = GPIO(182)

b = True
delay = 0.5

while True:
	pin1.setValue(b)
	time.sleep(delay)
	pin1.setValue(not b)
	pin2.setValue(b)
	time.sleep(delay)
	pin2.setValue(not b)
	pin3.setValue(b)
	time.sleep(delay)
	pin3.setValue(not b)

	print("Tick!")
