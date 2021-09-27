from django.http import HttpResponse
from django.shortcuts import render
import sumolib
import math
import xml.etree.cElementTree as ET
import os
from .models import Taz_model

# Create your views here.
def home_view(request, *args, **kwargs):
    """print(args, kwargs)
    print(request.user)"""
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "home.html", {})

def spremi_view(request, *args, **kwargs):
    if request.method == "GET":
            context = {}
            os.chdir("C:\\ag\\SUMO\\master")
            os.system("od2trips -c od2trips.config.xml && duarouter -c "
                      "duarcfg.trips2routes.duarcfg && sumo-gui "
                      "-c"+"C:\\ag\\SUMO\\master\\rotor.sumocfg"+" --device.rerouting.probability 0.7")
    return render(request, "ok.html", context=context)

def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})

def ok_view(request, *args, **kwargs):
    return render(request, "ok.html", {})

def map_view(request, *args, **kwargs):
    return render(request, "karta.html", {})

def taz_maker(request, *args, **kwargs):
    try:
        context = {}

    except Exception as e:
     context['status'] = 'Something went wrong!'
     return render(request, "taz_solver.html", context=context)
    else:
        return render(request, "taz_maker.html", context=context)


def taz_view(request, closestEdge=None, *args, **kwargs):





 try:
    Ttree = ET.parse('Tazzone_ag.xml') #XML file open
    Troot = Ttree.getroot()
    tazs = Ttree.find('tazs')

    flownew = open("flownew_proba.od", "a")



    context = {}
    podaci = request.GET.get('koordinate', 0)
    upodaci = podaci.split(";")
    upodaci.pop()
    locations = []
    locations1 = []

    br_vozila = request.GET.get('vozila', 0)


    sc = upodaci[0].find(",")
    dt = upodaci[0].find(".")
    lat = float(upodaci[0][:dt+7])
    lon = float(upodaci[0][sc+1:sc+10])
    sc1 = upodaci[1].find(",")
    dt1 = upodaci[1].find(".")
    lat1 = float(upodaci[1][:dt1+7])
    lon1 = float(upodaci[1][sc1+1:sc1+10])


    upxa = lat + .001
    locations.append(upxa)
    upya = lon + .001
    locations.append(upya)
    upxb = lat - .001
    locations.append(upxb)
    upyb = lon - .001
    locations.append(upyb)

    upxa1 = lat1 + .001
    locations1.append(upxa1)
    upya1 = lon1 + .001
    locations1.append(upya1)
    upxb1 = lat1 - .001
    locations1.append(upxb1)
    upyb1 = lon1 - .001
    locations1.append(upyb1)




    edgekojitezanima,convertedlocations, shape_a= ClosestEdge(lat, lon,
                                                            locations)
    edgekojitezanima1, convertedlocations1, shape_b= ClosestEdge(lat1, lon1,
                                                         locations1)




    if edgekojitezanima is None:
        return
    else:
     ctr = len(tazs.findall('taz'))

     taz_src = ET.SubElement(tazs, "taz", attrib={"id" : str(ctr), 'color' :
         'red', 'shape' : shape_a})
     sourcetaz_src = ET.SubElement(taz_src, "tazSource", {'id': str(
         edgekojitezanima), 'weight' : '1'})
     sinktaz_src = ET.SubElement(taz_src, "tazSink", {'id': str(
         edgekojitezanima), 'weight' : '1'})

     ctr = ctr + 1
     taz_dst = ET.SubElement(tazs, "taz", attrib={"id": str(ctr), 'color':
         'blue', 'shape': shape_b})
     sourcetaz_dst = ET.SubElement(taz_dst, "tazSource", {'id': str(
         edgekojitezanima1), 'weight' : '1'})
     sinktaz_dst = ET.SubElement(taz_dst, "tazSink", {'id': str(
         edgekojitezanima1), 'weight' : '1'})






     Ttree.write("Tazzone_ag.xml")
     flownew.write("\n")
     flownew.write("\t"  + str(ctr-1) + "\t"  + str(ctr) +
                   "\t" + br_vozila)
     flownew.close()

     ctr = ctr + 1  # id counter za TAZ

     context['podaci'] = podaci
     context['locations'] = locations
     context['locations1'] = locations1
     context['convertedlocations'] = convertedlocations
     context['edge'] = edgekojitezanima




 except Exception as e:
    context['status'] = 'Something went wrong!'
    return render(request, "karta.html", context=context)
 else:
    return render(request, "taz_solver.html", context=context)






def ClosestEdge(lat, lon, locations):
    convertedlocations = [0, 0, 0, 0]
    net = sumolib.net.readNet('planet32.net.xml')
    xc, yc = net.convertLonLat2XY(lon, lat)
    Listasvih, x, y = [], [], []


    convertedlocations[0], convertedlocations[1] = net.convertLonLat2XY(
    locations[1], locations[0])
    convertedlocations[2], convertedlocations[3] = net.convertLonLat2XY(
    locations[3], locations[2])

    cva = str(convertedlocations[0]) + "," + str(convertedlocations[1])
    cvb = str(convertedlocations[2]) + "," + str(convertedlocations[3])
    cv_final = cva + " " + cvb
    #cvasr = cva.replace(",", "-")
    #cva = [''.join(convertedlocations[0 : 1])]
    #cvb = [''.join(convertedlocations[2: 3])]
    #cvc = cva + cvb


    tree = ET.parse('planet32.net.xml')
    root = tree.getroot()

    for junctions in root.findall('junction'):
        Listasvih.append(junctions.get('id'))
        x.append(float(junctions.get('x')))
        y.append(float(junctions.get('y')))

    Min = 9999999
    Xmin = 0
    Ymin = 0

    for i in x:
        Udaljenost = math.sqrt(math.pow((xc - i), 2) + math.pow((yc - y[x.index(i)]), 2))

        if Udaljenost < Min:
            Min = Udaljenost
            Xmin = i
            Ymin = y[x.index(i)]

    Index = 0

    for i in x:
        if i == Xmin and y[x.index(i)] == Ymin:
            Index = x.index(i)

    Junctionofinterest = Listasvih[Index]

    for edges in root.findall('edge'):
        if edges.get('from') == str(Junctionofinterest):
            edgekojitezanima = edges.attrib['id']

    return (edgekojitezanima, convertedlocations, cv_final)


