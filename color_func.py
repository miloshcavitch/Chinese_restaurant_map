def autoRGB(r,g,b):
    string = '#'
    rgb = []
    rgb.append( hex(r).split('x',1)[1] )
    rgb.append( hex(g).split('x',1)[1] )
    rgb.append( hex(b).split('x',1)[1] )
    for i, color in enumerate(rgb):
        if (len(color) > 2):
            print(r,g,b)
        if len(color) == 1:
            rgb[i] = '0' + color
    return string + rgb[0] + rgb[1] + rgb[2]

def valueLERP(value, min, max):
    value = value - min
    max = max - min
    val = int( (value / max) * 255)
    if val > 255:
        val = 255
    if val < 0:
        val = 0
    return val
