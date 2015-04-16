import sys, os, subprocess
import sip
sip.setapi('QString', 2)
from PyQt4 import QtGui, QtCore
from radtrack.interactions.simulationpanel import Ui_Form
from radtrack.srw.RbSrwUndulator import *
from radtrack.srw.srwlib import *
from radtrack.srw.dataclass import *
from radtrack.srw.BPsdds2srw import *
from  radtrack.RbEle import RbEle
import numpy as np
from radtrack.srw.uti_plot import *

class RbSimulations(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.programs.setDragEnabled(True)
        self.ui.graphicsView.setAcceptDrops(True)

        rect = QtCore.QRectF(0,0,2000,1100)

        background = QtGui.QGraphicsRectItem(rect)
        whitebrush = QtGui.QBrush(QtCore.Qt.white)
        background.setBrush(whitebrush)
        background.setAcceptDrops(True)
        self.scene = customscene(self)
        self.scene.addItem(background)
        
        self.ui.graphicsView.setScene(self.scene)

        self.blocks = dict()
        self.simtrains = []
        self.lines = dict()
        #self.simtrain = []

        self.scene.signal.connect(self.drawblocks)
        self.scene.moving.connect(self.updatelines)
        self.ui.pushButton.clicked.connect(self.runeverything)
        self.count = 0

        self.container = QtGui.QScrollArea(parent)
        self.container.setWidget(self)
        self.defaultTitle = parent.tr('Interactions')

    def runeverything(self):
        if self.blocks['seed'].type == 'Elegant':
            subprocess.call([self.blocks['seed'].type, self.blocks['seed'].elefile])
        elif self.blocks['seed'].type == 'SRW':
            Up = self.blocks['seed'].un
            und = SRWLMagFldU([SRWLMagFldH(1, 'v', Up.By, Up.phBy, Up.sBy, 1), SRWLMagFldH(1, 'h', Up.Bx, Up.phBx, Up.sBx, 1)], Up.undPer, Up.numPer)
            magFldCnt = SRWLMagFldC([und], array('d', [Up.xcID]), array('d', [Up.ycID]), array('d', [Up.zcID]))
            precis = self.blocks['seed'].pr
            arPrecPar = [precis.meth, precis.relPrec, precis.zStartInteg, precis.zEndInteg, precis.npTraj, precis.useTermin, precis.sampFactNxNyForProp]
            self.blocks['seed'].wfr.partBeam = self.blocks['seed'].bm
            wfrXY = self.blocks['seed'].wfr
            wfrE = self.blocks['seed'].wfr

            mesh = deepcopy(self.blocks['seed'].wfr.mesh)
            wfrIn = deepcopy(self.blocks['seed'].wfr)

            Polar = self.blocks['seed'].polar
            Intens = self.blocks['seed'].intens
            DependArg = self.blocks['seed'].dependarg
                
            if DependArg == 0:
                #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
                str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
                #self.ui.status.setText(str1)
                #self.ui.status.repaint()
                srwl.CalcElecFieldSR(wfrE, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n'
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f',[0]*wfrE.mesh.ne)
                srwl.CalcIntFromElecField(arI1, wfrE, Polar, Intens, DependArg, wfrE.mesh.eStart, 0, 0)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #time.sleep(1)
                #self.ui.status.repaint()
                uti_plot1d(arI1, [wfrE.mesh.eStart, wfrE.mesh.eFin, wfrE.mesh.ne],['label','label','label'])
            elif DependArg == 1:
                str1='* Performing Electric Field (intensity vs x-coordinate) calculation ... \n \n'
                #self.ui.status.setText(str1)
                srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f',[0]*wfrXY.mesh.nx)
                srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.xStart, 0)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #self.ui.status.repaint()
                uti_plot1d(arI1, [wfrXY.mesh.xStart, wfrXY.mesh.xFin, wfrXY.mesh.nx],['label','label','label'])
            elif DependArg == 2:
                str1='* Performing Electric Field (intensity vs y-coordinate) calculation ... \n \n'
                #self.ui.status.setText(str1)
                #self.ui.status.repaint()
                srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f',[0]*wfrXY.mesh.ny)
                srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.yStart, 0)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #self.ui.status.repaint()
                uti_plot1d(arI1, [wfrXY.mesh.yStart, wfrXY.mesh.yFin, wfrXY.mesh.ny],['label','label','label'])
            elif DependArg == 3:
                str1='* Performing Electric Field (intensity vs x- and y-coordinate) calculation ... \n \n'
                #self.ui.status.setText(str1)
                #self.ui.status.repaint()
                srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f', [0]*wfrXY.mesh.nx*wfrXY.mesh.ny)
                srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #self.ui.status.repaint()
                uti_plot2d(arI1, [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
                [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
                ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
            elif DependArg == 4:
                str1='* Performing Electric Field (intensity vs energy- and x-coordinate) calculation ... \n \n '
                #self.ui.status.setText(str1)
                #self.ui.status.repaint()
                srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.nx)
                srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #self.ui.status.repaint()
                uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
                [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
                ['Energy [eV]', 'Horizontal Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
            elif DependArg == 5:
                str1='* Performing Electric Field (intensity vs energy- and y-coordinate) calculation ... \n \n'
                #self.ui.status.setText(str1)
                #self.ui.status.repaint()
                srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                #self.ui.status.setText(str1+str2)
                #self.ui.status.repaint()
                arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.ny)
                srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                str3='* Plotting the results ...\n'
                #self.ui.status.setText(str1+str2+str3)
                #self.ui.status.repaint()
                uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
                [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
                ['Energy [eV]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
            else:
                print 'Error'
    
            uti_plot_show()

        l = self.blocks['seed'].after

        while True:
            if len(l) == 0:
                break

            #just choose to simulate the 'first connected' simulation
            if self.blocks[l[0]].type == 'Elegant':
                subprocess.call([self.blocks[l[0]].type, self.blocks[l[0]].elefile])
            elif self.blocks[l[0]].type == 'SRW':
                Up = self.blocks[l[0]].un
                und = SRWLMagFldU([SRWLMagFldH(1, 'v', Up.By, Up.phBy, Up.sBy, 1), SRWLMagFldH(1, 'h', Up.Bx, Up.phBx, Up.sBx, 1)], Up.undPer, Up.numPer)
                magFldCnt = SRWLMagFldC([und], array('d', [Up.xcID]), array('d', [Up.ycID]), array('d', [Up.zcID]))
                precis = self.bloacks[l[0]].pr
                arPrecPar = [precis.meth, precis.relPrec, precis.zStartInteg, precis.zEndInteg, precis.npTraj, precis.useTermin, precis.sampFactNxNyForProp]
                self.blocks[l[0]].wfr.partBeam = self.blocks[l[0]].bm
                wfrXY = self.blocks[l[0]].wfr
                wfrE = self.blocks[l[0]].wfr

                mesh = deepcopy(self.blocks[l[0]].wfr.mesh)
                wfrIn = deepcopy(self.blocks[l[0]].wfr)

                Polar = self.blocks[l[0]].polar
                Intens = self.blocks[l[0]].intens
                DependArg = self.blocks[l[0]].dependarg
                
                if DependArg == 0:
                    #after setting the text call self.ui.status.repaint() to have it immediately show otherwise it will wait till it exits the block to draw
                    str1='* Performing Electric Field (spectrum vs photon energy) calculation ... \n \n'
                    #self.ui.status.setText(str1)
                    #self.ui.status.repaint()
                    srwl.CalcElecFieldSR(wfrE, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n'
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f',[0]*wfrE.mesh.ne)
                    srwl.CalcIntFromElecField(arI1, wfrE, Polar, Intens, DependArg, wfrE.mesh.eStart, 0, 0)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #time.sleep(1)
                    #self.ui.status.repaint()
                    uti_plot1d(arI1, [wfrE.mesh.eStart, wfrE.mesh.eFin, wfrE.mesh.ne],['label','label','label'])
                elif DependArg == 1:
                    str1='* Performing Electric Field (intensity vs x-coordinate) calculation ... \n \n'
                    #self.ui.status.setText(str1)
                    srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f',[0]*wfrXY.mesh.nx)
                    srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.xStart, 0)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #self.ui.status.repaint()
                    uti_plot1d(arI1, [wfrXY.mesh.xStart, wfrXY.mesh.xFin, wfrXY.mesh.nx],['label','label','label'])
                elif DependArg == 2:
                    str1='* Performing Electric Field (intensity vs y-coordinate) calculation ... \n \n'
                    #self.ui.status.setText(str1)
                    #self.ui.status.repaint()
                    srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f',[0]*wfrXY.mesh.ny)
                    srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, 0, wfrXY.mesh.yStart, 0)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #self.ui.status.repaint()
                    uti_plot1d(arI1, [wfrXY.mesh.yStart, wfrXY.mesh.yFin, wfrXY.mesh.ny],['label','label','label'])
                elif DependArg == 3:
                    str1='* Performing Electric Field (intensity vs x- and y-coordinate) calculation ... \n \n'
                    #self.ui.status.setText(str1)
                    #self.ui.status.repaint()
                    srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f', [0]*wfrXY.mesh.nx*wfrXY.mesh.ny)
                    srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #self.ui.status.repaint()
                    uti_plot2d(arI1, [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
                    [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
                    ['Horizontal Position [mm]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
                elif DependArg == 4:
                    str1='* Performing Electric Field (intensity vs energy- and x-coordinate) calculation ... \n \n '
                    #self.ui.status.setText(str1)
                    #self.ui.status.repaint()
                    srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.nx)
                    srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #self.ui.status.repaint()
                    uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
                    [1000*wfrXY.mesh.xStart, 1000*wfrXY.mesh.xFin, wfrXY.mesh.nx], 
                    ['Energy [eV]', 'Horizontal Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
                elif DependArg == 5:
                    str1='* Performing Electric Field (intensity vs energy- and y-coordinate) calculation ... \n \n'
                    #self.ui.status.setText(str1)
                    #self.ui.status.repaint()
                    srwl.CalcElecFieldSR(wfrXY, 0, magFldCnt, arPrecPar)
                    str2='* Extracting Intensity from calculated Electric Field ... \n \n '
                    #self.ui.status.setText(str1+str2)
                    #self.ui.status.repaint()
                    arI1 = array('f', [0]*wfrXY.mesh.ne*wfrXY.mesh.ny)
                    srwl.CalcIntFromElecField(arI1, wfrXY, Polar, Intens, DependArg, wfrXY.mesh.eStart, wfrXY.mesh.xStart, wfrXY.mesh.yStart)
                    str3='* Plotting the results ...\n'
                    #self.ui.status.setText(str1+str2+str3)
                    #self.ui.status.repaint()
                    uti_plot2d(arI1, [1000*wfrXY.mesh.eStart, 1000*wfrXY.mesh.eFin, wfrXY.mesh.ne], 
                    [1000*wfrXY.mesh.yStart, 1000*wfrXY.mesh.yFin, wfrXY.mesh.ny], 
                    ['Energy [eV]', 'Vertical Position [mm]', 'Intensity at ' + str(wfrXY.mesh.eStart) + ' eV'])
                else:
                    print 'Error'
    
                uti_plot_show()

            l = self.blocks[l[0].after]
            
                
            
        

    def updatelines(self, pos):
        a = self.scene.itemAt(pos)
        if a.after!=0:
            for i in a.after:      
                pt2 = self.blocks[i].getinpt()
                pt1 = a.getoutpt()
                linef = QtCore.QLineF()
                linef.setPoints(pt1,pt2)
                self.lines[a.name+i].setLine(linef)
                self.scene.update()

        if a.before!=0:
            for i in a.before:
                pt2 = self.blocks[i].getoutpt()
                pt1 = a.getinpt()
                linef = QtCore.QLineF()
                linef.setPoints(pt1,pt2)
                self.lines[a.name+i].setLine(linef)
                self.scene.update()
        

    def drawblocks(self, pos):
        a = self.scene.itemAt(pos)
        if self.ui.programs.currentItem().text()=='SRW':
            dialog = srwDialog()
            if dialog.exec_():
                if int(a.pos().x()) == 0 and int(a.pos().y()) == 0:
                    seed = block(self.ui.programs.currentItem().text())
                    seed.name = 'seed'
                    seed.setZValue(10)
                    seed.setPos(pos)
                    dialog.srw.UndParams(seed.un)
                    dialog.srw.BeamParams(seed.bm)
                    dialog.srw.WfrSetUpE(seed.wfr)
                    dialog.srw.Precision(seed.pr)
                    seed.polar = dialog.srw.ui.polar.currentIndex()
                    seed.intens = dialog.srw.ui.intensity.currentIndex()
                    seed.dependarg = dialog.srw.ui.deparg.currentIndex()

                    self.scene.addItem(seed)
                    self.blocks['seed'] = seed

                else:
                    a = self.scene.itemAt(pos)
                    x = a.x()+200
                    newblock = block(self.ui.programs.currentItem().text())
                    newblock.hasinput = True
                    newblock.before.append(a.name)
                    newblock.name = newblock.type+str(self.count)
                    newblock.setZValue(10)
                    
                    a.after.append(newblock.name)
                    y = a.y()+100*(len(a.after)-1)
                    newblock.setPos(x,y)

                    b=BP()
                    eleinput = os.path.splitext(a.elefile)[0]+'.out'               
                    words = BPsdds2srw(eleinput,'BP.txt',b)
      
                    dialog.srw.ui.iavg.setText('5')
                    dialog.srw.ui.iavg.repaint()
                    #dialog.srw.ui.iavg.update()
                    dialog.srw.ui.partstatmom1x.setText(str(b.Cx))
                    dialog.srw.ui.partstatmom1y.setText(str(b.Cy))
                    dialog.srw.ui.partstatmom1z.setText(str(b.Ct))
                    dialog.srw.ui.partstatmom1xp.setText(str(b.Cxp))
                    dialog.srw.ui.partstatmom1yp.setText(str(b.Cyp))
                    #self.ui.partstatmom1gamma.setText('5870.925')

                    dialog.srw.UndParams(newblock.un)
                    dialog.srw.BeamParams(newblock.bm)
                    dialog.srw.WfrSetUpE(newblock.wfr)
                    dialog.srw.Precision(newblock.pr)

                    newblock.polar = dialog.srw.ui.polar.currentIndex()
                    newblock.intens = dialog.srw.ui.intensity.currentIndex()
                    newblock.dependarg = dialog.srw.ui.deparg.currentIndex()
                    
                    self.count+=1
            
                    self.blocks[newblock.name] = newblock

                    self.scene.addItem(newblock)

                    simtrain = []

                    line = QtGui.QGraphicsLineItem(a.x()+100,a.y()+25,newblock.x(),newblock.y()+25)
                    line.setZValue(1)
                    self.lines[a.name+newblock.name] = line
                    self.lines[newblock.name+a.name] = line

                    self.scene.addItem(line)
                    
        elif self.ui.programs.currentItem().text() == 'Elegant':
            dialog = eleDialog()
            if dialog.exec_():
                runele = dialog.ele.simulate()
                if int(a.pos().x()) == 0 and int(a.pos().y()) == 0:
                    seed = block(self.ui.programs.currentItem().text())
                    #seed.type = self.ui.programs.currentItem().text()
                    seed.name = 'seed'
                    seed.setZValue(10)
                    seed.setPos(pos)
                    seed.elefile = runele
                    self.scene.addItem(seed)
                    #seed.seedpos = pos
                    self.blocks['seed'] = seed

                else:
                    a = self.scene.itemAt(pos)
                    x = a.x()+200
                    newblock = block(self.ui.programs.currentItem().text())
                    newblock.hasinput = True
                    newblock.before.append(a.name)
                    #newblock.type = self.ui.programs.currentItem().text()
                    newblock.name = newblock.type+str(self.count)
                    newblock.setZValue(10)

                    a.after.append(newblock.name)
                    y = a.y()+100*(len(a.after)-1)
                    newblock.setPos(x,y)
                    newblock.elefile = runele
            
                    self.count+=1
            
                    self.blocks[newblock.name] = newblock

                    self.scene.addItem(newblock)

                    simtrain = []

                    #dictionary of lines
                    line = QtGui.QGraphicsLineItem(a.x()+100,a.y()+25,newblock.x(),newblock.y()+25)
                    line.setZValue(1)
                    self.lines[a.name+newblock.name] = line
                    self.lines[newblock.name+a.name] = line

                    self.scene.addItem(line)    
                    
           
        
        
class block(QtGui.QGraphicsItem):

    def __init__(self, simtype):
        QtGui.QGraphicsItem.__init__(self)#parent = None?
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.limit = QtCore.QRectF(0,0,100,50)
        self.setAcceptDrops(True)

        self.before = []
        self.after = []
        #self.seedpos = None
        self.order = 0
        self.type = simtype
        self.name = ''
        self.hasinput = False
        self.ran = False
        if self.type =='Elegant':
            self.elefile = None
        if self.type =='SRW':
            self.bm = SRWLPartBeam()
            self.un = UP()
            self.pr = Precis()
            self.wfr = SRWLWfr()
            self.polar = 0
            self.intens = 0
            self.dependarg = 0
        

    def getinpt(self):
        pt = QtCore.QPointF()
        pt.setX(self.x())
        pt.setY(self.y()+25)
        return pt

    def getoutpt(self):
        pt = QtCore.QPointF()
        pt.setX(self.x()+100)
        pt.setY(self.y()+25)
        return pt
        
    def boundingRect(self):
        return self.limit

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.green)
        
        painter.drawRect(self.limit)
        painter.drawText(self.limit, QtCore.Qt.AlignCenter, self.type)
        
        if self.hasinput == False:
            painter.drawText(2,10,'input')
        else:
            painter.setPen(QtCore.Qt.darkGreen)
            painter.drawText(2,10,'input')
            painter.setBrush(QtCore.Qt.darkGreen)
            painter.drawEllipse(27,2,7,7)

        painter.setPen(QtCore.Qt.black)
        painter.drawText(67,10,'output')    
            

    def dropEvent(self, event):
        super(block, self).dropEvent(event)

    def dragEnterEvent(self, event):
        super(block, self).dragEnterEvent(event)
        
    def dragMoveEvent(self, event):
        super(block, self).dragMoveEvent(event)        

        
class customscene(QtGui.QGraphicsScene):
    signal = QtCore.Signal(QtCore.QPointF)
    moving = QtCore.Signal(QtCore.QPointF)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self)

    def dragEnterEvent(self, event):
        super(customscene, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(customscene, self).dragMoveEvent(event)

    def dropEvent(self, event):
        super(customscene, self).dropEvent(event)
        self.signal.emit(event.scenePos())

    def mouseMoveEvent(self, event):
        super(customscene, self).mouseMoveEvent(event)
        self.moving.emit(event.scenePos())

class srwDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.srw = srwund()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.srw)
        layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        self.resize(1000,720)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

class eleDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ele = RbEle()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ele)
        layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        self.resize(700,500)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        

def main():

    app = QtGui.QApplication(sys.argv)
    myapp = RbSimulations()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
