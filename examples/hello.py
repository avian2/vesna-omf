import logging
from vesna.omf import ALH

logging.basicConfig(level=logging.INFO)
coor = ALH()
print coor.get("hello")
