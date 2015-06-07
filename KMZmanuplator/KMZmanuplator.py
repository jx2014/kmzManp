import re
import os
import zipfile
from lxml import etree
from pykml import parser
from pykml.factory import KML_ElementMaker as KML


class KMZ():
    def __init__(self, target, kmzfile, color='ff0000ff', scale=1.0, visible=1, kmlremove = True):
        self.mainDir = os.path.dirname(kmzfile)
        #self.kmzFileNameOnly = os.path.basename(kmzfile) #get file name of the kmz file
        self.kmzFile = kmzfile # this is the kmz file with its full path
        self.macFile = target # target is the mac address data file, full path included, which should be the same as kmz file
        self.kmlList = []
        self.kmlPlacemarkColor = color
        self.kmlPlacemarkScale = scale
        self.kmlOtherPlacemarkVisible = visible # by default, turn off all other place mark
        self.removeKmls = kmlremove
        
        
        # load target mac ID to a list
        self.macList = []
        with open(self.macFile) as fn:
            for mac in fn.readlines():
                self.macList.append(mac.rstrip('\n'))
        # remove duplicated macs
        self.macList = list(set(self.macList))
        self.macList = filter(None, self.macList)
    
    # rename file extension KMZ to zip and vise versa
    def RenExt(self, fn, newExt):
        fileName, ext = os.path.splitext(fn)
        newFileName = '.'.join([fileName, newExt])
        os.rename(fn, newFileName)
        return newFileName
    
    # unzip the kmz file, also generate a list of zip file content to self.kmzList
    def Unzip(self, kmzfile):
        '''
            1. rename the kmz file to zip file
            2. unzip the zip file
            3. rename the zip file back to kmz file
        '''
        self.zipFilePath = os.path.dirname(kmzfile)
        
        fn = self.RenExt(kmzfile, 'zip')
    
        with zipfile.ZipFile(fn) as zf:
            for member in zf.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789                
                self.kmlList.append(member.filename) # save the kml filenames
                words = member.filename.split('/')            
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''): 
                        continue
                    path = os.path.join(self.zipFilePath, word)
                zf.extract(member, self.zipFilePath)
        
        self.RenExt(fn, 'kmz')
    
    # separate file name and extension and return dir, filename, and extension
    def DirNameExt(self, fn):
        dirName = os.path.dirname(fn)
        fileName = os.path.basename(fn)
        fileNameOnly, ext = os.path.splitext(fileName)                
        return dirName, fileNameOnly, ext, fileName
    
    # generate a new name for the modified zip file
    def NameGen(self, target, kmzfile):
        '''
            target is the full path of the data file that contents a list of mac id
            kmzfile is the full path of the kmz file, aka the zip file that contain the google map kml files. 
        '''
        dirname, macDataFile, macext, filename = self.DirNameExt(target)
        dirname, kmzFileOnly, ext, filename = self.DirNameExt(kmzfile)
        newKmzName = '_'.join([kmzFileOnly, macDataFile, macext.strip('.')]) #join kmz file name and mac data file
                                                                    #i.e lorenzo-fpl-mia-2015-06-01--23-35-29.meters-bystate_RF_WeakRF_txt
        newKmzName = '.'.join([newKmzName, 'kmz']) # give this new kmz file its extension back
        newKmzName = '\\'.join([dirname, newKmzName])
        
        return newKmzName
    
    # create the new zip file from the file list
    def NewZip(self, newKmzFileName, zipfiles = []):
        '''
            1. newKmzFileName must be the full path
            2. extract directory from newKmzFileName
            3. append each file to be ziped in the list with the directory
            4. create ZIP file
        '''
        fileList = zipfiles[:]
        dirname, fileNameOnly, ext, fileName = self.DirNameExt(newKmzFileName)
        for i, filename in enumerate(fileList):
            fileList[i] = '\\'.join([dirname, filename])
        
        print '...creating ZIP file %s in %s' % (fileNameOnly, dirname)
        
        zipFile = zipfile.ZipFile(newKmzFileName, mode='w')
        try:
            for i, n in enumerate(fileList):
                print '   adding %s' % n
                zipFile.write(n, arcname=os.path.basename(n), compress_type=zipfile.ZIP_DEFLATED)
        finally:
            print '...Zip finished...'
            zipFile.close
    
    # parser kml file from the kmlFile list
    def KmlParser(self):
        # test if kml list is empty
        if len(self.kmlList) == 0:
            print "kml list is empty, good bye!"
            return 0       
        
        # make a copy of mac list
        macList = self.macList[:]
        # count number of mac found in kml
        n = 1        
        for kml in self.kmlList:            
            if "style" not in kml: # we don't care about style file
                kmlPath = '\\'.join([self.mainDir, kml])
                with open(kmlPath) as f:
                    doc = parser.parse(f)
                    doc = doc.getroot()                    
                    # matching mac from target list with kml list                    
                    for i in doc.Document.Placemark:
                        n = n + 1
                        if i.name in macList:
                            print "%s found in KML" % i.name
                            self.KmlPlacemarkColor(KML=i, color=self.kmlPlacemarkColor)
                            self.KmlPlacemarkScale(KML=i, scale=self.kmlPlacemarkScale)
                            self.KmlPlacemarkVisiblity(KML=i, visible=1)
                            # define kml label style properties:                          
                            newlabel = KML.LabelStyle(KML.color("ffffd500"), 
                                                      KML.scale(1.0))                            
                            self.KmlPlacemarkLabel(KML=i, label=newlabel, info=0)
                            # mac found, style been edited, remove it from list.
                            macList.remove(i.name)
                        else:                             
                            # set visibility of irrelevant placemark                            
                            self.KmlPlacemarkVisiblity(KML=i, visible=self.kmlOtherPlacemarkVisible, info=0)
                #save the file
                print "...saving file... %s" % kmlPath
                ofile = file(kmlPath, 'w')
                ofile.write(etree.tostring(etree.ElementTree(doc), pretty_print=True))
        self.KmlSummary(n, newMacList=macList)             
    
    def KmlPlacemarkColor(self, KML, color, info=1):
        if info==1: print "change color from %s to %s" % (KML.Style.IconStyle.color, color)
        KML.Style.IconStyle.color = color
    
    def KmlPlacemarkScale(self, KML, scale=1.0, info=1):
        if info==1: print "change icon scale from %s to %s" % (KML.Style.IconStyle.scale, scale)
        KML.Style.IconStyle.scale = scale
    
    def KmlPlacemarkVisiblity(self, KML, visible=1, info=1):
        if info==1: print "change visibility to %s" % (visible)
        KML.visibility = visible
    
    def KmlPlacemarkLabel(self, KML, label, info=1):
        KML.Style.append(label)        
    
    def KmlSummary(self, totalMacs, newMacList=[]):
        # number of macs that has went through the style change
        # len(newMacList) may not be zero if target mac are not found in kml file
        numMacs = len(set(self.macList) - set(newMacList))
        
        print "--------      Summary      --------"
        print "Total MACs found in database: %d" % totalMacs
        print "Updated style for %d macs" % numMacs
        if len(newMacList) > 0:
            print "%d macs from target list not found in database" % len(newMacList)            
            for i in newMacList:
                print i
        print "--------   End of Summary  --------"
    
    # remove files from HDD, i.e. kml files
    def FilesRemove(self, dirname, fileList = []):
        for i in fileList:
            print '...removing... %s from %s' % (i, dirname)
            os.remove(os.path.join(dirname, i))
    
    # test function
    def TestFunc(self):
        # unzip the KMZ file
        self.Unzip(self.kmzFile)
        print self.kmlList
        print self.macList
        
        # process the kml file
        self.KmlParser()
        
        # generating a new KMZ file name
        newKmzFileName = self.NameGen(self.macFile, self.kmzFile)
        
        # zip the KML files to this new KMZ file 
        self.NewZip(newKmzFileName, zipfiles = self.kmlList)
        
        #remove remaining kml files
        if self.removeKmls: 
            self.FilesRemove(dirname=self.mainDir, fileList=self.kmlList)
                        
    
    
        
            
        
        
        