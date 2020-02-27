#-*-coding: utf-8 =*-
# R^2 = (x - x0)^2 + (y - y0)^2 + (z - z0)^2
#(x - x1) / (x2 - x1) = (y - y1) / (y2 - y1) = (z - z1) / (z2 - z1) = t
#(z - z1) / (z2- z1) = t ; t * (z2 - z1) + z1 = z
#x = x1 + t(x2 - x1)
#y = y1 + t(y2 - y1)
#z = z1 + t(z2 - z1)
#R^2 = (x1 + t(x2 - x1))^2 + (y1 + t(y2 - y1))^2 + (z1 + t(z2 - z1))^2
#R^2 = (x1 + t(x2 - x1) - x0)^2 + (y1 + t(y2 - y1) - y0)^2 + (z1 + t(z2 - z1) - z0)^2
#R^2 = x0^2 + x1^2 + y0^2 + y1^2 + z0^2 + z1^2 + t^2*x1^2 + t^2*x2^2 + t^2*y1^2 + t^2*y2^2 + t^2*z1^2 + t^2*z2^2 - 2*t*x1^2 - 2*t*y1^2 - 2*t*z1^2 - 2*x0*x1 - 2*y0*y1 - 2*z0*z1 - 2*t*x0*x2 - 2*t*y0*y2 - 2*t*z0*z2 - 2*x1*x2*t^2 - 2*y1*y2*t^2 - 2*z1*z2*t^2 + 2*t*x0*x1 + 2*t*x1*x2 + 2*t*y0*y1 + 2*t*y1*y2 + 2*t*z0*z1 + 2*t*z1*z2

def intersection(t1, t2 , x1, y1,  z1, x2, y2, z2):
    if t1 == None:
        return None, None
    elif t2 == None:
        xt1 = x1 + t1 * (x2 - x1)
        yt1 = y1 + t1 * (y2 - y1)
        zt1 = z1 + t1 * (z2 - z1)
        return [xt1, yt1, zt1], None
    else:
        xt1 = x1 + t1 * (x2 - x1)
        yt1 = y1 + t1 * (y2 - y1)
        zt1 = z1 + t1 * (z2 - z1)

        xt2 = x1 + t2 * (x2 - x1)
        yt2 = y1 + t2 * (y2 - y1)
        zt2 = z1 + t2 * (z2 - z1)
        return [xt1, yt1, zt1], [xt2, yt2, zt2]

def quadraticEquation(a, b, c):
    D = b ** 2 - 4 * a * c
    if D < 0:
        return None, None
    elif D == 0:
        return (-b + math.sqrt(D))/(2*a), None
    elif D > 0:
        return (-b + math.sqrt(D))/(2*a), (-b - math.sqrt(D))/(2*a)

def countCoefficient(x0, y0, z0, R, x1, y1, z1, x2, y2, z2):
    a = x1 ** 2 + x2 ** 2 + y1 ** 2 + y2 ** 2 + z1 ** 2 + z2 ** 2 - 2 * x1 * x2 - 2 * y1 * y2 - 2 * z1 * z2
    b = - 2 * x1 ** 2 - 2 * y1 ** 2 - 2 * z1 ** 2 - 2 * x0 * x2 - 2 * y0 * y2 - 2 * z0 * z2 + 2 * x0 * x1 + 2 * x1 * x2 + 2 * y0 * y1 + 2 * y1 * y2 + 2 * z0 * z1 + 2 * z1 * z2
    c = x0 ** 2 + x1 ** 2 + y0 ** 2 + y1 ** 2 + z0 ** 2 + z1 ** 2 - R ** 2 - 2 * x0 * x1 - 2 * y0 * y1 - 2 * z0 * z1
    return a, b, c

def findObjectInStr(str, objectName):
    objectStarts = str.find('{0}'.format(objectName) + ': {') + len('{0}'.format(objectName) + ' :{')
    objectEnds = str.find("}", str.find('{0}'.format(objectName) + ': {'))
    return str[objectStarts:objectEnds]

path = "coordinatsTask2"

def parseFile(path):
    try:
        input = open(path, 'r').read()
    except:
        print("Неверно указан путь к файлу")
        sys.exit(1)
    lineCoords = findObjectInStr(input, "line")
    sphere = findObjectInStr(input, "sphere")
    lineCoords = list(map(float, lineCoords.replace('[','').replace(']', '').split(',')))
    coordsSphereCenter = list(map(float, sphere[sphere.find('center: [') + len('center: [') : sphere.find("]", sphere.find('center: [') + len('center: [')) ].split(',')))
    if sphere.find("center") > sphere.find("radius"):
        coordsSphereRadius = float(sphere[sphere.find("radius: ") + len("radius: "):sphere.find(",")])
    else:
        coordsSphereRadius = float(sphere[sphere.find("radius: ") + len("radius: "):])

    return coordsSphereCenter, coordsSphereRadius, lineCoords

def showIntersection(intersectionFirst, intersectionSecond):
    if intersectionFirst == None:
        return "Коллизий не найдено"
    elif intersectionSecond == None:
        return " ".join(list(map(str, intersectionFirst)))
    else:
        return " ".join(list(map(str, intersectionFirst))) + "\n" + " ".join(list(map(str, intersectionSecond)))

if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if (len(sys.argv) == 1):
        coordsSphereCenter, coordsSphereRadius, lineCoords = parseFile(sys.argv[0])

        a, b, c = countCoefficient(coordsSphereCenter[0], coordsSphereCenter[1], coordsSphereCenter[2],
                                   coordsSphereRadius, lineCoords[0], lineCoords[1], lineCoords[2], lineCoords[3],
                                   lineCoords[4], lineCoords[5])

        t1, t2 = quadraticEquation(a, b, c)

        intersectionFirst, intersectionSecond = intersection(t1, t2, lineCoords[0], lineCoords[1], lineCoords[2],
                                                             lineCoords[3], lineCoords[4], lineCoords[5])

        print(showIntersection(intersectionFirst, intersectionSecond))



