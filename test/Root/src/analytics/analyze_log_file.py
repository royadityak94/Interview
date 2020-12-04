# -*- coding: utf-8 -*-
# Code for graphing, log file
import pandas as pd
import os
import mmap
from parse import parse
from enum import Enum
import sys
from matplotlib import pyplot as plt

class Constants(Enum):
    """Controllable Hyperparameters
    """
    BASE_URL = '../main'

# Importing the required modules
sys.path.append(Constants.BASE_URL.value)
from utilities import RunningConstants

def get_file_information(file_path:str, strip_extras: bool = False) -> str:
    """Module to fetch file name or file type.

    Parameters
    ----------
    file_path*: Support both relative, absolute references to the input file location.
    strip_extras: Returns file source instead of file name (if set True), default: False
    (* - Required parameters)

    Returns
    -------
    base path as string
    """
    base_url_idx = file_path.rindex('/')+1
    file_name = file_path[base_url_idx:]
    # Return the file name (if that's what the module has been called for)
    if not strip_extras:
        return file_name
    # Return file type (if strip_extras flag is set to True)
    return file_name[17:file_name.rindex('_')]

def load_file_to_pandas(file_path: str) -> pd.DataFrame:
    """Module to manipuate, load file contents into a pandas dataframe

    Parameters
    ----------
    file_path*: Support both relative, absolute references to the input file location.
    (* - Required parameters)

    Returns
    -------
    Pandas dataframe
    """
    # Check if the input file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError
    file_output = {}
    # Pattern to parse from the output file
    pattern = 'Log Timed {ts}: Input File: {inp_path}, ' + \
            'Output File: {op_path}, Input Data Size: {ip_size}, Output Data' + \
            ' Size: {op_size} -> Time Taken: {time_spent}.'
    with open(file_path, mode='r', encoding='utf-8') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            try:
                chunks = mmap_obj.read().decode('utf-8')
                for chunk in chunks.split('\n'):
                    if len(chunk):
                        # Parsing parameters of interest
                        non_zero_parse = parse(pattern, chunk)
                        inp_file = get_file_information(non_zero_parse['inp_path'])
                        file_type = get_file_information(non_zero_parse['op_path'], True)
                        ip_size = non_zero_parse['ip_size']
                        op_size = non_zero_parse['op_size']
                        time_spent = non_zero_parse['time_spent']
                        key = inp_file + '_' + file_type
                        # Appending to the composite key = (inp_file, file_type)
                        file_output[key] = {'input_file': inp_file,
                            'implementation': file_type, 'input_size': ip_size,
                            'output_size': op_size, 'time_spent': time_spent }
            except KeyError as keye:
                raise KeyError("Missing key value in the parsed contents: ", non_zero_parse, chunk)
            except AttributeError as ae:
                raise AttributeError("Attribute Error encountered, possibly with : ", non_zero_parse)
            except IOError as ioe:
                raise IOError('I/O Error({0}): {1}'.format(ioe.errno, ioe.strerror))
            except Exception as ex:
                raise Exception("Error: ", ex)
    # Filter out columns of interest
    chosen_columns = list(file_output[key].keys())
    # Returning the dictionary as a pandas dataframe
    return pd.DataFrame.from_dict(file_output, orient='index').reset_index()[chosen_columns]

def save_plot_to_file(df:pd.DataFrame, file_path:str) -> None:
    """Module to manipulate, load requisite plots

    Parameters
    ----------
    df*: Pandas dataframe comprised of the data to be plotted
    file_path*: Support both relative, absolute references to the output file location
    (* - Required parameters)

    Returns
    -------
    None
    """
    ncols = 2
    # ideally nrows should be ceil(total_groups/2), however, we already know
    #that we have total of 4 implementations, thus, nrows = ceil(4/2) = 2 (reduced computational overhead)
    nrows = 2
    template = 'File: %s\n(Input Size: %s, Distinct Keys: %s)'
    # Extracting the grouping key as list
    unique_sets = df.input_file.unique().tolist()
    colors = ['red', 'blue', 'green', 'cyan']
    fig, axes = plt.subplots( figsize=(14, 10), nrows=nrows, ncols=ncols)
    for row in range(nrows):
        for col in range(ncols):
            inputs = unique_sets.pop(0)
            subdata = df.query("input_file=='%s'" % inputs)
            input_size = subdata.input_size.iloc[0]
            distinct_keys = subdata.output_size.iloc[0]
            title = template % (inputs, input_size, distinct_keys)
            # Subplot for implementation type as specidfied in inputs
            subdata.plot.bar(x='implementation', y='time_spent', color=colors,
                             title=title, ax=axes[row, col], legend=False)

    fig.suptitle("Time-Spent across different implementation by individual input sets\n \n")
    plt.tight_layout()
    plt.savefig(file_path)
    return

def analyze_log_file() -> None:
    """
        Analyzing the log file using pandas
    """
    # Extracting dynamically configured log file information to load as pandas dataframe
    log_file = os.path.join(RunningConstants.LOG_DIR.value, RunningConstants.LOG_FILE.value)
    df = load_file_to_pandas(log_file)
    # Specifying the numeric column for creating bar plot
    df['time_spent'] = pd.to_numeric(df['time_spent'])
    # Generating, saving the created plot in a file under resources directory (configurable in the utilities file)
    save_plot_to_file(df, RunningConstants.GRAPHING_FILE.value)
    return

if __name__ == '__main__':
    # Enabling command-line support to run this file directly from the terminal
    analyze_log_file()
