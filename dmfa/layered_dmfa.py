
from dataclasses import dataclass
from dmfa.dmfa import DMFA, DMFAConfiguration
from dmfa.scenario_input import ScenarioInput
from dmfa.usephase import calculate_use_phase_inflowdriven, calculate_use_phase_stockdriven

@dataclass 
class LayeredDMFA:
    """ Holds all relevent objects (classes) for the layered DMFA """
    scenario_input: ScenarioInput
    plastic: DMFA
    decaBDE: DMFA
    TPP: DMFA

def calculate_layered_DMFA(scenario_input: ScenarioInput) -> LayeredDMFA:

    years = scenario_input.df_input.index

    # create dmfa configuration
    dmfa_configuration = DMFAConfiguration(
        time_start=years.min(),
        time_end=years.max(),
        lifespan=15,
    )
    
    ### PLASTIC ### 
    # create plastic dmfa and set coefficients
    dmfa_plastic = DMFA(dmfa_configuration)
    dmfa_plastic.set_transfer_coefficients(scenario_input.df_plastic_TFs)

    # calculate the plastic inflow and outflows from the stock (stockdriven)
    usephase_plastic = calculate_use_phase_stockdriven(
        stock=scenario_input.plastic_stock.to_numpy(),
        dmfa_configuration=dmfa_configuration
    )
    # solve the remaining plastic flows and stocks 
    for t in range(dmfa_configuration.Nt):
        dmfa_plastic.solve_flows_and_stocks(usephase_plastic, t=t)

    # shift the export flow and stock by 5 years, and 
    # correct the inflow according to:
    # dS(t) = i(t) - (o_dismantling(t) + o_export(t + 5))  # mass balance
    # i(t) = dS(t) + (o_dismantling(t) + o_export(t+5) )  # correct inflow
    dmfa_plastic.shift_export_flow_and_stock(num_years=5)
    usephase_plastic.inflow = (
        usephase_plastic.stock_change + 
        (dmfa_plastic.F_1_2.values + dmfa_plastic.F_1_9.values)                    
    )
    dmfa_plastic.usephase = usephase_plastic

    ### DECABDE ###
    # create decaBDE dmfa and set transfer coefficients 
    dmfa_decaBDE = DMFA(dmfa_configuration)
    dmfa_decaBDE.set_transfer_coefficients(scenario_input.df_decaBDE_TFs)
    
    # calculate the decaBDE inflow by multiplying the plastic inflow by the decaBDE inflow share
    inflow_decaDBE = usephase_plastic.inflow * scenario_input.decaBDE_inflow_share.to_numpy()
    
    # calculate the decaBDE stock and outflow from the inflow (inflowdriven)
    usephase_decaBDE = calculate_use_phase_inflowdriven(
        inflow=inflow_decaDBE,
        dmfa_configuration=dmfa_configuration,
    )
    # solve the remaining decaBDE flows and stocks 
    for t in range(dmfa_configuration.Nt):
        dmfa_decaBDE.solve_flows_and_stocks(usephase_decaBDE, t=t)
    dmfa_decaBDE.usephase = usephase_decaBDE   
    
    # add the emissions to the environment from the Production process (outside dmfa)
    inflow_recycled = dmfa_decaBDE.F_2_1.values + dmfa_decaBDE.F_4_1.values 
    inflow_new = dmfa_decaBDE.usephase.inflow - inflow_recycled
    # ef: emission_factor
    # dS_0_from_production = ef * production_inflow 
    # inflow_new = (1-ef) * production_inflow
    # dS_0_from_production = ef / (1-ef) * inflow_new 
    ef_decaBDE = scenario_input.production_emission_factor_decaBDE
    dS_0_from_production = inflow_new * ef_decaBDE / (1-ef_decaBDE)
    dmfa_decaBDE.dS_0.values += dS_0_from_production
    
    ### TPP ###
    # create TPP dmfa and set transfer coefficients 
    dmfa_TPP = DMFA(dmfa_configuration)
    dmfa_TPP.set_transfer_coefficients(scenario_input.df_TPP_TFs)

    # calculate the TPP inflow by multiplying the plastic inflow by the TPP inflow share
    inflow_TPP = usephase_plastic.inflow * scenario_input.TPP_inflow_new_share.to_numpy()
    # calculate the TPP stock and outflow from the inflow (inflowdriven)
    usephase_TPP = calculate_use_phase_inflowdriven(
        inflow=inflow_TPP,
        dmfa_configuration=dmfa_configuration,
    )
    # solve the remaining TPP flows and stocks 
    for t in range(dmfa_configuration.Nt):
        dmfa_TPP.solve_flows_and_stocks(usephase_TPP, t=t)
    
    dmfa_TPP.usephase = usephase_TPP    
    
    # add the emissions to the environment from the Production process (outside dmfa)
    inflow_recycled = dmfa_TPP.F_2_1.values + dmfa_TPP.F_4_1.values 
    inflow_new = dmfa_TPP.usephase.inflow - inflow_recycled
    
    # ef: emission_factor
    # dS_0_from_production = ef * production_inflow 
    # inflow_new = (1-ef) * production_inflow
    # dS_0_from_production = ef / (1-ef) * inflow_new 
    ef_TPP = scenario_input.production_emission_factor_TPP
    dS_0_from_production = inflow_new * ef_TPP / (1-ef_TPP)
    dmfa_TPP.dS_0.values += dS_0_from_production
        
    layered_dmfa = LayeredDMFA(
        scenario_input=scenario_input,
        plastic=dmfa_plastic,
        decaBDE=dmfa_decaBDE,
        TPP=dmfa_TPP
    )
    return layered_dmfa
