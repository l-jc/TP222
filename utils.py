import time
import numpy as np
import pickle
class Generator:
    """
    this is part of application level.
    don't have to worry about until we implement transport level.
    """
    def __init__(self):
        # Check if it's time to generate another iframe/pframe
        self.startTime = time.time()
        self.iFrameList = []
        self.pFrameList = []
        

    def get_iframe(self):
        res = np.random.randint(10,240, size=(640, 640,3))
        iFrameList.append(res)
        return res

    def get_pframe(self):
        res = np.random.randint(0,11, size=(80, 80,3))
        pFrameList.append(res)
        return res

    def store(self):
        with open('iframePKL.pkl', 'wb') as f:
            pkl.dump(iFrameList, f)
        with open('pframePKL.pkl', 'wb') as f:
            pkl.dump(pFrameList, f)

