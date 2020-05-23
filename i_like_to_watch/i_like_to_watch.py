from skyfield.api import EarthSatellite, load
from pwn import *


ts = load.timescale()
## Start Connection
r = remote('watch.satellitesabove.me', 5011)
log.info(r.recvuntil("\n").decode())

## Send Ticket
r.sendline("victor7694yankee:GCHDoBeg13q5bL4Vtzqmye5w8CGybi_apWnPt3DYn_WyBIJjDQnulaqsEUbm5VpYVw")
log.info(r.recvuntil('\n\n').decode())
r.recvline()

line1 = r.recvline()
line2 = r.recvline()

satellite = EarthSatellite(line1, line2, 'HSC', ts)
datetime = ts.utc(2020, 3, 26, 21, 54, 36)

geocentric = satellite.at(datetime)
subpoint = geocentric.subpoint()
print("lat: ", subpoint.latitude)
print("long: ", subpoint.longitude)
print("elv: ", int(subpoint.elevation.m))
r.interactive()