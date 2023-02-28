# Add a secrety.py file with the following content
# SSID = "your_ssid"
# PASSWORD = "your_password"

# Import the secrets file
from .secrets import SSID, PASSWORD
import sys
sys.path.append('../stingy-ota')
import wifi_helper


wifi_helper.WifiHelper(SSID, PASSWORD).connect()