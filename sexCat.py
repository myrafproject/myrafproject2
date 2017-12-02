#!/usr/bin/env python
import alipy
import os, ntpath

class runSex:
    
    def __init__(self, filepath):
        
        self.filepath = filepath

    def run(self, fRadius, fwhm_min, fwhm_max, getHead):
        
        alipy.pysex.run(image=self.filepath, imageref='', params=['X_IMAGE', 'Y_IMAGE', 'MAG_APER', 'MAG_AUTO', 'MU_MAX', 'FLUX_RADIUS', 'FWHM_IMAGE', 'ELLIPTICITY'], conf_file=None, conf_args={}, keepcat=True, rerun=True, catdir="/tmp/")
        fileName = ntpath.splitext(self.filepath)
        filepath = ntpath.basename(fileName[0])
        os.popen("cat /tmp/%s.pysexcat| grep -v '#'| awk '{if ($3 != '99.0000' && $4 != '99.0000' && $6 > %s && $7 > %s && $7 <%s) print $1, $2, $3, $4, $5, $6, $7, $8}'| sort -nk5| head -%s > /tmp/sexCoor" %(filepath, fRadius, fwhm_min, fwhm_max, getHead))
        
        ins = open("/tmp/sexCoor", "rb")
        array = []
        
        for line in ins:
            array.append(line.replace("\n","").split(" "))
        ins.close()
        
        os.remove("/tmp/%s.pysexcat" %(filepath))
        
        return array
  
