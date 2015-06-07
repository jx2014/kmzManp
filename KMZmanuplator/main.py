from KMZmanuplator import KMZ

FPL_weakRF_all = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\RF_weakRF.txt"
FPL_weakRF_8 = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\FPL_weakRF_8.txt"
KMZ_file = r"C:\Users\jxue\Documents\Projects_LocalDrive\FPL Units\Map\lorenzo-fpl-mia-2015-06-01--23-35-29.meters-bystate.kmz"

newKMZ = KMZ(target = FPL_weakRF_all, kmzfile = KMZ_file)

#newKMZ.renExt(KMZ_file, 'zip')

#newKMZ.Unzip(newKMZ.kmzFile)
newKMZ.TestFunc()




