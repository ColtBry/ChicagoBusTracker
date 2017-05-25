import math

class Bus(object):

    def __init__(self, info, timestamp):
        self.info = info
        self.info['coords'] = (float(info['lat']), float(info['lon']))
        self.info['c'] = info['c'][1:]

        self.info['speed']   = 0
        self.info['bearing'] = 0
        self.info['avg_speed'] = 0

        self.speed_list = []

        self.current_timestamp = timestamp

    def update(self, info, timestamp):
        avg_speed = 0

        self.last_location  = self.info['coords']

        self.info = info
        self.info['coords'] = (float(info['lat']), float(info['lon']))
        self.info['c'] = info['c'][1:]

        self.last_timestamp    = self.current_timestamp
        self.current_timestamp = timestamp

        speed = round(self.get_speed())
        bearing = self.get_bearing(self.info['coords'], self.last_location)

        if 5 < speed < 80:
            # Lower Limit on speed so stopping isn't factored into avg
            # Top speed because some of the GPSs are malfunctioning
            self.speed_list.append(speed)
            if len(self.speed_list) > 100:
                self.speed_list.pop(0)
            avg_speed = round(sum(self.speed_list)/len(self.speed_list), 2)

        self.info['speed']   = speed
        self.info['bearing'] = round(bearing, 1)
        self.info['avg_speed'] = avg_speed

    def get_speed(self):
        distance = self.get_distance(self.info['coords'], self.last_location)

        time_dif = self.current_timestamp - self.last_timestamp
        speed = (3600 / time_dif) * distance # 3600 == Seconds in an hour
        return speed

    def get_distance(self, coord1, coord2): # (Lat, Lon)
        # Calculates distance between two coordinates.
        # Code is from
        # http://www.johndcook.com/python_longitude_latitude.html
        phi1 = math.radians(90.0 - coord1[0])
        phi2 = math.radians(90.0 - coord2[0])

        theta1 = math.radians(coord1[1])
        theta2 = math.radians(coord2[1])

        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
               math.cos(phi1)*math.cos(phi2))

        if cos > 1:
            cos = 1

        arc = math.acos(cos)

        arc *= 3963.1676 # Radius of the Earth in Miles
        return arc

    def get_bearing(self, coord1, coord2):
        # http://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
        lon_dif = math.radians(coord2[1] - coord1[1]) 

        lat1 = math.radians(coord1[0])
        lat2 = math.radians(coord2[0])

        X = math.cos(lat2) * math.sin(lon_dif)

        Y = (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * 
             math.cos(lat2) * math.cos(lon_dif))

        bearing = math.degrees(math.atan2(X,Y))

        if bearing < 0:
            bearing += 360

        return bearing
