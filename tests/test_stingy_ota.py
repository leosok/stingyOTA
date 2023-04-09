import sys
import os
sys.path.append('../stingy-ota')

from stingy_ota import StingyOTA

owner = 'leosok'
repo = 'stingyOTA'
path = 'tests'
branch = 'test-data'

ota = StingyOTA(user=owner, repo=repo, branch=branch, subfolder=path)
if ota.has_new_version:
    print("OTA-TEST: has_new_version = True")
    print(f"OTA-TEST: Current Remote version: ({branch}) {ota.remote_version}")
    print(f"OTA-TEST: Current Local version: {ota._get_local_hash()}")
    ota.update()
else:
    print("OTA-TEST: Remote version == Current Version")
    os.remove(ota.version_file) # Next time we want to download again