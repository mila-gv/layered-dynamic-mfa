import numpy as np
from dmfa.usephase import UsePhase
from dmfa.dmfa_configuration import DMFAConfiguration
import pandas as pd

class Stock:
    def __init__(self, name: str, Nt: int, explanation: str = '') -> None:
        self.name = name 
        self.values = np.zeros(Nt)  # initialize to zeros
        self.explanation = explanation

class Flow: 
    def __init__(self, name: str, Nt: int, explanation: str = '') -> None:
        self.name = name 
        self.values = np.zeros(Nt)  # initialize to zeros
        self.transfer_coefficient = np.zeros(Nt)  # initialize to zeros
        self.explanation = explanation
    
    def set_transfer_coefficient(self, transfer_coefficient: np.ndarray):
        if transfer_coefficient.shape != self.values.shape:
            raise AssertionError(f"""Transfer coefficient does not have same shape as 
                                 values {transfer_coefficient.shape}, {self.values.shape}
                                 """)
        self.transfer_coefficient = transfer_coefficient


class DMFA:

    def __init__(self, dmfa_configruation: DMFAConfiguration):

        self.usephase: UsePhase = None
        self.dmfa_configruation = dmfa_configruation
        Nt = dmfa_configruation.Nt
        
        self.dS_0 = Stock('dS_0', Nt)
        self.dS_8 = Stock('dS_8', Nt)
        self.dS_9 = Stock('dS_9', Nt)
        self.dS_10 = Stock('dS_10', Nt)

        self.F_1_0 =  Flow('F_1_0', Nt, explanation='Flow from Use Phase to Air')
        self.F_1_2 =  Flow('F_1_2', Nt, explanation='Flow from Use Phase to Dismantling')
        self.F_1_9 =  Flow('F_1_9', Nt, explanation='Flow From Use Phase to Exports')
        self.F_1_10 = Flow('F_1_9', Nt, explanation='Flow from Use Phase to Water')
        self.F_2_0 =  Flow('F_2_0', Nt, explanation='Flow from Dismantling to Air')
        self.F_2_1 =  Flow('F_2_1', Nt, explanation='Flow from Dismantling to Use Phase')
        self.F_2_3 =  Flow('F_2_3', Nt, explanation='Flow from Dismantling to Incineration')
        self.F_2_4 =  Flow('F_2_4', Nt, explanation='Flow from Dismantling to Mechanical Recycling')
        self.F_3_0 =  Flow('F_3_0', Nt, explanation='Flow from Incineration to Air')
        self.F_3_8 =  Flow('F_3_8', Nt, explanation='Flow from Incineration to Losses')
        self.F_3_10 = Flow('F_3_10', Nt, explanation='Flow from Incineration to Water')
        self.F_4_0 =  Flow('F_4_0', Nt, explanation='Flow from Mechanical Recycling to Air')
        self.F_4_1 =  Flow('F_4_1', Nt, explanation='Flow from Mechanical Recycling to Use Phase')
        self.F_4_3 =  Flow('F_4_3', Nt, explanation='Flow from Mechanical Recycling to Incineration')
        self.F_4_10 = Flow('F_4_10', Nt, explanation='Flow from Mechanical Recycling to Water')

    def set_transfer_coefficients(self, df: pd.DataFrame):
        self.F_1_0.set_transfer_coefficient(df['F_1_0'].values)
        self.F_1_2.set_transfer_coefficient(df['F_1_2'].values)
        self.F_1_9.set_transfer_coefficient(df['F_1_9'].values)
        self.F_1_10.set_transfer_coefficient(df['F_1_10'].values)
        self.F_2_0.set_transfer_coefficient(df['F_2_0'].values)
        self.F_2_1.set_transfer_coefficient(df['F_2_1'].values)
        self.F_2_3.set_transfer_coefficient(df['F_2_3'].values)
        self.F_2_4.set_transfer_coefficient(df['F_2_4'].values)
        self.F_3_0.set_transfer_coefficient(df['F_3_0'].values)
        self.F_3_8.set_transfer_coefficient(df['F_3_8'].values)
        self.F_3_10.set_transfer_coefficient(df['F_3_10'].values)
        self.F_4_0.set_transfer_coefficient(df['F_4_0'].values)
        self.F_4_1.set_transfer_coefficient(df['F_4_1'].values)
        self.F_4_3.set_transfer_coefficient(df['F_4_3'].values)
        self.F_4_10.set_transfer_coefficient(df['F_4_10'].values)

    def get_flows_and_stocks(self) -> list[Flow]:
        attributes = self.__dict__
        flow_attributes = [
            value for key, value in attributes.items() 
            if isinstance(value, Flow) or isinstance(value, Stock)]
        return flow_attributes
    
    def solve_flows_and_stocks(self, usephase: UsePhase, t: int):
        
        outflow = usephase.outflow
        stock = usephase.stock 
        # P1 outflows
        self.F_1_0.values[t] = stock[t] * self.F_1_0.transfer_coefficient[t]  
        
        # something with stock
        self.F_1_2.values[t] = self.F_1_2.transfer_coefficient[t] * outflow[t]
        self.F_1_9.values[t] = self.F_1_9.transfer_coefficient[t] * outflow[t]
        self.F_1_10.values[t] = self.F_1_10.transfer_coefficient[t] * outflow[t]
                                         
        # P2 outflows
        self.F_2_0.values[t] = self.F_2_0.transfer_coefficient[t] * self.F_1_2.values[t]
        self.F_2_1.values[t] = self.F_2_1.transfer_coefficient[t] * self.F_1_2.values[t]
        self.F_2_3.values[t] = self.F_2_3.transfer_coefficient[t] * self.F_1_2.values[t]
        self.F_2_4.values[t] = self.F_2_4.transfer_coefficient[t] * self.F_1_2.values[t]
        
        # P3 outflows
        self.F_3_0.values[t] = self.F_3_0.transfer_coefficient[t] * self.F_2_3.values[t]
        self.F_3_8.values[t] = self.F_3_8.transfer_coefficient[t] * self.F_2_3.values[t]
        self.F_3_10.values[t] = self.F_3_10.transfer_coefficient[t] * self.F_2_3.values[t]
        
        # P4 outflows
        self.F_4_0.values[t] = self.F_4_0.transfer_coefficient[t] * self.F_2_4.values[t]
        self.F_4_1.values[t] = self.F_4_1.transfer_coefficient[t] * self.F_2_4.values[t]
        self.F_4_3.values[t] = self.F_4_3.transfer_coefficient[t] * self.F_2_4.values[t]
        self.F_4_10.values[t] = self.F_4_10.transfer_coefficient[t] * self.F_2_4.values[t]

        # dS0
        self.dS_0.values[t] = (
            + self.F_1_0.values[t] + self.F_2_0.values[t] 
            + self.F_3_0.values[t] + self.F_4_0.values[t]
        )
        # dS8
        self.dS_8.values[t] = self.F_3_8.values[t] 
        # dS9
        self.dS_9.values[t] = self.F_1_9.values[t] 
        # dS10
        self.dS_10.values[t] = self.F_1_10.values[t] + self.F_3_10.values[t] + self.F_4_10.values[t]  
        
    def shift_export_flow_and_stock(self, num_years: int):
        self.F_1_9.values = np.roll(self.F_1_9.values, -num_years, axis=0)
        self.F_1_9.values[-num_years:] = self.F_1_9.values[-num_years-1]
        self.dS_9.values = np.roll(self.dS_9.values, -num_years, axis=0)
        self.dS_9.values[-num_years:] = self.dS_9.values[-num_years-1]
