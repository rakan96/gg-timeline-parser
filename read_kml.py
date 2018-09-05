#!/usr/bin/env python

# Input parameters
# ================
# dates to be taken into account (can be None => all dates)
dates = ['2018-08-02', '2018-08-03', '2018-08-04']
# file to open
file_name = "all.kml"
# no more input parameters after this line

f = open(file_name)

header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
  <Document>
    <open>1</open>
    <Folder>
"""
footpage = """
    </Folder>
  </Document>
</kml>"""

# hashmap with all points found
# {
#   '2018-08-02': [ ['2018-08-02T23:58:56Z', '-118 34 0'], ... ],
#   '2018-08-03': [ ['2018-08-03T00:00:00Z', '-120 33 200'], ... ],
# }
points = {}

import xml.etree.ElementTree as ET
tree = ET.parse('all.kml')
root = tree.getroot()
timestamp = ""
date = ""

for child in root[0][0][1]:
    if child.tag == "{http://www.opengis.net/kml/2.2}when":
        timestamp = child.text
        date = timestamp[0:10]
        if dates and date not in dates:
            date = ""
            continue
        if date not in points:
            points[date] = []
    if date and child.tag == "{http://www.google.com/kml/ext/2.2}coord":
        coord = ",".join(child.text.split(" ")[0:2])
        points[date].append([timestamp, coord])

for key in points.keys():
    print("Writing {}.kml".format(key))
    f = open("{}.kml".format(key), "w")
    f.write(header)
    for gx in list(reversed(points[key])):
        f.write("      <Placemark>\n")
        f.write("        <TimeStamp>\n")
        f.write("          <when>{}</when>\n".format(gx[0]))
        f.write("        </TimeStamp>\n")
        f.write("        <Point>\n")
        f.write("          <coordinates>{}</coordinates>\n".format(gx[1]))
        f.write("        </Point>\n")
        f.write("      </Placemark>\n")
    f.write(footpage)
    f.close()
