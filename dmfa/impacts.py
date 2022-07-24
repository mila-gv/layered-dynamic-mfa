from dataclasses import dataclass
from dmfa.layered_dmfa import LayeredDMFA 
import numpy as np 

@dataclass
class MidpointImpact:
    human_carcinogenic_toxicity: np.ndarray  
    human_non_carcinogenic_toxicity: np.ndarray  
    terrestrial_ecotoxicity: np.ndarray
    freshwater_ecotoxicity: np.ndarray
    marine_ecotoxicity: np.ndarray 
    CO2_global_warming: np.ndarray 
    
@dataclass 
class EndpointImpact:
    human_health: np.ndarray 
    human_health_without_global_warming: np.ndarray
    human_health_only_global_warming: np.ndarray 
    
    ecosystem_health: np.ndarray
    ecosystem_health_without_global_warming: np.ndarray
    ecosystem_health_only_global_warming: np.ndarray
    
@dataclass 
class Impacts:
    midpoint_impact: MidpointImpact
    endpoint_impact: EndpointImpact
    
def calculate_impacts(layered_dmfa: LayeredDMFA) -> Impacts:
    scenario_input = layered_dmfa.scenario_input
    
    dS_0_decaBDE = layered_dmfa.decaBDE.dS_0.values
    dS_0_TPP = layered_dmfa.TPP.dS_0.values
    
    incineration_flow_decaBDE = layered_dmfa.decaBDE.F_2_3.values - layered_dmfa.decaBDE.F_3_0.values
    CO2_conversion_decaBDE = 0.055047
    CO2_decaBDE = incineration_flow_decaBDE * CO2_conversion_decaBDE
    incineration_flow_TPP = layered_dmfa.TPP.F_2_3.values - layered_dmfa.TPP.F_3_0.values
    CO2_conversion_TPP = 2.4273
    CO2_TPP = incineration_flow_TPP * CO2_conversion_TPP
    CO2_global_warming = (CO2_decaBDE + CO2_TPP)
    
    midpoint_impact = MidpointImpact(
        human_carcinogenic_toxicity = (dS_0_decaBDE * 
            scenario_input.df_decaBDE_CFs.loc['human carcinogenic toxicity', 'mid point characterization factor (kg 1,4-DCB / kg)']
        ),
        human_non_carcinogenic_toxicity = (dS_0_decaBDE *
            scenario_input.df_decaBDE_CFs.loc['human non-carcinogenic toxicity', 'mid point characterization factor (kg 1,4-DCB / kg)']
        ),
        terrestrial_ecotoxicity = (dS_0_TPP *
            scenario_input.df_TPP_CFs.loc['terrestrial ecotoxicity', 'mid point characterization factor (kg 1,4-DCB / kg)']    
        ),
        freshwater_ecotoxicity = (dS_0_TPP *
            scenario_input.df_TPP_CFs.loc['freshwater ecotoxicity', 'mid point characterization factor (kg 1,4-DCB / kg)']    
        ),
        marine_ecotoxicity = (dS_0_TPP *
            scenario_input.df_TPP_CFs.loc['marine ecotoxicity', 'mid point characterization factor (kg 1,4-DCB / kg)']    
        ),
        CO2_global_warming = CO2_global_warming,
    )
    
    
    human_health_without_global_warming = dS_0_decaBDE * (
            scenario_input.df_decaBDE_CFs.loc['human carcinogenic toxicity', 'end point characterization factor (DALY/kg)']
            + scenario_input.df_decaBDE_CFs.loc['human non-carcinogenic toxicity', 'end point characterization factor (DALY/kg)']
        ) 
    human_health_only_global_warming = scenario_input.CO2_endpoint_CF_health * CO2_global_warming
    human_health = human_health_without_global_warming + human_health_only_global_warming 
    
    ecosystem_health_without_global_warming = dS_0_TPP * (
            scenario_input.df_TPP_CFs.loc['terrestrial ecotoxicity', 'end point characterization factor (species.yr/kg)']
            + scenario_input.df_TPP_CFs.loc['freshwater ecotoxicity', 'end point characterization factor (species.yr/kg)']
            + scenario_input.df_TPP_CFs.loc['marine ecotoxicity', 'end point characterization factor (species.yr/kg)']
        )
    ecosystem_health_only_global_warming = CO2_global_warming * (
        scenario_input.CO2_endpoint_CF_terrestrial 
        + scenario_input.CO2_endpoint_CF_freshwater)
    ecosystem_health = ecosystem_health_without_global_warming + ecosystem_health_only_global_warming
    
    endpoint_impact = EndpointImpact(
        human_health = human_health,
        human_health_without_global_warming = human_health_without_global_warming,
        human_health_only_global_warming = human_health_only_global_warming,
        ecosystem_health = ecosystem_health,
        ecosystem_health_without_global_warming = ecosystem_health_without_global_warming,
        ecosystem_health_only_global_warming = ecosystem_health_only_global_warming,
    )

    return Impacts(
        midpoint_impact,
        endpoint_impact,
    )

