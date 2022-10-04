import os
from pathlib import Path
import pandas as pd
from functools import reduce  # forward compatibility for Python 3
import operator
import streamlit as st
import pickle
import time

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
    app_abs_dir = Path().resolve()
    return app_abs_dir

def get_configs_dir():
    configs_dir = get_app_abs_dir() / 'configs'
    return configs_dir

def make_configs_dir():
    configs_dir = get_configs_dir()
    Path(configs_dir).mkdir(parents=True, exist_ok=True) # create parents if not exists

def get_settings_dir():
    settings_dir = get_app_abs_dir() / 'settings'
    return settings_dir

def make_settings_dir():
    settings_dir = get_settings_dir()
    Path(settings_dir).mkdir(parents=True, exist_ok=True) # create parents if not exists
    
def get_temp_dir():
    temp_dir = get_app_abs_dir() / 'tmp'
    return temp_dir

def make_temp_dir():
    temp_dir = get_temp_dir()
    Path(temp_dir).mkdir(parents=True, exist_ok=True) # create parents if not exists

def get_cluster_settings_dir():
    cluster_settings = get_app_abs_dir() / 'cluster_settings'
    return cluster_settings

def make_cluster_settings_dir():
    cluster_settings = get_cluster_settings_dir()
    Path(cluster_settings).mkdir(parents=True, exist_ok=True) # create parents if not exists

############### cuda environment variables
def default_cuda_env_vars():
    env_vars = ['CUDA_DEVICE_ORDER', 'RAPIDS_NO_INITIALIZE', 'DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT', 'DASK_JIT_UNSPILL_COMPATIBILITY_MODE', 'UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES']
    vars_vals = ['PCI_BUS_ID', '1', 'True', 'True', 'cuda']
    used_by_default = [False, True, True, False, False]
    # default_env_vars = []
    default_env_vars = {}
    for var, val, used in zip(env_vars, vars_vals, used_by_default):
        # default_env_vars.append(
        #     {'env_var': var,
        #      'var_val': val,
        #      'used': used,
        #     }
        # )
        default_env_vars[var] = {'val': val,
                                 'used': used,
                                }
    return default_env_vars

def make_default_cuda_env_vars_file():
    default_env_vars = default_cuda_env_vars()
    filepath = get_app_abs_dir() / 'cli_options' / 'default_env_vars.pkl'
    filehandler = open(filepath, 'wb') 
    pickle.dump(default_env_vars, filehandler)

#################### startup functions

def run_startup_functions():
    make_configs_dir()
    make_settings_dir()
    make_temp_dir()
    make_cluster_settings_dir()
    make_default_cuda_env_vars_file()

#################### cuda devices

def get_cuda_device_csv_pathname():
    cuda_device_csv_pathname = get_temp_dir() / 'cuda_device.csv'
    return cuda_device_csv_pathname

def make_cuda_devices_df_file():
    cuda_device_csv_pathname = get_cuda_device_csv_pathname()
    cli_string = f"nvidia-smi --query-gpu=gpu_name,pci.sub_device_id,index --format=csv > {cuda_device_csv_pathname}"
    os.system(cli_string)

def get_cuda_devices_df():
    """
    combine the two columns to make unique cols 
    """
    cuda_device_csv_pathname = get_cuda_device_csv_pathname()
    cuda_devices_df = pd.read_csv(cuda_device_csv_pathname, header=0, names=['name', 'pci_id', 'id'], dtype=str)
    cuda_devices_df['device'] = cuda_devices_df['name'] + ' | ' + cuda_devices_df['pci_id']
    
    return cuda_devices_df[['device', 'id']]

def get_all_cuda_device_ids():
    cuda_devices_df = get_cuda_devices_df()
    cuda_device_ids = cuda_devices_df['id'].tolist()
    cuda_device_ids = ','.join(cuda_device_ids).replace(' ', '')
    return cuda_device_ids

#################### streamlit object creation
def get_st_inp_obj(cur, cli_type):
    cur_type = cur['type']
    cur_arg = cur['arg']
    cur_options = cur['options']
    cur_default = cur['default']
    cur_desc = cur['description']

    if cur_type == str:
        if cur_default != None:
            cur_selection = st.text_input(
                label=cur_arg,
                value=cur_default,
                help=cur_desc,
                key=cur_arg + f"_{cli_type}",
            )
        else:
            cur_selection = st.text_input(
                label=cur_arg,
                placeholder=cur_default,
                help=cur_desc,
                key=cur_arg + f"_{cli_type}",
            )

    if cur_type == int:
        if cur_default != None:
            cur_selection = st.text_input(
                label=cur_arg,
                value=cur_default,
                help=cur_desc,
                key=cur_arg + f"_{cli_type}",
            )
        else:
            cur_selection = st.text_input(
                label=cur_arg,
                placeholder=cur_default,
                help=cur_desc,
                key=cur_arg + f"_{cli_type}",
            )

    if cur_type == bool:
        if cur_default != None:
            cur_selection = st.checkbox(
                    label=cur_arg,
                    value=cur_default,
                    help=cur_desc,
                    key=cur_arg + f"_{cli_type}",
                )
        else:
            cur_selection = st.checkbox(
                    label=cur_arg,
                    help=cur_desc,
                    key=cur_arg + f"_{cli_type}",
                )

    if cur_type == 'binary':
        if cur_default != None:
            cur_selection = st.radio(
                    label='/'.join(cur_arg),
                    options=cur_arg,
                    index=cur_arg.index(cur_default),
                    help=cur_desc,
                    key='/'.join(cur_arg) + f"_{cli_type}",
                )
        else:
            cur_selection = st.radio(
                    label='/'.join(cur_arg),
                    options=cur_arg,
                    help=cur_desc,
                    key='/'.join(cur_arg) + f"_{cli_type}",
                )

    if cur_type == 'single-select':
        if cur_default != None:
            cur_selection = st.selectbox(
                    label=cur_arg,
                    options=cur_options,
                    value=cur_options.index(cur_default),
                    help=cur_desc,
                    key=cur_arg + f"_{cli_type}",
                )
        else:
            cur_selection = st.selectbox(
                    label=cur_arg,
                    options=cur_options,
                    help=cur_desc,
                    key=cur_arg + f"_{cli_type}",
                )

    return cur_selection


    
def load_default_cuda_env_vars_file():
    filepath = get_app_abs_dir() / 'cli_options' / 'default_env_vars.pkl'
    filehandler = open(filepath, 'rb') 
    default_env_vars = pickle.load(filehandler)
    return default_env_vars


##### starting cluster
def start_scheduler(scheduler_cli_command):
    cmd_to_run = scheduler_cli_command + ' &'
    os.system(cmd_to_run)
    time.sleep(5)

def start_worker(worker_cli_command, env_cli_command=None):
    if env_cli_command == None:

        cmd_to_run = worker_cli_command + ' &'
    else:
        cmd_to_run = env_cli_command + ' ' + worker_cli_command + ' &'
    os.system(cmd_to_run)
    time.sleep(5)

def start_a_cluster(scheduler_cli_command, worker_cli_command, env_cli_command=None):
    start_scheduler(scheduler_cli_command)
    start_worker(worker_cli_command, env_cli_command)

##### stopping cluster
def stop_a_cluster(scheduler_pathname):
    from dask.distributed import Client
    client = Client(scheduler_file=scheduler_pathname)
    client.shutdown()
    client.close()
    del client