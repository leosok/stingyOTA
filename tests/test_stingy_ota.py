import sys
sys.path.append('../stingy-ota')

from stingy_ota import StingyOTA

owner = 'leosok'
repo = 'erika-esp32'
path = 'tests'
branch = 'test-data'

ota = StingyOTA(user=owner, repo=repo, branch=branch, subfolder=path)