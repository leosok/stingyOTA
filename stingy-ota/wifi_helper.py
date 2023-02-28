import network, time

class WifiHelper:
    def __init__(self, sid, password):
        self.ssid = sid
        self.password = password

    def connect(self):
        # Set up Wi-Fi connection
        print(f"Connecting to Wi-Fi network with SSID: {self.ssid} and password: {self.password}")

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)


        # Wait for connection to be established, limit for 10 seconds
        start = time.time()
        while not sta_if.isconnected():
            if time.time() - start > 10:
                print("TIMEOUT - ERROR: Connection to Wi-Fi network timed out. Check your SSID and password.")
                break
            else:
                time.sleep(0.5)

        # Print connection details
        print("Connected to Wi-Fi network with IP address:", sta_if.ifconfig()[0])

            
       
       