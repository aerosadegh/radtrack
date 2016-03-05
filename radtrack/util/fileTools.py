from PyQt4.QtGui import QFileDialog
import os

# Generic Exception class for file read errors
class FileParseException(Exception):
    def __init__(self, message):
        super(FileParseException, self).__init__()
        self.message = message

__fileTypeDescription = dict()
__fileTypeDescription['*'] = 'All files'
__fileTypeDescription['lte'] = 'Elegant lattice file'
__fileTypeDescription['sdds'] = 'Self-Describing Data Set'
__fileTypeDescription['save'] = None
__fileTypeDescription['start'] = None
__fileTypeDescription['csv'] = 'Comma-separated value file'
__fileTypeDescription['rad'] = 'Laser beam line file'
__fileTypeDescription['out'] = 'Output file'
__fileTypeDescription['bun'] = 'Beam bunch file'
__fileTypeDescription['twi'] = 'Twiss parameter file'
__fileTypeDescription['sig'] = 'Sigma matrix file'
__fileTypeDescription['cen'] = 'Centroid output file'
__fileTypeDescription['dat'] = 'Data file'
__fileTypeDescription['txt'] = 'Text file'
__fileTypeDescription['fin'] = 'Elegant final properties file'
__fileTypeDescription['fel'] = 'FEL Calculator file'
__fileTypeDescription['lat'] = 'Genesis lattice file'
__fileTypeDescription['png'] = 'PNG Image'
__fileTypeDescription['jpg'] = 'JPG Image'
__fileTypeDescription['bmp'] = 'BMP Image'
__fileTypeDescription['ppm'] = 'PPM Image'
__fileTypeDescription['tiff'] = 'TIFF Image'
__fileTypeDescription['xbm'] = 'XBM Image'
__fileTypeDescription['xpm'] = 'XPM Image'
__fileTypeDescription['h5'] = 'Hierarchial Data Format'
__fileTypeDescription['in'] = 'Genesis Input File'

def fileTypeDescription(ext):
    try:
        return __fileTypeDescription[ext] + ' (*.' + ext + ')'
    except TypeError:
        return None


def fileTypeList(exts):
    return ';;'.join([fileTypeDescription(ext.strip('.')) for ext in ['*'] + exts if fileTypeDescription(ext)])


def getSaveFileName(widget, exts = None):
    if exts:
        if isinstance(exts, (str, unicode)):
            exts = [exts]
    else:
        exts = widget.acceptsFileTypes

    dialog = QFileDialog(widget, 'Save File', widget.parent.lastUsedDirectory, fileTypeList(exts))
    dialog.setDefaultSuffix(exts[0])
    dialog.filterSelected.connect(lambda filter : dialog.setDefaultSuffix(filter.split('*')[1].strip(')').strip('.')))
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    if dialog.exec_():
        fileName = dialog.selectedFiles()[0]
        if os.path.isdir(fileName):
            return None
        else:
            widget.parent.lastUsedDirectory = os.path.dirname(fileName)
            return fileName


def isSDDS(fileName):
    with open(fileName) as f:
        return f.readline().startswith('SDDS')
