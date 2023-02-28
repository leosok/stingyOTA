import sys
sys.path.append('../stingy-ota')

from stingy_ota import StingyOTA

owner = 'leosok'
repo = 'erika-esp32'
path = 'tests'
branch = 'develop'

ota = StingyOTA(user=owner, repo=repo, branch=branch, subfolder=path)