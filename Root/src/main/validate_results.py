# -*- coding: utf-8 -*-
# Helper scripts to validate the output by the individual implementations against the verified implementation
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pandas.util.testing import assert_frame_equal
import os
import mmap
from parse import parse
from utilities import RunningConstants
import argparse

def load_file_to_pandas(file_path: str) -> pd.DataFrame:
    """Module to load structured file data into pandas dataframe
    Parameters
    ----------
    file_path*: Support both relative, absolute references to the input file location.
    (* - Required parameters)

    Returns
    -------
    pandas dataframe
    """
    # Return exception should the file be inexistent
    if not os.path.exists(file_path):
        raise FileNotFoundError
    file_output = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            try:
                chunks = mmap_obj.read().decode('utf-8')+'\n'
                for chunk in chunks.split('\n'):
                    if len(chunk) > 0:
                        non_zero_parse = parse(
                            '{driver}: {distance} miles @ {speed} mph', chunk) \
                             or parse(
                             '{driver}: {distance} miles', chunk)
                        if not non_zero_parse:
                            raise SyntaxError("The format of the line processed is unexpected " + chunk)
                        non_zero_parse = non_zero_parse.named
                        if len(non_zero_parse) not in range(2, 4):
                            raise ValueError("The value of the line processed is unexpected " + chunk)
                        elif len(non_zero_parse) == 3:
                            driver_info = non_zero_parse['driver']
                            miles_info = non_zero_parse['distance']
                            speed = non_zero_parse['speed']
                            file_output[driver_info] = {'distance': miles_info, 'speed': speed}
                        else:
                            file_output[non_zero_parse['driver']] = {'distance': 0, 'speed': 0}
            except AttributeError as ae:
                raise AttributeError("Attribute Error encountered, possibly with : ", non_zero_parse)
            except IOError as ioe:
                raise IOError('I/O Error({0}): {1}'.format(ioe.errno, ioe.strerror))
            except Exception as ex:
                raise Exception("Error: ", ex)
    # Load the file into dataframe and return the dataframe
    return pd.DataFrame.from_dict(file_output, orient='index').reset_index().rename(columns={'index': 'driver'})

def prepareDf(df:pd.DataFrame) -> pd.DataFrame:
    """Helper module to sort the pandas dataframe

    The purpose of this module is to bring consistency in the compared dataframes, as
    two records with same miles driven may be written in different rows in the output file
    Parameters
    ----------
    df*: Pandas dataframe (with columns: distance, speed, driver)
    (* - Required parameters)

    Returns
    -------
    pandas dataframe
    """
    # Sort the dataframe by appropriate key
    return df.sort_values(by=['distance', 'speed', \
        'driver'], ascending=False).reset_index(drop=True)

def validate_results(table1: str, table2: str, tolerance:int = 0) -> dict:
    """Module to verify if the contents of two files are same or different
    within a given tolerance value.
    Parameters
    ----------
    table1*: Support both relative, absolute references to the file location
    table2*: Support both relative, absolute references to the file location
    tolerance: Supports mismatch upto a certain count (default: 0)
    (* - Required parameters)

    Returns
    -------
    dictionary:
        Tuple:
            0: status- boolean value (True if matched, False elsewise)
            1: mismatch count (if matched under tolerance) or
               entire mismatch (in case of a failed match)
    """
    # Load both the reference and baseline dataframes
    base_table = load_file_to_pandas(table1)
    reference_table = load_file_to_pandas(table2)
    base_table = prepareDf(base_table)
    reference_table = prepareDf(reference_table)
    if not tolerance:
        tolerance = RunningConstants.RESULTSET_TOLERANCE.value
    try:
        assert_frame_equal (base_table, reference_table, check_dtype=False, check_like=True)
        return {'status': (True, 0)}
    except AssertionError as ae:
        # Ignoring mismatch within a given tolerance
        mismatch = reference_table.compare(base_table).reset_index(drop=True)
        all_mismatched = 0
        for level in mismatch.columns.levels[0]:
            if level not in ['speed', 'distance']:
                continue
            compared = mismatch[level]
            compared['self'] = pd.to_numeric(compared['self'])
            compared['other'] = pd.to_numeric(compared['other'])
            compared = compared.query("abs(self-other) > 1")
            mismatched_count = compared.count()[0]
            if mismatched_count > tolerance:
                return {'status': (False, mismatch)}
            all_mismatched += mismatched_count
        return {'status': (True, all_mismatched)}
    return

if __name__ == '__main__':
    # Enabling command-line support to run this file directly from the terminal
    # with support for arguments (required, default)
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-t1",
            "--table1",
            help="First table file path (Relative/Absolute)",
            type=str
        )
    parser.add_argument(
            "-t2",
            "--table2",
            help="Second table file path (Relative/Absolute)",
            type=str
        )
    args = parser.parse_args()
    # Throwing error, should the required input arguments  be missing
    if not args.table1:
        parser.error("Missing *required --table1 argument")
    elif not args.table2:
        parser.error("Missing *required --table2 argument")

    flag, others = validate_results(args.table1, args.table2)['status']
    # Comprehending the comparison results as approprate
    if flag:
        if not others:
            print ("Successful. Additional Details: Both tables have matched completely")
        else:
            print ("Successful. Additional Details: Mismatch %d under tolerance" % others)
    else:
        print ("Comparison was unsuccessful. Detailed mismatch is as follows: \n", others)
