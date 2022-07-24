from dmfa.dmfa import Flow
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from dmfa.layered_dmfa import LayeredDMFA
from dmfa.impacts import calculate_impacts
from copy import deepcopy 
import io

def download_df_button(df: pd.DataFrame, filename: str):
    
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=filename)

    st.download_button(
        label="Download as Excel",
        data=buffer,
        file_name=f"{filename}.xlsx",
        mime="application/vnd.ms-excel"
    )
    

def select_scenario(layered_dmfas: list[LayeredDMFA], title: str) -> list[LayeredDMFA]:
    
    scenario_numbers = [layered_dmfa.scenario_input.scenario_number 
                        for layered_dmfa in layered_dmfas]
    selected_scenario_numbers = st.multiselect(
        title,
        options=scenario_numbers,
        default=scenario_numbers,
    )
    selected_layered_dmfas = [layered_dmfa 
                              for layered_dmfa in layered_dmfas 
                              if layered_dmfa.scenario_input.scenario_number in selected_scenario_numbers]
    return selected_layered_dmfas
    

def download_timeseries_button(df: pd.DataFrame, filename: str):
    """ assumes year name vlaue"""
    if df.empty: return 
    df_table = df.pivot(index='year', columns='name')['value']
    download_df_button(df_table, filename)


def download_barplot_button(df: pd.DataFrame, filename: str):
    """ assumes year name"""
    if df.empty: return 
    download_df_button(df, filename)
    

def plot_usephase_inflow_and_outflow(layered_dmfas: list[LayeredDMFA]):
    
    selected_layered_dmfas = select_scenario(layered_dmfas, 'Select your scenarioo')
    selected_dmfas = st.multiselect(
        'Select dmfa layerss',   
        options=['plastic', 'decaBDE', 'TPP'],
        default=['decaBDE', 'TPP'],
    )
    
    time_list = layered_dmfas[0].plastic.dmfa_configruation.time_list
    
    rows_inflows_outflows = []
    rows_stocks = []
    for layered_dmfa in selected_layered_dmfas:
        name = f'scenario={layered_dmfa.scenario_input.scenario_number}'
        for i, year in enumerate(time_list):
            if 'plastic' in selected_dmfas:
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_inflow_plastic',
                    'value': layered_dmfa.plastic.usephase.inflow[i]
                })
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_outflow_plastic',
                    'value': layered_dmfa.plastic.usephase.outflow[i]
                })
                rows_stocks.append({
                     'year': year,
                    'name': name+'_stock_plastic',
                    'value': layered_dmfa.plastic.usephase.stock[i]
                })
            if 'decaBDE' in selected_dmfas:
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_inflow_decaBDE',
                    'value': layered_dmfa.decaBDE.usephase.inflow[i]
                })
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_outflow_decaBDE',
                    'value': layered_dmfa.decaBDE.usephase.outflow[i]
                })  
                rows_stocks.append({
                     'year': year,
                    'name': name+'_stock_decaBDE',
                    'value': layered_dmfa.decaBDE.usephase.stock[i]
                })
            if 'TPP' in selected_dmfas:
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_inflow_TPP',
                    'value': layered_dmfa.TPP.usephase.inflow[i]
                })
                rows_inflows_outflows.append({
                    'year': year,
                    'name': name+'_outflow_TPP',
                    'value': layered_dmfa.TPP.usephase.outflow[i]
                })
                
                rows_stocks.append({
                     'year': year,
                    'name': name+'_stock_TPP',
                    'value': layered_dmfa.TPP.usephase.stock[i]
                })
            
    df_plot = pd.DataFrame(rows_inflows_outflows)
    fig = px.line(df_plot, x="year", y="value", color="name")
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "inflow outflow timeseries")
    
    df_plot = pd.DataFrame(rows_stocks)
    fig = px.line(df_plot, x="year", y="value", color="name")
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "stocks timeseries")
    
    
def plot_flows_and_stocks(layered_dmfas: list[LayeredDMFA]):
    
    selected_layered_dmfas = select_scenario(layered_dmfas, 'Select your scenarihohooo')
    selected_dmfas = st.multiselect(
        'Select dmfa layers',   
        options=['plastic', 'decaBDE', 'TPP'],
        default=['decaBDE', 'TPP'],
    )
    
    time_list = layered_dmfas[0].plastic.dmfa_configruation.time_list

    flow_names = [flow.name for flow in layered_dmfas[0].decaBDE.get_flows_and_stocks()]
    selected_flow_names = st.multiselect(
        'Select relevant flows',
        options=flow_names,
        default=[],
    )
    flows: list[Flow] = [] 
    
    for layered_dmfa in selected_layered_dmfas:
        for flow_name in selected_flow_names:
            for selected_dmfa in selected_dmfas:
                flow: Flow
                if selected_dmfa == 'plastic':
                    flow: Flow = layered_dmfa.plastic.__dict__[flow_name]
                elif selected_dmfa == 'decaBDE':
                    flow: Flow = layered_dmfa.decaBDE.__dict__[flow_name]
                elif selected_dmfa == 'TPP':
                    flow: Flow = layered_dmfa.TPP.__dict__[flow_name]
                else: 
                    continue
                flow = deepcopy(flow)
                flow.name += f'_{selected_dmfa}_scenario={layered_dmfa.scenario_input.scenario_number}'
                flows.append(flow)

    
    time_list = layered_dmfas[0].plastic.dmfa_configruation.time_list

    values = [flow.values for flow in flows]

    flow_names = [[flow.name] * len(time_list) for flow in flows]
    years = [time_list] * len(flows)
    df_plot = pd.DataFrame()
    df_plot['year'] = np.ravel(years)
    df_plot['value'] = np.ravel(values)
    df_plot['name'] = np.ravel(flow_names)

    fig = px.line(df_plot, x="year", y="value", color='name')
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "flows timeseries")

def plot_impacts(layered_dmfas: list[LayeredDMFA]) -> None:
    st.write("health: eat your veggies")
    selected_layered_dmfas = select_scenario(layered_dmfas, "select that scenario baby")
    
    time_list = layered_dmfas[0].plastic.dmfa_configruation.time_list

    rows_midpoint = []
    rows_endpoint = []
    rows_bars_human_health_without_global = []
    rows_bars_human_health_split = []
    rows_bars_ecosystem_health_without_global = []
    rows_bars_ecosystem_health_split = []
    rows_global_warming = []
    
    years = range(1980, 2050)
    health_start_year = st.selectbox(
        "Select health barplot start year",
        years,
        index=0,
    )
    health_stop_year = st.selectbox(
        "Select health barplot start year",
        years,
        index=len(years)-1,
    )
    health_start_year_index = health_start_year-years[0]
    health_stop_year_index = health_stop_year-years[0]
    
    for layered_dmfa in selected_layered_dmfas: 
        impact = calculate_impacts(layered_dmfa)
        
        name = f'scenario={layered_dmfa.scenario_input.scenario_number}'
        
        midpoint_timeseries_dict = {
            name+'_human_carcinogenic': impact.midpoint_impact.human_carcinogenic_toxicity,
            name+'_human_non_carcinogenic': impact.midpoint_impact.human_non_carcinogenic_toxicity,
            name+'_freshwata': impact.midpoint_impact.freshwater_ecotoxicity,
            name+'_marine': impact.midpoint_impact.marine_ecotoxicity,
            name+'_terrestrial': impact.midpoint_impact.terrestrial_ecotoxicity,
        }
        
        endpoint_timeseries_dict = {
            name+'_human_health': impact.endpoint_impact.human_health,
            name+'_ecosystem_health': impact.endpoint_impact.ecosystem_health,
        }
        
        rows_bars_human_health_without_global.append({
            'name': name,
            'value': sum(impact.endpoint_impact.human_health_without_global_warming[health_start_year_index:health_stop_year_index]),
        })
        rows_bars_human_health_split.append({
            'name': name,
            'value': sum(impact.endpoint_impact.human_health_without_global_warming[health_start_year_index:health_stop_year_index]),
            'color': 'without global warming'
        })
        rows_bars_human_health_split.append({
            'name': name,
            'value': sum(impact.endpoint_impact.human_health_only_global_warming[health_start_year_index:health_stop_year_index]),
            'color': 'only global warming'
        })
        
        rows_bars_ecosystem_health_without_global.append({
            'name': name,
            'value': sum(impact.endpoint_impact.ecosystem_health_without_global_warming[health_start_year_index:health_stop_year_index]),
        })
        rows_bars_ecosystem_health_split.append({
            'name': name,
            'value': sum(impact.endpoint_impact.ecosystem_health_without_global_warming[health_start_year_index:health_stop_year_index]),
            'color': "without global warming"
        })
        rows_bars_ecosystem_health_split.append({
            'name': name,
            'value': sum(impact.endpoint_impact.ecosystem_health_only_global_warming[health_start_year_index:health_stop_year_index]),
            'color': "only global warming"
        })
            
        for name, timeseries in midpoint_timeseries_dict.items():
            for i, year in enumerate(time_list):
                rows_midpoint.append({
                    'year': year,
                    'name': name,
                    'value': timeseries[i],
                })
        
        for i, year in enumerate(time_list):
            rows_global_warming.append({
                'name': name+"_gloabal_warming",
                'year': year, 
                'value': impact.midpoint_impact.CO2_global_warming[i]
            })
            
        for name, timeseries in endpoint_timeseries_dict.items():
            for i, year in enumerate(time_list):
                rows_endpoint.append({
                    'year': year,
                    'name': name,
                    'value': timeseries[i],
                })

    st.write('midpoint impacts')
    df_plot = pd.DataFrame(rows_midpoint)
    fig = px.line(df_plot, x='year', y='value', color='name')
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "midpoint timeseries")
    
    st.write('global warming')
    df_plot = pd.DataFrame(rows_global_warming)
    fig = px.line(df_plot, x='year', y='value', color='name')
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "CO2 global warming")
    
    st.write('endpoints impacts')
    df_plot = pd.DataFrame(rows_endpoint)
    fig = px.line(df_plot, x='year', y='value', color='name')
    st.plotly_chart(fig)
    download_timeseries_button(df_plot, "endpoint timeseries")
    
    
    st.write('human health sums without global')
    df_plot = pd.DataFrame(rows_bars_human_health_without_global)
    fig = px.bar(df_plot, x='name', y='value')
    st.plotly_chart(fig)
    download_barplot_button(df_plot, "human health bar without global")
    
    st.write('human health sums split')
    df_plot = pd.DataFrame(rows_bars_human_health_split)
    fig = px.bar(df_plot, x='name', y='value', color="color")
    st.plotly_chart(fig)
    download_barplot_button(df_plot, "human health barplot split")
    
    st.write('ecosystem health sums without global')
    df_plot = pd.DataFrame(rows_bars_ecosystem_health_without_global)
    fig = px.bar(df_plot, x='name', y='value')
    st.plotly_chart(fig)
    download_barplot_button(df_plot, "ecosystemhealthbarwithoutglobal")
    
    st.write('ecosystem health sums split')
    df_plot = pd.DataFrame(rows_bars_ecosystem_health_split)
    fig = px.bar(df_plot, x='name', y='value', color="color")
    st.plotly_chart(fig)
    download_barplot_button(df_plot, "ecosystem health barplot split")
    
    
def plot_inflows(layered_dmfas: list[LayeredDMFA]) -> None:
    st.write("Compare inflows")
    selected_layered_dmfas = select_scenario(layered_dmfas, "select that scenario baby cheerios")
    selected_dmfas = st.multiselect(
        'Select dmfa layers',   
        options=['plastic', 'decaBDE', 'TPP'],
        default=['plastic', 'decaBDE', 'TPP'],
    )
    
    time_list = layered_dmfas[0].plastic.dmfa_configruation.time_list

    rows = []
    for layered_dmfa in selected_layered_dmfas:
        
        name = f'{layered_dmfa.scenario_input.scenario_number}'
        for i, year in enumerate(time_list):
            if 'plastic' in selected_dmfas:
                inflow = layered_dmfa.plastic.usephase.inflow[i]
                inflow_recycled = (
                    layered_dmfa.plastic.F_2_1.values[i] + 
                    layered_dmfa.plastic.F_4_1.values[i] )
                percentage = 100 * inflow_recycled / inflow if inflow != 0 else 0
                rows.append({
                    'value': percentage,
                    'year': year,
                    'name': name+'_percentage_recycled_inflow_plastic'
                })
            if 'decaBDE' in selected_dmfas:
                inflow = layered_dmfa.decaBDE.usephase.inflow[i]
                inflow_recycled = (
                    layered_dmfa.decaBDE.F_2_1.values[i] + 
                    layered_dmfa.decaBDE.F_4_1.values[i] )
                percentage = 100 * inflow_recycled / inflow if inflow != 0 else 0 
                rows.append({
                    'value': percentage,
                    'year': year,
                    'name': name+'_percentage_recycled_inflow_decaBDE'
                })
            if 'TPP' in selected_dmfas:
                inflow = layered_dmfa.TPP.usephase.inflow[i]
                inflow_recycled = (
                    layered_dmfa.TPP.F_2_1.values[i] + 
                    layered_dmfa.TPP.F_4_1.values[i] )
                percentage = 100 * inflow_recycled / inflow if inflow != 0 else 0 
                rows.append({
                    'value': percentage,
                    'year': year,
                    'name': name+'_percentage_recycled_inflow_TPP'
                })
    
    df_plot = pd.DataFrame(rows)
    fig = px.line(df_plot, x='year', y='value', color='name')
    st.plotly_chart(fig)    