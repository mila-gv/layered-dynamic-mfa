import numpy as np
from odym.modules.dynamic_stock_model import DynamicStockModel

class DMFAConfiguration:
    """ Holds all dmfa related data to configure a dmfa """
    
    def __init__(self, time_start: int, time_end: int, lifespan: int):
        self.time_start = time_start 
        self.time_end = time_end 
        self.lifespan = lifespan 
        self.time_list = np.arange(self.time_start, self.time_end + 1)
        self.Nt = len(self.time_list)
        self.Nc = self.Nt 
        self.lt = {
            'Type': 'LogNormal',
            'Mean': [self.lifespan],
            'StdDev': [self.lifespan]
        }
        
        # create survival function matrix
        self.sf = np.zeros((self.Nt, self.Nc))
        self.sf[:, :] = DynamicStockModel(t=np.arange(self.Nt), lt=self.lt).compute_sf().copy()        
        np.fill_diagonal(self.sf[:, :], 1)