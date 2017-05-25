# -*- coding: cp1252 -*-

import urllib
import time
import math
from xml.etree.ElementTree import parse


def distance_on_unit_sphere(lat1, long1, lat2, long2):#Calculates distance between two coords.
  #Slighty modified code from http://www.johndcook.com/python_longitude_latitude.html
  degrees_to_radians = math.pi/180.0
  phi1 = (90.0 - lat1)*degrees_to_radians
  phi2 = (90.0 - lat2)*degrees_to_radians
  theta1 = long1*degrees_to_radians
  theta2 = long2*degrees_to_radians
  cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
       math.cos(phi1)*math.cos(phi2))
  if cos > 1:
    cos = 1
  arc = math.acos( cos )
  arc *= 3963.1676
  return (3600 / dif) * arc


def Get_Bearing(y1,x1,y2,x2):
  global bears
  
  bearing = int(90 - (180/math.pi)*math.atan2(y2-y1,x2-x1))

  if bearing < 0:
    bearing += 360 + bearing
    
  last = bearing
  
  if bearing > 180:
    bearing -= 180
  elif bearing == 180:
    bearing = 0
  elif bearing < 180:
    bearing += 180

  bears = bearing
  return str(bearing)

coords = {}
times = time.clock()
dif = 0
dis = 0
bears = "180"
first = True
avg = 0
debug = 0
wait = 30

tm = input("[How long?]")

if tm == "debug":
  Debug = 1
  tm = 20
  wait = 10
else:
  tm = int(int(tm) * (60/wait))

for i in range(1, tm):
  dif = time.clock() - times
  times = time.clock()

  print("\nRequesting")#Requests and parses the XML request.
  f = open("rt22.xml", "wb")
  data = f.write(urllib.urlopen("http://ctabustracker.com/bustime/map/getBusesForRouteAll.jsp").read() )
  f.close()
  doc = parse("rt22.xml")
  print("Done\n")

  #print("name, latitude, longitude, speed\n")
  
  f = open("Track.kml","w")
  f.write('<?xml version="1.0" encoding="utf-8" ?>\n')
  f.write('<kml xmlns="http://earth.google.com/kml/2.2">\n')
  f.write("<Document>")
  f.write("<name>test kml</name>")
  f.write('<Schema name="test kml"></Schema>')
  f.write("<Folder>\n")
    
  for bus in doc.findall('bus'):
    bear = "180"
    bears = "180"
    op = bus.findtext('op')#If bus ID doesn't exist it creates it.
    if "lat" + op not in coords.keys():
      coords["First" + op] = True
      coords["con" + op] = False
      coords["lat" + op] = 0
      coords["lon" + op] = 0
      coords["rt" + op] = ""
      coords["dire" + op] = ""
      coords["total" + op] = 0
      coords["count" + op] = 0
            
    if coords["con" + op] == 0:#Makes sure if duplicate ID's that it doesn't run twice.
      coords["con" + op] = True
        
      if op != "N/A":#Checks for a valid working GPS                  
        if coords["First" + op] == False:#Calculates the speed.
          lat = float(bus.findtext('lat'))
          lon = float(bus.findtext('lon'))
          if coords["lat" + op] != 0 and lat != 0:
            spd = distance_on_unit_sphere(float(coords["lat" + op]), float(coords["lon" + op]), lat, lon )
            bears = Get_Bearing(float(coords["lat" + op]), float(coords["lon" + op]), lat, lon)
        else:
          spd = 0   #If first run, don't calculate speed.

        coords["lat" + op] = str(float(bus.findtext('lat')))#Saves info
        coords["lon" + op] = str(float(bus.findtext('lon')))
        coords["rt" + op] = bus.findtext('rt')
        coords["dire" + op] = bus.findtext('pd')
        coords["First" + op] = False

        avg = 0
        if spd > 100:
          print(op)
        if int(spd) > 5 and int(spd) < 100:
          coords["total" + op] += int(spd)
          coords["count" + op] += 1

        if coords["total" + op] > 0:
          avg = coords["total" + op] / coords["count" + op]
          
        
        f.write('    <Placemark name=\"' + op + '">\n')#Creates the points.
        f.write("       <Style>")
        f.write("           <IconStyle>\n")
        f.write("               <Icon>")
        f.write("                   <href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href>\n")
        f.write("               </Icon>")
        f.write("               <heading>" + bears + "</heading>")
        f.write("               <color>d10000ff</color>")
        f.write("               <scale>.6</scale>")
        f.write("           </IconStyle>\n")
        f.write("           <LabelStyle>")
        f.write("               <scale>.7</scale>")
        f.write("           </LabelStyle>")
        f.write("       </Style>\n")
        f.write('       <name>' + op + '</name>')
        f.write("       <description> Speed: " + str(int(spd)) + " MPH\n            Avg Spd: " + str(int(avg)) + " MPH\n            Route: " + coords["rt" + op] + "\n            Direction: " + coords["dire" + op] + "\n            Bearing: " + bears + "° \n        </description>\n")
        f.write("       <Point>\n")
        f.write("           <coordinates>" + str(coords["lon" + op] + ",") + str(coords["lat" + op] + ",0") + "</coordinates>\n")
        f.write("       </Point>\n")
        f.write("    </Placemark>\n")               #f.write(str(op + "," + coords["lat" + op] + "," + coords["lon" + op] + "," + str(int(spd)) ) + "," + "\n" )

        #print(str(int(spd)))

        #print(op + "," + coords["lat" + op] + "," + coords["lon" + op] + "," + str(int(spd)))


  f.write("</Folder>\n")
  f.write("</Document>")
  f.write("</kml>\n")
  f.close()

  count = 0
  for bus in doc.findall("bus"):#Resets the value used to check for repeats.
    count += 1
    op = bus.findtext('op')
    coords["con" + op] = False

  #print("\n" + str(elapsed) + " Seconds\n")
  #print(str(elapsed1 + 5) + " Seconds\n")
  print("\nActive Buses: " + str(count))
   
  time.sleep(wait)
