"""

EWH - used to start a thread for a specific valuelogger. 

"""

from datetime import datetime
import os
import time
from PyQt5 import QtCore
import numpy as np
from PyQt5.QtCore import pyqtSlot
        
def isnan(num):
    return num != num

class valuelogger(QtCore.QThread):
    timelog=None
    valuelog=None
    historylength=None
    logfile=None
    filebasepath=None
    filebasename=None
    fid=None
    parent=None

    def __init__(self, *args, **kwargs) :
        #super().__init__(self, *args, **kwargs)
        super().__init__(*args, **kwargs)
        
        # ========================================
        # 09-10-2024 YC: we no longer setup any threading inside the class now
        #self.Timer = QtCore.QTimer()
        #self.Timer.moveToThread(self)
        #self.Timer.timeout.connect(self.datacollector)
        #self.is_running = False

    def initiateTimer(self,timeout,filebasepath,filebasename,parent=None):
        self.timeout=timeout
        self.filebasepath=filebasepath
        self.filebasename=filebasename
        self.timelog=[]
        self.valuelog=[]
        #self.timelog=[np.nan] * self.historylength 
        #self.valuelog=[np.nan] * self.historylength     
        #self.currentPointer = 0
        self.parent=parent
    
    # 09-10-2024 YC: deprecated    
    def run(self):        
        self.Timer.start(self.timeout)
        self.Timer.timeout.connect(self.datacollector)
        self.is_running = True
        while self.is_running:
            self.msleep(100)
        self.Timer.stop()
                
    def updateLog(self,value,valtime=None):
        if valtime==None:
            valtime=time.time()
        self.timelog.append(valtime)
        self.valuelog.append(value)
        #self.timelog[self.currentPointer] = valtime
        #self.valuelog[self.currentPointer] = value
        #self.currentPointer += 1        
        if self.parent.unit_test == True:
            self.historylength = 30
        
# =============================================================================
#         if not self.fid is None:
#              if not isnan(self.valuelog[-1]):
#                  if self.fid.closed:
#                      datestr=datetime.today().strftime('%Y%m%d%H%M%S')
#                      if not (self.filebasename is None or self.filebasepath is None):
#                          self.logfile=os.path.join(self.filebasepath,self.filebasename + '_' + datestr + '.csv')
#                          self.fid=open(self.logfile,'w')
#                  self.fid.write("{0},{1}\n".format(self.timelog[-1],self.valuelog[-1]))
# =============================================================================
        if len(self.timelog)>self.historylength:
        #if self.currentPointer >= self.historylength:
# =============================================================================
#               if not self.fid is None:
#                    self.fid.close()
#                    if not (self.filebasename is None or self.filebasepath is None):
#                        datestr=datetime.today().strftime('%Y%m%d%H%M%S')
#                        self.logfile=os.path.join(self.filebasepath,self.filebasename + '_' + datestr + '.csv')
#                        self.fid=open(self.logfile,'w')
# =============================================================================
              
               # whenever it reaches historylength, save .csv, keep last 5, continue to log
              #self.timelog.clear()
              #self.valuelog.clear()
              self.timelog.pop(0)
              self.valuelog.pop(0)
#              del self.timelog[:-10]
#              del self.valuelog[:-10]

        self.updateVis()

    # 09-10-2024 YC: deprecated       
    @pyqtSlot()
    def stopLog(self):
        print(self.thread(), self.Timer.thread())
        #self.Timer.stop()   # how to stop the Timer???????????????????????
        #self.Timer.deleteLater()
        self.is_running = False
        #print(self.Timer.isActive())
        for istep in range(10):

            if not self.Timer.isActive():
    
                break;
            else:
                print("Timer Stop:", istep)
                self.Timer.stop()
           

        self.terminate()

        if not self.fid is None:
            self.fid.close()
        self.timelog=[]
        self.valuelog=[]    
        
        
    def updateVis(self):
        1;
        
    def datacollector(self):
        print("collecting data")
        1
        