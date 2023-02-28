# "from tests import run" to run all tests

print("Running tests...")
from . import test_wifi_helper # will connect to wifi
from . import test_stingy_ota # will check for updates
