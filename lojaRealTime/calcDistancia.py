import math
from geopy.distance import geodesic

def distance(lng_A, lat_A, lng_B, lat_B):
    """R = 6371.004
    pi = 3.141592654

    Mlng_A = lng_A
    Mlat_A = 90 - lat_A

    Mlng_B = lng_B
    Mlat_B = 90 - lat_B

    C = math.sin(Mlat_A*pi/180) * math.sin(Mlat_B*pi/180) * math.cos((Mlng_A - Mlng_B)*pi/180) +math.cos(Mlat_A*pi/180) * math.cos(Mlat_B*pi/180)
    Distance = R * math.acos(C)
""" 
    puntoA = (lat_A, lng_A)
    puntoB = (lat_B, lng_B)
    ditancia = geodesic(puntoA, puntoB).km
    
    velocidad = ditancia / 0.05
    
    return ditancia, velocidad

d = distance(-79.200572, -4.010026,-79.19758, -4.003007)

print("La distancia es: " + str(round(distancia[0], 2)))

, "velocidad" : round(distancia[1],2)
