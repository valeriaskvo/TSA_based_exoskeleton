class IMU():
    def __init__(self, i2c, imu_id=0, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.id = imu_id
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()
        self.val_names = ["AcX", "AcY", "AcZ", "Tmp", "GyX", "GyY", "GyZ"]
        self.vals = {key: 0 for key in self.val_names}

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        """
        returned in range of Int16
        -32768 to 32767
        """
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_data(self):
        raw_ints = self.get_raw_values()
        for i, key in enumerate(self.val_names):
            self.vals[key] = self.bytes_toint(raw_ints[i*2], raw_ints[i*2+1])
            if key == "Tmp":
                self.vals[key] = self.vals[key] / 340.00 + 36.53
        return self.vals


    def print_data(self):
        self.get_data()
        str_out = f"ID: {self.id}"
        for i, key in enumerate(self.val_names):
            str_out += "\t"
            if key == "Tmp":
                str_out += f"{key} {self.vals[key]:5.2f}"
            else:
                str_out += f"{key} {self.vals[key]:5}"
        print(str_out)

    def test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            self.print_data()
            sleep(0.05)
