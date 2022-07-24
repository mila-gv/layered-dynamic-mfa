import streamlit as st
from dmfa.scenario_input import import_scenarios
from dmfa.layered_dmfa import LayeredDMFA, calculate_layered_DMFA
from figures import plot_flows_and_stocks, plot_impacts, plot_inflows, plot_usephase_inflow_and_outflow
import streamlit as st
st.set_page_config(page_title='Thesis', layout='wide')

def show_comparison():

    if not layered_dmfas:
        st.write("No file loaded")
        return 
        
    with st.expander("Impacts"):
        plot_impacts(layered_dmfas)
    
    with st.expander("Usephase"):
        plot_usephase_inflow_and_outflow(layered_dmfas)

    with st.expander("Flows and stocks"):
        plot_flows_and_stocks(layered_dmfas)

def show_sidebar():
    uploaded_file = st.sidebar.file_uploader("Upload", type=['xlsx', 'xls'])

    # uploaded_file = 'data/dmfa_data.xlsx'
    if uploaded_file is not None:

        scenario_inputs = import_scenarios(uploaded_file)
        st.sidebar.write(f"✔️ {uploaded_file.name}")
        st.sidebar.write(
            f"✔️ number of scenarios found: {len(scenario_inputs)}")

        layered_dmfas.clear()  # reset
        for scenario_input in scenario_inputs:
            layered_dmfa = calculate_layered_DMFA(scenario_input)
            layered_dmfas.append(layered_dmfa)

layered_dmfas: list[LayeredDMFA] = []
show_sidebar()
show_comparison()