'''TAQ data main module.

The functions in the module run the complete analysis and plot of the TAQ data.

This script requires the following modules:
    * itertools.product
    * multiprocessing
    * pandas
    * pickle
    * taq_data_analysis_responses_activity
    * taq_data_plot_responses_activity
    * taq_data_tools_responses_activity

The module contains the following functions:
    * taq_data_plot_generator - generates all the analysis and plots from the
      TAQ data.
    * main - the main function of the script.

.. moduleauthor:: Juan Camilo Henao Londono <www.github.com/juanhenao21>
'''

# -----------------------------------------------------------------------------
# Modules

from itertools import product as iprod
import multiprocessing as mp
import pandas as pd
import pickle

import taq_data_analysis_responses_activity
import taq_data_plot_responses_activity
import taq_data_tools_responses_activity

# -----------------------------------------------------------------------------


def taq_data_plot_generator(tickers, year):
    """Generates all the analysis and plots from the TAQ data.

    :param tickers: list of the string abbreviation of the stocks to be
     analized (i.e. ['AAPL', 'MSFT']).
    :param year: string of the year to be analized (i.e '2016').
    :return: None -- The function saves the data in a file and does not return
     a value.
    """

    date_list = taq_data_tools_responses_activity.taq_bussiness_days(year)

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Basic functions
        pool.starmap(taq_data_analysis_responses_activity
                     .taq_trades_count_responses_activity_data,
                     product(tickers, date_list))

    # Especific functions
    # Self-response
    for ticker in tickers:

        taq_data_analysis_responses_activity \
            .taq_self_response_year_responses_activity_data(ticker, year)

    ticker_prod = iprod(tickers, tickers)

    # Cross-response
    for ticks in ticker_prod:

        taq_data_analysis_responses_activity \
            .taq_cross_response_year_responses_activity_data(ticks[0],
                                                             ticks[1], [year])

    # Parallel computing
    with mp.Pool(processes=mp.cpu_count()) as pool:

        # Plot
        pool.starmap(taq_data_plot_responses_activity
                     .taq_self_response_year_avg_plot,
                     product(tickers, [year]))
        pool.starmap(taq_data_plot_responses_activity
                     .taq_cross_response_year_avg_plot,
                     product(tickers, tickers, [year]))

    return None

# -----------------------------------------------------------------------------


def main():
    """The main function of the script.

    The main function extract, analyze and plot the data.

    :return: None.
    """

    # Tickers and days to analyze
    year, tickers = taq_data_tools_responses_activity.taq_initial_data()

    # Basic folders
    taq_data_tools_responses_activity.taq_start_folders(year)

    # Run analysis
    # Analysis and plot
    taq_data_plot_generator(tickers, year)

    print('Ay vamos!!')

    return None

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    main()