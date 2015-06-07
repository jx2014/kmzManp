from KMZmanuplator import KMZ

def ColorD2H(dec, alpha=255):
    '''
        RGBA
        Red=255 Green=18 Blue=25 alpha=255
        i.e. ColorD2H(255018025, alpha=255)   
    '''
    if len(str(dec)) !=9 or len(str(alpha)) !=3:
        print "Must use three digits to represent each color and alpha channel"
        return 0
    else:
        red = dec / 1000000
        green = (dec  - red * 1000000) / 1000
        blue = (dec - red * 1000000 - green * 1000)        
    
    if red > 255 or green > 255 or blue > 255:
        print "Each color must be less than or equal to 255"
        return 0
    else:
        red = hex(red).split('x')[1].split('L')[0]
        green = hex(green).split('x')[1].split('L')[0]
        blue = hex(blue).split('x')[1].split('L')[0]
        alpha = hex(alpha).split('x')[1].split('L')[0]
        
        return red+green+blue+alpha
    
    

FPL_weakRF_all = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\RF_weakRF.txt"
FPL_weakRF_8 = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\FPL_weakRF_8.txt"
KMZ_file = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\lorenzo-fpl-mia-2015-06-01--23-35-29.meters-bystate.kmz"

hightLight = ColorD2H(255255128) # yellow

newKMZ = KMZ(target=FPL_weakRF_all, color=hightLight, kmzfile=KMZ_file, visible=0)

#newKMZ.renExt(KMZ_file, 'zip')

#newKMZ.Unzip(newKMZ.kmzFile)
newKMZ.TestFunc()




