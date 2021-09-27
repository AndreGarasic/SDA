import math
import xml.etree.cElementTree as ET

def GenerateeXMl(fileName) :
    root = ET.Element("additional")
    tree = ET.ElementTree(root)
    e1 = ET.Element("routes")
    root.append(e1)

    e2 = ET.SubElement(e1, "vType", {'id':'CAR', 'IcKeepRight':'0'})



    e3 = ET.Element("tazs")
    root.append(e3)
    e4 = ET.SubElement(e3, "taz", {'id': '0', 'shape': '0'})


    # e5 = ET.SubElement(e4, "tazSink", {'id':'0', 'weight':'xx'})




    with open(fileName, "wb") as files :
        tree.write(files)

if __name__ == "__main__":
    GenerateeXMl("Tazproba.xml")


