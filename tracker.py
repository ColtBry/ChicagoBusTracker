import xml.etree.ElementTree as ET
import requests
import time

import atexit
from os import _exit

import template_operations as template_ops
from Bus import Bus

TEMPLATE_FILE = 'templates.txt'
KML_FILE = 'TrackKML.kml'

API_URL = 'http://ctabustracker.com/bustime/map/getBusesForRouteAll.jsp'

def exit_handler():
    print('\nStopped')
    _exit(1)

def main():

    def return_url_xml(url):
        data = session.get(url).text.replace('&', '')
        return ET.fromstring(data)

    def xml_to_dicts(xml):
        dictionaries = []

        for node in xml:
            element = {}
            for tag in node:
                element[tag.tag] = tag.text
            dictionaries.append(element)
        return dictionaries

    def write_kml_file(buses, templates, path):
        with open(path, 'w') as file:
            file.write(templates['Header'])
            for bus in buses:
                file.write(templates['Point'].format(**bus))

            file.write(templates['Footer'])

    templates = template_ops.get_from_file(TEMPLATE_FILE)
    session = requests.session()

    active_buses = {}

    while 1:
        timestamp = int(time.time())

        xml = return_url_xml(API_URL)
        buses = xml_to_dicts(xml)

        inactive_buses = list(active_buses.keys())

        for bus in buses:
            try:
                active_buses[bus['id']].update(bus, timestamp)
                inactive_buses.remove(bus['id'])
            except KeyError:
                active_buses[bus['id']] = Bus(bus, timestamp)

        for bus_id in inactive_buses: # Removes buses that aren't active
            active_buses.pop(bus_id)

        write_kml_file(buses, templates, KML_FILE)

        time.sleep(30) # 

atexit.register(exit_handler)

print('\nRunning... see the ReadMe for help.')
print('\nPress Ctrl+C to exit.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass