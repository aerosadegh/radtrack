import RadTrack.plot.RbPlotImageSequence as imageseq
import numpy as np

def main():
    mySequence = np.linspace(0, 10, 100)
    numImages  = 4
    numLines   = 7
    
    axes = imageseq.RbPlotImageSequence()
    for i, myAxis in zip(range(numLines), axes):
        myAxis.plot(mySequence, np.sin(i*mySequence))
        myAxis.set_title('Line {} '.format(i+1) + 'of {}'.format(numLines))
    for i, myAxis in zip(range(numImages), axes):
        myAxis.imshow(np.random.random((40,40)))
        myAxis.set_title('Image {} '.format(i+1) + 'of {}'.format(numImages))
    axes.show()

if __name__ == '__main__':
    main()
