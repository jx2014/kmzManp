import re
import os
import zipfile


class KMZ():
    def __init__(self, target, kmzfile):
        #self.kmzDir = os.path.dirname(kmzfile)
        #self.kmzFileNameOnly = os.path.basename(kmzfile) #get file name of the kmz file
        self.kmzFile = kmzfile # this is the kmz file with its full path
        self.macFile = target # target is the mac address data file, full path included, which should be the same as kmz file
        self.kmlList = []
        
        #load target mac ID to a list
        self.macList = []
        with open(self.macFile) as fn:
            for mac in fn.readlines():
                self.macList.append(mac)
    
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
        
        print 'creating ZIP file %s in %s' % (fileNameOnly, dirname)
        
        zipFile = zipfile.ZipFile(newKmzFileName, mode='w')
        try:
            for i, n in enumerate(fileList):
                print 'adding %s' % n
                zipFile.write(n, arcname=os.path.basename(n), compress_type=zipfile.ZIP_DEFLATED)
        finally:
            print 'Zip finished...'
            zipFile.close        
    
    # test function
    def TestFunc(self):
        # unzip the KMZ file
        self.Unzip(self.kmzFile)
        print self.kmlList
        print self.macList
        
        # generating a new KMZ file name
        #newKmzFileName = self.NameGen(self.macFile, self.kmzFile)
        
        # zip the KML files to this new KMZ file 
        #self.NewZip(newKmzFileName, zipfiles = self.kmlList)
                        
    
    
        
            
        
        
        