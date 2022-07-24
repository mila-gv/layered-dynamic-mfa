import pandas as pd
from dataclasses import dataclass
import streamlit as st 

@dataclass
class ScenarioInput:
    scenario_number: int
    scenario_name: str
    df_input: pd.DataFrame
    plastic_stock: pd.Series
    df_plastic_TFs: pd.DataFrame
    
    decaBDE_inflow_share: pd.Series
    df_decaBDE_TFs: pd.DataFrame
    df_decaBDE_CFs: pd.DataFrame
    
    TPP_inflow_new_share: pd.Series
    df_TPP_TFs: pd.DataFrame
    df_TPP_CFs: pd.DataFrame
    
    production_emission_factor_decaBDE: float
    production_emission_factor_TPP: float
    CO2_endpoint_CF_health: float
    CO2_endpoint_CF_terrestrial: float 
    CO2_endpoint_CF_freshwater: float

@st.cache
def import_scenarios(excel_path) -> list[ScenarioInput]:
    """ Reads the excel with all provided sheets and scenarios and outputs it 
        as a ScenarioInput class used for calculating the layered DMFA effects """
    # emission factors 
    df_emission_factors = pd.read_excel(
        excel_path, sheet_name="EFs", index_col="life cycle phase", engine='openpyxl'
    )
    
    production_emission_factor_decaBDE = df_emission_factors.loc['production', 'decaBDE']
    production_emission_factor_TPP = df_emission_factors.loc['production', 'TPP']
    
    
    df_decaBDE_CFs = pd.read_excel(
        excel_path, sheet_name="decaBDE_CFs", index_col="impact category", engine='openpyxl'
    )
    
    # co2 characterization factors
    df_CO2_CFs = pd.read_excel(
        excel_path, sheet_name="CO2_CFs", index_col="impact category", engine='openpyxl'
    )
    CO2_endpoint_CF_health = df_CO2_CFs.loc['global warming, human health', 'end point characterization factor (DALY / kg)']
    CO2_endpoint_CF_terrestrial = df_CO2_CFs.loc['global warming, terrestrial ecosystems', 'end point characterization factor (species.yr/kg)']
    CO2_endpoint_CF_freshwater = df_CO2_CFs.loc['global warming, freshwater ecosystems', 'end point characterization factor (species.yr/kg)']
    
    # TPP CFS
    df_TPP_CFs = pd.read_excel(
        excel_path, sheet_name="TPP_CFs", index_col="impact category", engine='openpyxl'
    )

    
    sheet_names = pd.ExcelFile(excel_path).sheet_names
    scenario_numbers = sorted(set([int(num)
                                   for sheet_name in sheet_names
                                   if (num := sheet_name[0]).isdigit()]))

    scenario_inputs: list[ScenarioInput] = []
    for scenario_number in scenario_numbers:
        df_fleet = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_fleet", index_col='year', engine='openpyxl')
        df_fleet = df_fleet[['vehicle stock']]

        df_plastic = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_plastic_share", index_col='year', engine='openpyxl')

        df_plastic = df_plastic[[
            'plastic share', 'average vehicle weight']]
        df_plastic = df_plastic.reindex(df_fleet.index)
        df_plastic = df_plastic.interpolate('linear')

        df_input = df_fleet.join(df_plastic)    
        
        df_input['plastic stock (ton)'] = (
            df_input['vehicle stock'] *
            df_input['plastic share'] *
            df_input['average vehicle weight']
        )
        
        df_plastic_TFs = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_plastics_TFs", index_col='year', engine='openpyxl')
        
        # decaBDE specific
        df_decaBDE_share = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_decaBDE_share", index_col='year', engine='openpyxl')

        df_decaBDE_TFs = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_decaBDE_TFs", index_col='year', engine='openpyxl')
        
        # TPP specific
        df_TPP_TFs = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_TPP_TFs", index_col='year', engine='openpyxl')

        df_TPP_share = pd.read_excel(
            excel_path, sheet_name=f"{scenario_number}_TPP_share", index_col='year', engine='openpyxl')

        scenario_inputs.append(
            ScenarioInput(
                scenario_number=scenario_number,
                scenario_name="",
                df_input=df_input.join(df_decaBDE_share).join(df_TPP_share),
                plastic_stock=df_input['plastic stock (ton)'],
                df_plastic_TFs=df_plastic_TFs,
                decaBDE_inflow_share=df_decaBDE_share['decaBDE content in new plastics'],
                df_decaBDE_TFs=df_decaBDE_TFs,
                df_decaBDE_CFs=df_decaBDE_CFs,
                
                TPP_inflow_new_share=df_TPP_share['TPP content in new plastics'],
                df_TPP_TFs=df_TPP_TFs,
                df_TPP_CFs=df_TPP_CFs,
                
                production_emission_factor_decaBDE = production_emission_factor_decaBDE,
                production_emission_factor_TPP = production_emission_factor_TPP,
                CO2_endpoint_CF_health = CO2_endpoint_CF_health,
                CO2_endpoint_CF_terrestrial = CO2_endpoint_CF_terrestrial,
                CO2_endpoint_CF_freshwater = CO2_endpoint_CF_freshwater,
            ))

    return scenario_inputs
