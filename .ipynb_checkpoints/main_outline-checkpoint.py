import streamlit as st
# import dask scheduler
# import dask cuda worker
import os
from pathlib import Path
import pandas as pd
from functools import reduce  # forward compatibility for Python 3
import operator

#################### general utility functions

def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

def del_by_path(root, items):
    """Delete a key-value in a nested object in root by item sequence."""
    del get_by_path(root, items[:-1])[items[-1]]


#################### make dirs and get strings

def get_app_abs_dir():
    return Path(app_abs_dir)

def get_configs_dir():
    configs_dir = get_app_abs_dir() / 'configs'
    return configs_dir

def make_configs_dir():
    configs_dir = get_configs_dir()
    Path(configs_dir) # create parents if not exists

def get_temp_dir():
    temp_dir = get_app_abs_dir() / 'tmp'
    return temp_dir

def make_temp_dir():
    temp_dir = get_temp_dir()
    Path(temp_dir) # create parents if not exists

def get_cluster_settings_dir():
    cluster_settings = get_app_abs_dir() / 'cluster_settings'
    return cluster_settings

def make_cluster_settings_dir():
    cluster_settings = get_cluster_settings_dir()
    Path(cluster_settings) # create parents if not exists
#################### startup functions

def run_startup_functions():
    make_configs_dir()
    make_temp_dir()
    make_cluster_settings_dir()

#################### scheduler and worker settings 
def get_start_configs_pathname():
    make_configs_dir()
    start_configs_pathname = get_configs_dir() / 'start_configs.yaml'
    return start_configs_pathname

def get_dask_cuda_worker_args():
    cli_command = 'dask-cuda-worker'

    raw_help = raw_help_output(cli_command)
    list_of_args = parse_raw_help_output(raw_help)
    """
    should be a list of dictionaries. dictionary should have the following keys:
    + 'arg'
    + 'type'
    + 'default'
    + 'description'
    if its just a flag then default should be none
    add validation
    """

    return list_of_args

def get_dask_scheduler_args():
    cli_command = 'dask-scheduler'

    raw_help = raw_help_output(cli_command)
    list_of_args = parse_raw_help_output(raw_help)
    """
    should be a list of dictionaries. dictionary should have the following keys:
    + 'arg'
    + 'type'
    + 'default'
    + 'description'
    if its just a flag then default should be none
    add validation
    """

    return list_of_args

def create_start_config_yamls(all_args_lists):
    start_configs_pathname
    pass

def create_default_start_config():
    all_args_lists = []
    all_args_lists.extend(list_of_args())
    all_args_lists.extendget_dask_scheduler_args()
    create_start_config_yamls(all_args_lists)

def check_if_start_config_exits():
    pass

def import_start_configs():
    start_config_exists = check_if_start_config_exits()
    if start_config_exists == False:
        create_default_config()
    start_configs = load(start_configs)
    return start_configs


def start_dask_cuda_cluster(start_configs):
    pass

def stop_dask_cuda_cluster():
    pass

def update_dask_cuda_defaults(start_configs):
    start_configs_pathname
    pass

"""
create class for AppSettings

"""

#################### scheduler and worker settings 

def get_cuda_device_csv_pathname():
    cuda_device_csv_pathname = get_temp_dir() / 'cuda_device.csv'
    return cuda_device_csv_pathname

@st.cache
def get_cuda_devices_df():
    cuda_device_csv_pathname = get_cuda_device_csv_pathname()
    cli_string = f"nvidia-smi --query-gpu=c1,c2 --format=csv > {cuda_device_csv_pathname}"
    os.system(cli_string)
    cuda_devices_df = pd.read_csv(cuda_device_csv_pathname, header=0, names=[''])
    """
    combine the two columns to make unique cols 
    """
    return cuda_devices_df



#################### main functions

def main(args):
    @st.cache #??
    run_startup_functions()

    selected_cuda_devices = st.select_cuda_devices()

    app_settings = AppSettings()
    app_settings.update_cuda_devices(selected_cuda_devices)

    """
    """

    if st.button("start dask cuda cluster"):
        start_dask_cuda_cluster(app_settings.start_configs)

    if st.button("stop dask cuda cluster"):
        stop_dask_cuda_cluster()

    if st.button("set current settings as default")
        update_dask_cuda_defaults(app_settings.start_configs)
        app_settings.reload_start_configs

    show_advanced_options = st.checkbox(False)

    if show_advanced_options:
        for cli_i, cur_cli in enumerate(app_settings.start_configs):
            for arg_val_i, cur_arg_vals in enumerate(cur_cli):
                cur_arg = cur_arg_vals['arg']
                cur_type = cur_arg_vals['type']
                cur_default = cur_arg_vals['default']
                cur_description = cur_arg_vals['description']

                


if __name__ == '__main__':
    main()