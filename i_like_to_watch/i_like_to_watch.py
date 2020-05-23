# from skyfield.api import EarthSatellite, load, Topos
from skyfield import api
from pwn import *

def dms2dd(dms):
	degMinSec = dms.split(' ')
	return str(float(degMinSec[0][:-3]) + float(degMinSec[1][:-1])/60 + float(degMinSec[2][:-1])/3600)


ts = api.load.timescale()


# ts = load.timescale()
## Start Connection
r = remote('watch.satellitesabove.me', 5011)
log.info(r.recvuntil("\n").decode())

## Send Ticket
r.sendline("victor7694yankee:GCHDoBeg13q5bL4Vtzqmye5w8CGybi_apWnPt3DYn_WyBIJjDQnulaqsEUbm5VpYVw")
log.info(r.recvuntil('\n\n').decode())
r.recvline()

line1 = r.recvline().decode()
line2 = r.recvline().decode()

satellite = api.EarthSatellite(line1, line2, 'HSC', ts)
datetime = ts.utc(2020, 3, 26, 21, 54, 36)

geocentric = satellite.at(datetime)
subpoint = geocentric.subpoint()

lat = str(subpoint.latitude)
longitude = str(subpoint.longitude)
alt = int(subpoint.elevation.m)
r.recvline()
link = r.recvline().decode().split(' ')[10]
r.recvline()

log.info("lat: "+str(lat))
log.info("long: "+ str(longitude))
log.info("elv: "+ str(alt))
log.info("Link: " + link)
#
      	
r.close()
kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Folder>
    <name>HackASatCompetition</name>
    <visibility>0</visibility>
    <open>0</open>
    <description>HackASatComp1</description>
    <NetworkLink>
      <name>View Centered Placemark</name>
      <visibility>0</visibility>
      <open>0</open>
      <description>This is where the satellite was located when we saw it.</description>
      <refreshVisibility>0</refreshVisibility>
      <flyToView>0</flyToView>
      <LookAt id="ID">
      	<gx:TimeStamp>
        	<when>2020-03-26T21:54:36</when>
        </gx:TimeStamp>
        <!-- specific to LookAt -->
        <longitude>"""+str(dms2dd(longitude))+"""</longitude>            	<!-- kml:angle180 -->
        <latitude>"""+str(dms2dd(lat))+"""</latitude>              	<!-- kml:angle90 -->
        <altitude>"""+str(alt)+"""</altitude>              		<!-- double -->
        <heading>61.9928</heading>                <!-- kml:angle360 -->
        <tilt>83.3154</tilt>                     <!-- kml:anglepos90 -->
        <range>15.48919755219337</range>                     <!-- double -->
        <altitudeMode>clampToGround</altitudeMode>
      </LookAt>
      <Link>
        <href>"""+str(link)+"""</href>
        <refreshInterval>1</refreshInterval>
        <viewRefreshMode>onStop</viewRefreshMode>
        <viewRefreshTime>1</viewRefreshTime>
        <viewFormat>BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth];CAMERA=[lookatLon],[lookatLat],[lookatRange],[lookatTilt],[lookatHeading];VIEW=[horizFov],[vertFov],[horizPixels],[vetrPixels],[terrainEnabled]</viewFormat>
      </Link>
    </NetworkLink>
  </Folder>
</kml>"""


f = open("hsc.kml", "w")
f.write(kml)
f.close()

print(kml)