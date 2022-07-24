import numpy as np
from dmfa.dmfa_configuration import DMFAConfiguration
from odym.modules.dynamic_stock_model import DynamicStockModel
from dataclasses import dataclass 


@dataclass
class UsePhase:
    stock_by_cohort: np.ndarray
    stock_change_by_cohort: np.ndarray
    outflow_by_cohort: np.ndarray
    
    inflow: np.ndarray
    stock: np.ndarray
    stock_change: np.ndarray
    outflow: np.ndarray 

def calculate_use_phase_stockdriven(stock: np.ndarray, dmfa_configuration: DMFAConfiguration) -> UsePhase:
    
    dsm = DynamicStockModel(
        t=np.arange(dmfa_configuration.Nt),
        lt=dmfa_configuration.lt,
        s=stock,
        sf=dmfa_configuration.sf
    )

    S_C, O_C, inflow = dsm.compute_stock_driven_model(NegativeInflowCorrect=True)
    DS_C = np.zeros(S_C.shape)
    DS_C[0, :] = S_C[0, :]
    DS_C[1::, :] = np.diff(S_C, axis=0)
    
    return UsePhase(
        stock_by_cohort=S_C,
        stock_change_by_cohort=DS_C,
        outflow_by_cohort=O_C,
        inflow=inflow,
        stock=np.einsum('tc->t', S_C),
        stock_change=np.einsum('tc->t', DS_C),
        outflow=np.einsum('tc->t', O_C),
    )


def calculate_use_phase_inflowdriven(inflow: np.ndarray, dmfa_configuration: DMFAConfiguration) -> UsePhase:

    dsm = DynamicStockModel(
        t=np.arange(dmfa_configuration.Nt),
        lt=dmfa_configuration.lt,
        i=inflow,
        sf=dmfa_configuration.sf,
    )
    
    S_C = dsm.compute_s_c_inflow_driven()
    O_C = dsm.compute_o_c_from_s_c()
    S = dsm.compute_stock_total()
    DS = dsm.compute_stock_change()
    DS_C = np.zeros(S_C.shape)
    DS_C[0, :] = S_C[0, :]
    DS_C[1::, :] = np.diff(S_C, axis=0)
    
    return UsePhase(
        stock_by_cohort=S_C,
        stock_change_by_cohort=DS_C,
        outflow_by_cohort=O_C,
        inflow=inflow,
        stock=np.einsum('tc->t', S_C),
        stock_change=np.einsum('tc->t', DS_C),
        outflow=np.einsum('tc->t', O_C),
    )