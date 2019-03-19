import time
import numpy as np
import pickle as pkl
import sys
class Generator:
    """
    this is part of application level.
    don't have to worry about until we implement transport level.
    """
    def __init__(self):
        # Check if it's time to generate another iframe/pframe
        self.iFrameList = []
        self.pFrameList = []
        self.CONST_dtype = 'int64'
        self.CONST_pFrameSize = 153633
        self.CONST_iFrameSize = 9830433
        self.pFrameShape = (80, 80, 3)
        self.iFrameShape = (640, 640, 3)

    def get_iframe(self):
        res = np.random.randint(10,240, size=self.iFrameShape)
        self.iFrameList.append(res)
        byteRes = res.tobytes()
        return byteRes

    def get_pframe(self):
        res = np.random.randint(0,11, size=self.pFrameShape)
        self.pFrameList.append(res)
        byteRes = res.tobytes()
        return byteRes

    def byteToFrame(self,frameInput):
        if sys.getsizeof(frameInput) == self.CONST_pFrameSize:
            res = np.frombuffer(frameInput,dtype=self.CONST_dtype).reshape(self.pFrameShape)
        elif sys.getsizeof(frameInput) == self.CONST_iFrameSize:
            res = np.frombuffer(frameInput,dtype=self.CONST_dtype).reshape(self.iFrameShape)
        return res
    
    # # integer to byte
    # # https://www.devdungeon.com/content/working-binary-data-python#int-to-bytes
    # def conv2Bytes(self, frame):
    #     res = b''
    #     for i in frame:
    #         for j in i:
    #             for k in j:
    #                 res += k.to_bytes(1, byteorder='big', signed=False)
    #     return res

    def store(self):
        with open('iframePKL.pkl', 'wb') as f:
            pkl.dump(self.iFrameList, f)
        with open('pframePKL.pkl', 'wb') as f:
            pkl.dump(self.pFrameList, f)