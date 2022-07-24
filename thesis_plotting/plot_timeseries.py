import functools
from attr import dataclass
import matplotlib.pyplot as plt 
import pandas as pd 

@dataclass 
class Line:
    key: str
    label: str
    color: str 
    
def plot_lines(filepath: str, 
                figure_filepath: str,
                lines: list[Line] = None,
                xlabel: str = None, 
                ylabel: str = None,
                aspect_ratio: float = 1,
                legend_location='top',
                kind = 'line'):

    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    lgd = None
    
    if kind == 'line':
        df = pd.read_excel(filepath, index_col='year')
        if lines is None:
            for column in df:
                ax.plot(df.index, df[column], label=column)
        else:
            for line in lines:
                ax.plot(df.index, df[line.key], label=line.label,  c=line.color)

        ax.margins(x=0, y=0)
        # legend
        if legend_location == 'right':
            lgd = ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5))
        elif legend_location == 'bottom':
            lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12))
        elif legend_location == 'top':
            lgd = ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=2)
        else:
            raise AssertionError(f"Invalid legend location {legend_location}")
    
    elif kind == 'bar':
        df = pd.read_excel(filepath, index_col='name')
        if lines is None:
            labels = df.index
            values = df['value']
            ax.bar(labels, values)
        else:
            labels = [line.label for line in lines]
            values = [df.loc[line.key, 'value'] for line in lines]
            colors = [line.color for line in lines]
            ax.bar(labels, values, color=colors)
    else:
        raise AssertionError(f"kind {kind} is not a valid kind")
    
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*aspect_ratio)

    bbox_extra_artists = None if lgd is None else (lgd,)
    fig.savefig(figure_filepath, bbox_extra_artists=bbox_extra_artists, 
                bbox_inches='tight', dpi=500)

plot_timeseries = functools.partial(plot_lines, kind='line')
plot_bar = functools.partial(plot_lines, kind='bar')

def main():
 
  #  plot_timeseries('thesis_plotting/data/stocks timeseries.xlsx',
  #                  'thesis_plotting/figures/stock_timeseries_all.png')
  #  plot_timeseries('thesis_plotting/data/stocks timeseries.xlsx', 
  #                  'thesis_plotting/figures/stock_timeseries_formatted.png',
  #                  lines = [
  #                      Line('scenario=0_stock_TPP', 'Scenario 0', 'deepskyblue'),
  #                      Line('scenario=4_stock_TPP', 'Scenario 4', 'orangered'),
  #                      Line('scenario=1_stock_TPP', 'Scenario 1', 'hotpink'),
  #                      Line('scenario=2_stock_TPP', 'Scenario 2', 'yellowgreen'),
  #                      Line('scenario=3_stock_TPP', 'Scenario 3', 'darkblue')
  #                  ],
  #                  xlabel='Time (year)',
  #                  ylabel='Total emissions (kg)')
                    #hotpink, deepskyblue, red, darkblue/navy/mediumblue, orange, yellowgreen

    plot_timeseries('thesis_plotting/data/total_emissions.xlsx',
                    'thesis_plotting/figures/total_TPP_emissions_sl.png')
    plot_timeseries('thesis_plotting/data/total_emissions.xlsx', 
                    'thesis_plotting/figures/total_TPP_emissions_formatted.png',
                    lines = [
                        Line('dS_0_TPP_scenario=0', 'Scenario 0', 'cornflowerblue'),
                        Line('dS_0_TPP_scenario=1', 'Scenario 1', 'forestgreen'),
                        Line('dS_0_TPP_scenario=2', 'Scenario 2', 'crimson'),
                        Line('dS_0_TPP_scenario=3', 'Scenario 3', 'mediumpurple'),
                        Line('dS_0_TPP_scenario=4', 'Scenario 4', 'darkorange'),
                        Line('dS_0_TPP_scenario=5', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Total TPP emissions (kg)')

    plot_timeseries('thesis_plotting/data/total_emissions.xlsx',
                    'thesis_plotting/figures/total_decaBDE_emissions_sl.png')
    plot_timeseries('thesis_plotting/data/total_emissions.xlsx', 
                    'thesis_plotting/figures/total_decaBDE_emissions_formatted.png',
                    lines = [
                        Line('dS_0_decaBDE_scenario=0', 'Scenario 0', 'cornflowerblue'),
                        Line('dS_0_decaBDE_scenario=1', 'Scenario 1', 'forestgreen'),
                        Line('dS_0_decaBDE_scenario=2', 'Scenario 2', 'crimson'),
                        Line('dS_0_decaBDE_scenario=3', 'Scenario 3', 'mediumpurple'),
                        Line('dS_0_decaBDE_scenario=4', 'Scenario 4', 'darkorange'),
                        Line('dS_0_decaBDE_scenario=5', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Total decaBDE emissions (kg)')    

    plot_timeseries('thesis_plotting/data/process_emissions_TPP.xlsx',
                    'thesis_plotting/figures/process_TPP_emissions_TPP_sl.png')
    plot_timeseries('thesis_plotting/data/process_emissions_TPP.xlsx', 
                    'thesis_plotting/figures/process_TPP_emissions_formatted.png',
                    lines = [
                        Line('dS_0_TPP_scenario=0', 'Total', 'cornflowerblue'),
                        Line('F_1_0_TPP_scenario=0', 'Vehicle Use', 'forestgreen'),
                        Line('F_2_0_TPP_scenario=0', 'Car Dismantling & others', 'crimson'),
                        Line('F_3_0_TPP_scenario=0', 'Incineration', 'mediumpurple'),
                        Line('F_4_0_TPP_scenario=0', 'Recycling', 'darkorange'),
                    ],
                    xlabel='Time (year)',
                    ylabel='TPP emissions to atmosphere (Scenario 0) (kg)')  

    plot_timeseries('thesis_plotting/data/process_emissions_decaBDE.xlsx',
                    'thesis_plotting/figures/process_decaBDE_emissions_sl.png')
    plot_timeseries('thesis_plotting/data/process_emissions_decaBDE.xlsx', 
                    'thesis_plotting/figures/process_decaBDE_emissions_formatted.png',
                    lines = [
                        Line('dS_0_decaBDE_scenario=0', 'Total', 'cornflowerblue'),
                        Line('F_1_0_decaBDE_scenario=0', 'Vehicle Use', 'forestgreen'),
                        Line('F_2_0_decaBDE_scenario=0', 'Car Dismantling & others', 'crimson'),
                        Line('F_3_0_decaBDE_scenario=0', 'Incineration', 'mediumpurple'),
                        Line('F_4_0_decaBDE_scenario=0', 'Recycling', 'darkorange'),
                    ],
                    xlabel='Time (year)',
                    ylabel='DecaBDE emissions to atmosphere (Scenario 0) (kg)')   

    plot_timeseries('thesis_plotting/data/process_emissions_TPP.xlsx',
                    'thesis_plotting/figures/process_TPP_emissions_TPP_sl.png')
    plot_timeseries('thesis_plotting/data/process_emissions_TPP.xlsx', 
                    'thesis_plotting/figures/process_TPP_emissions_1_formatted.png',
                    lines = [
                        Line('dS_0_TPP_scenario=1', 'Total', 'cornflowerblue'),
                        Line('F_1_0_TPP_scenario=1', 'Vehicle Use', 'forestgreen'),
                        Line('F_2_0_TPP_scenario=1', 'Car Dismantling & others', 'crimson'),
                        Line('F_3_0_TPP_scenario=1', 'Incineration', 'mediumpurple'),
                        Line('F_4_0_TPP_scenario=1', 'Recycling', 'darkorange'),
                    ],
                    xlabel='Time (year)',
                    ylabel='TPP emissions to atmosphere (Scenario 1) (kg)') 

    plot_timeseries('thesis_plotting/data/process_emissions_decaBDE.xlsx',
                    'thesis_plotting/figures/process_decaBDE_emissions_sl.png')
    plot_timeseries('thesis_plotting/data/process_emissions_decaBDE.xlsx', 
                    'thesis_plotting/figures/process_decaBDE_emissions_1_formatted.png',
                    lines = [
                        Line('dS_0_decaBDE_scenario=1', 'Total', 'cornflowerblue'),
                        Line('F_1_0_decaBDE_scenario=1', 'Vehicle Use', 'forestgreen'),
                        Line('F_2_0_decaBDE_scenario=1', 'Car Dismantling & others', 'crimson'),
                        Line('F_3_0_decaBDE_scenario=1', 'Incineration', 'mediumpurple'),
                        Line('F_4_0_decaBDE_scenario=1', 'Recycling', 'darkorange'),
                    ],
                    xlabel='Time (year)',
                    ylabel='DecaBDE emissions to atmosphere (Scenario 1) (kg)')      

    plot_timeseries('thesis_plotting/data/stocks_FRs.xlsx',
                    'thesis_plotting/figures/stocks_TPP_sl.png')
    plot_timeseries('thesis_plotting/data/stocks_FRs.xlsx', 
                    'thesis_plotting/figures/stocks_TPP_formatted.png',
                    lines = [
                        Line('scenario=0_stock_TPP', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_stock_TPP', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_stock_TPP', 'Scenario 2', 'crimson'),
                        Line('scenario=3_stock_TPP', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_stock_TPP', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_stock_TPP', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Stock of TPP in Vehicle Use process (kg)')     

    plot_timeseries('thesis_plotting/data/stocks_FRs.xlsx',
                    'thesis_plotting/figures/stocks_decaBDE_sl.png')
    plot_timeseries('thesis_plotting/data/stocks_FRs.xlsx', 
                    'thesis_plotting/figures/stocks_decaBDE_formatted.png',
                    lines = [
                        Line('scenario=0_stock_decaBDE', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_stock_decaBDE', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_stock_decaBDE', 'Scenario 2', 'crimson'),
                        Line('scenario=3_stock_decaBDE', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_stock_decaBDE', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_stock_decaBDE', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Stock of decaBDE in Vehicle Use process (kg)')    

    plot_timeseries('thesis_plotting/data/stocks_plastics.xlsx',
                    'thesis_plotting/figures/stocks_plastics_sl.png')
    plot_timeseries('thesis_plotting/data/stocks_plastics.xlsx', 
                    'thesis_plotting/figures/stocks_plastics_formatted.png',
                    lines = [
                        Line('scenario=0_stock_plastic', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_stock_plastic', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_stock_plastic', 'Scenario 2', 'crimson'),
                        Line('scenario=3_stock_plastic', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_stock_plastic', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_stock_plastic', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Stock of plastics in Vehicle Use process (kg)')   

    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_toxicity_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx', 
                    'thesis_plotting/figures/mid_human_non_carcinogenic.png',
                    lines = [
                        Line('scenario=0_human_non_carcinogenic', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_human_non_carcinogenic', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_human_non_carcinogenic', 'Scenario 2', 'crimson'),
                        Line('scenario=3_human_non_carcinogenic', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_human_non_carcinogenic', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_human_non_carcinogenic', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Human toxicity (non-carcinogenic) potential (kg 1,4-DCB)') 

    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_toxicity_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx', 
                    'thesis_plotting/figures/mid_human_carcinogenic.png',
                    lines = [
                        Line('scenario=0_human_carcinogenic', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_human_carcinogenic', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_human_carcinogenic', 'Scenario 2', 'crimson'),
                        Line('scenario=3_human_carcinogenic', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_human_carcinogenic', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_human_carcinogenic', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Human toxicity (carcinogenic) potential (kg 1,4-DCB)') 

    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_toxicity_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx', 
                    'thesis_plotting/figures/mid_ecosystem_terrestrial.png',
                    lines = [
                        Line('scenario=0_terrestrial', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_terrestrial', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_terrestrial', 'Scenario 2', 'crimson'),
                        Line('scenario=3_terrestrial', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_terrestrial', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_terrestrial', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Terrestrial ecotoxicity potential (kg 1,4-DCB)') 

    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_toxicity_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx', 
                    'thesis_plotting/figures/mid_ecosystem_freshwater.png',
                    lines = [
                        Line('scenario=0_freshwata', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_freshwata', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_freshwata', 'Scenario 2', 'crimson'),
                        Line('scenario=3_freshwata', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_freshwata', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_freshwata', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Freshwater ecotoxicity potential (kg 1,4-DCB)') 

    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_toxicity_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_toxicity_impacts.xlsx', 
                    'thesis_plotting/figures/mid_ecosystem_marine.png',
                    lines = [
                        Line('scenario=0_marine', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_marine', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_marine', 'Scenario 2', 'crimson'),
                        Line('scenario=3_marine', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_marine', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_marine', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Marine ecotoxicity potential (kg 1,4-DCB)') 


    plot_timeseries('thesis_plotting/data/midpoint_globalwarming_impacts.xlsx',
                    'thesis_plotting/figures/midpoint_globalwarming_impacts.png')
    plot_timeseries('thesis_plotting/data/midpoint_globalwarming_impacts.xlsx', 
                    'thesis_plotting/figures/midpoint_globalwarming.png',
                    lines = [
                        Line('scenario=0_terrestrial_gloabal_warming', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_terrestrial_gloabal_warming', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_terrestrial_gloabal_warming', 'Scenario 2', 'crimson'),
                        Line('scenario=3_terrestrial_gloabal_warming', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_terrestrial_gloabal_warming', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_terrestrial_gloabal_warming', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Global warming potential (kg CO2)') 

    plot_timeseries('thesis_plotting/data/endpoint_timeseries.xlsx',
                    'thesis_plotting/figures/endpoint_timeseries.png')
    plot_timeseries('thesis_plotting/data/endpoint_timeseries.xlsx', 
                    'thesis_plotting/figures/endpoint_human_timeseries.png',
                    lines = [
                        Line('scenario=0_human_health', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_human_health', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_human_health', 'Scenario 2', 'crimson'),
                        Line('scenario=3_human_health', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_human_health', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_human_health', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Damage to human health (DALYs)') 

    plot_timeseries('thesis_plotting/data/endpoint_timeseries.xlsx',
                    'thesis_plotting/figures/endpoint_timeseries.png')
    plot_timeseries('thesis_plotting/data/endpoint_timeseries.xlsx', 
                    'thesis_plotting/figures/endpoint_ecosystem_timeseries.png',
                    lines = [
                        Line('scenario=0_ecosystem_health', 'Scenario 0', 'cornflowerblue'),
                        Line('scenario=1_ecosystem_health', 'Scenario 1', 'forestgreen'),
                        Line('scenario=2_ecosystem_health', 'Scenario 2', 'crimson'),
                        Line('scenario=3_ecosystem_health', 'Scenario 3', 'mediumpurple'),
                        Line('scenario=4_ecosystem_health', 'Scenario 4', 'darkorange'),
                        Line('scenario=5_ecosystem_health', 'Scenario 5', 'darkgray')
                    ],
                    xlabel='Time (year)',
                    ylabel='Damage to ecosystems (species * year)') 

    plot_bar('thesis_plotting/data/endpoint_human_noglobal.xlsx',
             'thesis_plotting/figures/endpoint_human_noglobal.png')
    plot_bar('thesis_plotting/data/endpoint_human_noglobal.xlsx',
             'thesis_plotting/figures/endpoints_human_noglobal.png',
             lines = [
                Line('scenario=0', 'S0', 'cornflowerblue'),
                Line('scenario=1', 'S1', 'cornflowerblue'),
                Line('scenario=2', 'S2', 'cornflowerblue'),
                Line('scenario=3', 'S3', 'cornflowerblue'),               
                Line('scenario=4', 'S4', 'cornflowerblue'),
                Line('scenario=5', 'S5', 'cornflowerblue'),
            ],
             ylabel='Damage to human health (DALYs')


    plot_bar('thesis_plotting/data/endpoint_ecosystem_noglobal.xlsx',
             'thesis_plotting/figures/endpoint_ecosystem_noglobal.png')
    plot_bar('thesis_plotting/data/endpoint_ecosystem_noglobal.xlsx',
             'thesis_plotting/figures/endpoints_ecosystem_noglobal.png',
             lines = [
                Line('scenario=0', 'S0', 'forestgreen'),
                Line('scenario=1', 'S1', 'forestgreen'),
                Line('scenario=2', 'S2', 'forestgreen'),
                Line('scenario=3', 'S3', 'forestgreen'),               
                Line('scenario=4', 'S4', 'forestgreen'),
                Line('scenario=5', 'S5', 'forestgreen'),
            ],
             ylabel='Damage to ecosystems ((species * year)')

if __name__ == "__main__":
    main()