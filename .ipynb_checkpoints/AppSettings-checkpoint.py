from pathlib import Path
from utils.functions import *
from cli_options.dask_scheduler_options import *
from cli_options.dask_cuda_worker_options import *
from cli_options.dask_worker_options import *
import pickle 
import os
from copy import deepcopy

class AppSettings:
 
    # The init method or constructor
    def __init__(self,):
        run_startup_functions()
        make_cuda_devices_df_file()
        
        self.cuda_devices_df = get_cuda_devices_df()
        self.selected_cuda_devices = self.cuda_devices_df['id'].tolist()
        
        self.dask_scheduler_options = deepcopy(dask_scheduler_options)
        self.dask_scheduler_options_selected = deepcopy(dask_scheduler_options)

        self.dask_cuda_worker_options = deepcopy(dask_cuda_worker_options)
        self.dask_cuda_worker_options_selected = deepcopy(dask_cuda_worker_options)

        self.dask_worker_options = deepcopy(dask_worker_options)
        self.dask_worker_options_selected = deepcopy(dask_worker_options)
        
        self.cuda_env_vars = load_default_cuda_env_vars_file()
        self.cuda_env_vars['CUDA_VISIBLE_DEVICES'] = {'val': get_all_cuda_device_ids(),
                                                      'used': False,
                                                      'names': deepcopy(self.cuda_devices_df['device'].tolist()),
                                                     }
        self.cuda_env_vars_selected = load_default_cuda_env_vars_file()
        self.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES'] = {'val': get_all_cuda_device_ids(),
                                                      'used': False,
                                                      'names': deepcopy(self.cuda_devices_df['device'].tolist()),
                                                     }

        
    def reload_cuda_device_df(self):
        make_cuda_devices_df_file()
        self.cuda_devices_df = get_cuda_devices_df()
        self.selected_cuda_devices = self.cuda_devices_df['id'].tolist()
    
    #### scheduler settings
    def load_default_scheduler_settings(self):
        self.dask_scheduler_options = deepcopy(dask_scheduler_options)
        self.dask_scheduler_options_selected = deepcopy(dask_scheduler_options)
        
    def save_scheduler_settings(self, filename):
        filepath = get_settings_dir() / 'scheduler'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        filepath = filepath / f"{filename}.pkl"
        filehandler = open(filepath, 'wb') 
        pickle.dump(self.dask_scheduler_options_selected, filehandler)
        
    def load_scheduler_settings(self, filename):
        filepath = get_settings_dir() / 'scheduler' / f"{filename}.pkl"
        filehandler = open(filepath, 'rb') 
        self.dask_scheduler_options = pickle.load(filehandler)
        filehandler = open(filepath, 'rb') 
        self.dask_scheduler_options_selected = pickle.load(filehandler)
        
    def list_scheduler_settings_files(self):
        filepath = get_settings_dir() / 'scheduler'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        files = os.listdir(filepath)
        files = [x for x in files if '.pkl' in x]
        files = [x.split('.')[0] for x in files]
        return files
    
    def delete_saved_scheduler_settings_file(self, filename):
        filepath = get_settings_dir() / 'scheduler' / f"{filename}.pkl"
        os.remove(filepath)
        
    #### cuda worker settings (GPU)
    def load_default_cuda_worker_settings(self):
        self.dask_cuda_worker_options = deepcopy(dask_cuda_worker_options)
        self.dask_cuda_worker_options_selected = deepcopy(dask_cuda_worker_options)
        
    def save_cuda_worker_settings(self, filename):
        filepath = get_settings_dir() / 'cuda_worker'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        filepath = filepath / f"{filename}.pkl"
        filehandler = open(filepath, 'wb') 
        pickle.dump(self.dask_cuda_worker_options_selected, filehandler)
        
    def load_cuda_worker_settings(self, filename):
        filepath = get_settings_dir() / 'cuda_worker' / f"{filename}.pkl"
        filehandler = open(filepath, 'rb') 
        self.dask_cuda_worker_options = pickle.load(filehandler)
        filehandler = open(filepath, 'rb') 
        self.dask_cuda_worker_options_selected = pickle.load(filehandler)
        
    def list_cuda_worker_settings_files(self):
        filepath = get_settings_dir() / 'cuda_worker'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        files = os.listdir(filepath)
        files = [x for x in files if '.pkl' in x]
        files = [x.split('.')[0] for x in files]
        return files
    
    def delete_saved_cuda_worker_settings_file(self, filename):
        filepath = get_settings_dir() / 'cuda_worker' / f"{filename}.pkl"
        os.remove(filepath)
        
    #### worker settings (CPU)
    def load_default_worker_settings(self):
        self.dask_worker_options = deepcopy(dask_worker_options)
        self.dask_worker_options_selected = deepcopy(dask_worker_options)
        
    def save_worker_settings(self, filename):
        filepath = get_settings_dir() / 'worker'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        filepath = filepath / f"{filename}.pkl"
        filehandler = open(filepath, 'wb') 
        pickle.dump(self.dask_worker_options_selected, filehandler)
        
    def load_worker_settings(self, filename):
        filepath = get_settings_dir() / 'worker' / f"{filename}.pkl"
        filehandler = open(filepath, 'rb') 
        self.dask_worker_options = pickle.load(filehandler)
        filehandler = open(filepath, 'rb') 
        self.dask_worker_options_selected = pickle.load(filehandler)
        
    def list_worker_settings_files(self):
        filepath = get_settings_dir() / 'worker'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        files = os.listdir(filepath)
        files = [x for x in files if '.pkl' in x]
        files = [x.split('.')[0] for x in files]
        return files
    
    def delete_saved_worker_settings_file(self, filename):
        filepath = get_settings_dir() / 'worker' / f"{filename}.pkl"
        os.remove(filepath)
        
    #### cuda environment settings
    def load_default_cuda_env_vars_settings(self):
        self.reload_cuda_device_df()
        self.cuda_env_vars = load_default_cuda_env_vars_file()
        self.cuda_env_vars['CUDA_VISIBLE_DEVICES'] = {'val': get_all_cuda_device_ids(),
                                                      'used': False,
                                                      'names': deepcopy(self.cuda_devices_df['device'].tolist()),
                                                     }
        self.cuda_env_vars_selected = load_default_cuda_env_vars_file()
        self.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES'] = {'val': get_all_cuda_device_ids(),
                                                      'used': False,
                                                      'names': deepcopy(self.cuda_devices_df['device'].tolist()),
                                                     }
        
    def save_cuda_env_vars_settings(self, filename):
        filepath = get_settings_dir() / 'env'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        filepath = filepath / f"{filename}.pkl"
        filehandler = open(filepath, 'wb') 
        pickle.dump(self.cuda_env_vars_selected, filehandler)
        
    def load_cuda_env_vars_settings(self, filename):
        filepath = get_settings_dir() / 'env' / f"{filename}.pkl"
        filehandler = open(filepath, 'rb') 
        self.cuda_env_vars = pickle.load(filehandler)
        filehandler = open(filepath, 'rb') 
        self.cuda_env_vars_selected = pickle.load(filehandler)
        
    def list_cuda_env_vars_settings_files(self):
        filepath = get_settings_dir() / 'env'
        Path(filepath).mkdir(parents=True, exist_ok=True)
        files = os.listdir(filepath)
        files = [x for x in files if '.pkl' in x]
        files = [x.split('.')[0] for x in files]
        return files
    
    def delete_saved_cuda_env_vars_settings_file(self, filename):
        filepath = get_settings_dir() / 'env' / f"{filename}.pkl"
        os.remove(filepath)
        
    def update_selected_cuda_device_ids(self):
        selected_names = self.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['names']
        selected_device_ids = self.cuda_devices_df.set_index('device').loc[selected_names]['id'].tolist()
        selected_device_ids = ','.join(selected_device_ids).replace(' ', '')
        self.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['val'] = selected_device_ids
        
    def update_selected_cuda_device_names(self, selected_device_names):
        self.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['names'] = selected_device_names
