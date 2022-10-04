import streamlit as st
from AppSettings import AppSettings
from scripts.functions import get_st_inp_obj, start_a_cluster, get_by_path, stop_a_cluster
import pandas as pd
from pathlib import Path

def main():

    @st.cache(allow_output_mutation=True)
    def load_app_settings():
        app_settings = AppSettings()
        return app_settings
    app_settings = load_app_settings()

    # app_settings = AppSettings()

    with st.expander("Settings"):

        st.write("## Scheduler options")

        st.write("#### load scheduler settings")

        do_load_saved_scheduler_settings = st.checkbox(
            label='load saved scheduler settings?',
            value=False,
            key='do_load_saved_scheduler_settings',
            )

        if do_load_saved_scheduler_settings:
            scheduler_settings_files = app_settings.list_scheduler_settings_files()
            if len(scheduler_settings_files) > 0:
                selected_scheduler_settings_file = st.selectbox(
                    label='select scheduler file',
                    options=scheduler_settings_files,
                    key='selected_scheduler_settings_file',
                    )

                load_scheduler_settings = st.button(
                    label='load saved scheduler settings',
                    key='load_scheduler_settings')

                if load_scheduler_settings:
                    app_settings.load_scheduler_settings(selected_scheduler_settings_file)
                    st.empty()
            else:
                st.write("no saved scheduler settings file(s)")

        do_load_default_scheduler_settings = st.checkbox(
            label='load default scheduler settings?',
            value=False,
            key='do_load_default_scheduler_settings',
            )

        if do_load_default_scheduler_settings:

                load_default_scheduler_settings = st.button(
                    label='load default scheduler settings',
                    key='load_default_scheduler_settings',
                    )
                if load_default_scheduler_settings:
                    app_settings.load_default_scheduler_settings()
                    st.empty()

        show_advanced_scheduler_options = st.checkbox(
            label='Show advanced scheduler options',
            value=False,
            key='show_advanced_scheduler_options',
            )

        if show_advanced_scheduler_options:

            st.write("#### scheduler options")
            for i, cur in enumerate(app_settings.dask_scheduler_options_selected):
                cur_type = cur['type']
                #print(cur_type)
                cur_arg = cur['arg']
                cur_options = cur['options']
                cur_default = cur['default']
                cur_desc = cur['description']

                if type(cur_arg) == list:
                    cur_label = 'toggle ' + '"' + '/'.join(cur_arg) + '"' + ' scheduler option'
                else:
                    cur_label = 'toggle ' + '"' + cur_arg + '"' + ' scheduler option'

                if cur_default == None:
                    cur_display = st.checkbox(
                        label=cur_label,
                        value=False,
                        key=cur_label,
                        )
                else:
                    cur_display = st.checkbox(
                        label=cur_label,
                        value=True,
                        key=cur_label,
                        )

                if cur_display: 

                    cur_selection = get_st_inp_obj(cur, 'scheduler')

                    app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

                else:
                    app_settings.dask_scheduler_options_selected[i]['default'] = None

            st.write("#### Save/delete scheduler settings")
            do_save_scheduler_settings = st.checkbox(
                label='save current scheduler settings?',
                value=False,
                key='do_save_scheduler_settings')

            if do_save_scheduler_settings:
                scheduler_save_filename = st.text_input(
                    label='enter a name for your scheduler settings',
                    key='new_scheduler_save_filename',
                    )
                if len(scheduler_save_filename) > 0:
                    save_scheduler_settings = st.button(
                        label='save scheduler settings',
                        key='save_scheduler_settings',
                        )
                    if save_scheduler_settings:
                        app_settings.save_scheduler_settings(scheduler_save_filename)
                else:
                    st.write('scheduler settings filename cannot be blank')

            do_delete_saved_scheduler_settings_file = st.checkbox(
                label='delete saved scheduler settings file?',
                value=False,
                key='do_delete_saved_scheduler_settings_file')

            if do_delete_saved_scheduler_settings_file:
                scheduler_settings_files = app_settings.list_scheduler_settings_files()
                scheduler_settings_files_no_ext = [x.split('.')[0] for x in scheduler_settings_files]

                if len(scheduler_settings_files_no_ext) > 0:
                    delete_saved_scheduler_filename = st.selectbox(
                            label='select scheduler file',
                            options=scheduler_settings_files,
                            key='delete_saved_scheduler_filename',
                            )
                    delete_saved_scheduler_settings_file = st.button(
                        label='delete saved scheduler settings file',
                        key='delete_saved_scheduler_settings_file',
                        )

                    if delete_saved_scheduler_settings_file:
                        app_settings.delete_saved_scheduler_settings_file(delete_saved_scheduler_filename)
                        st.empty()
                else:
                    st.write("no saved scheduler settings file(s)")
                    st.empty()



        scheduler_cli_command = 'dask-scheduler'
        for cur in app_settings.dask_scheduler_options_selected:
            cur_type = cur['type']
            cur_arg = cur['arg']
            cur_options = cur['options']
            cur_default = cur['default']
            cur_desc = cur['description']

            if cur_default != None:
                if cur_type == 'binary':
                    scheduler_cli_command += f" --{cur_default}"
                else:
                    scheduler_cli_command += f" --{cur_arg}={cur_default}"

        st.write("#### scheduler CLI command")
        st.write(f"```{scheduler_cli_command}```")
        st.code(scheduler_cli_command, language='bash')


        st.write('### Select worker type')
        worker_type = st.selectbox(
            label='worker type',
            options=['GPU', 'CPU'],
            index=0,
            )

        if worker_type == 'GPU':
            st.write("## Cuda worker options")

            st.write("#### load cuda_worker settings")

            do_load_saved_cuda_worker_settings = st.checkbox(
                label='load saved cuda_worker settings?',
                value=False,
                key='do_load_saved_cuda_worker_settings',
                )

            if do_load_saved_cuda_worker_settings:
                cuda_worker_settings_files = app_settings.list_cuda_worker_settings_files()
                if len(cuda_worker_settings_files) > 0:
                    selected_cuda_worker_settings_file = st.selectbox(
                        label='select cuda_worker file',
                        options=cuda_worker_settings_files,
                        key='selected_cuda_worker_settings_file',
                        )

                    load_cuda_worker_settings = st.button(
                        label='load saved cuda_worker settings',
                        key='load_cuda_worker_settings')

                    if load_cuda_worker_settings:
                        app_settings.load_cuda_worker_settings(selected_cuda_worker_settings_file)
                else:
                    st.write("no saved cuda_worker settings file(s)")

            do_load_default_cuda_worker_settings = st.checkbox(
                label='load default cuda_worker settings?',
                value=False,
                key='do_load_default_cuda_worker_settings',
                )

            if do_load_default_cuda_worker_settings:

                load_default_cuda_worker_settings = st.button(
                    label='load default cuda_worker settings',
                    key='load_default_cuda_worker_settings',
                    )
                if load_default_cuda_worker_settings:
                    app_settings.load_default_cuda_worker_settings()
                    st.empty()

            show_advanced_cuda_worker_options = st.checkbox(
                label='Show advanced cuda_worker options',
                value=False,
                key='show_advanced_cuda_worker_options',
                )

            if show_advanced_cuda_worker_options:

                st.write("#### cuda_worker options")
                for i, cur in enumerate(app_settings.dask_cuda_worker_options_selected):
                    cur_type = cur['type']
                    cur_arg = cur['arg']
                    cur_options = cur['options']
                    cur_default = cur['default']
                    cur_desc = cur['description']

                    if type(cur_arg) == list:
                        cur_label = 'toggle ' + '"' + '/'.join(cur_arg) + '"' + ' cuda_worker option'
                    else:
                        cur_label = 'toggle ' + '"' + cur_arg + '"' + ' cuda_worker option'

                    if cur_default == None:
                        cur_display = st.checkbox(
                            label=cur_label,
                            value=False,
                            key=cur_label,
                            )
                    else:
                        cur_display = st.checkbox(
                            label=cur_label,
                            value=True,
                            key=cur_label,
                            )

                    if cur_display: 

                        cur_selection = get_st_inp_obj(cur, 'cuda_worker')

                        app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection
                    else:
                        app_settings.dask_cuda_worker_options_selected[i]['default'] = None

                st.write("#### Save/delete cuda_worker settings")
                do_save_cuda_worker_settings = st.checkbox(
                    label='save current cuda_worker settings?',
                    value=False,
                    key='do_save_cuda_worker_settings')

                if do_save_cuda_worker_settings:
                    cuda_worker_save_filename = st.text_input(
                        label='enter a name for your cuda_worker settings',
                        key='new_cuda_worker_save_filename',
                        )
                    if len(cuda_worker_save_filename) > 0:
                        save_cuda_worker_settings = st.button(
                            label='save cuda_worker settings',
                            key='save_cuda_worker_settings',
                            )
                        if save_cuda_worker_settings:
                            app_settings.save_cuda_worker_settings(cuda_worker_save_filename)
                    else:
                        st.write('cuda_worker settings filename cannot be blank')

                do_delete_saved_cuda_worker_settings_file = st.checkbox(
                    label='delete saved cuda_worker settings file?',
                    value=False,
                    key='do_delete_saved_cuda_worker_settings_file')

                if do_delete_saved_cuda_worker_settings_file:
                    cuda_worker_settings_files = app_settings.list_cuda_worker_settings_files()
                    cuda_worker_settings_files_no_ext = [x.split('.')[0] for x in cuda_worker_settings_files]

                    if len(cuda_worker_settings_files_no_ext) > 0:
                        delete_saved_cuda_worker_filename = st.selectbox(
                                label='select cuda_worker file',
                                options=cuda_worker_settings_files,
                                key='delete_saved_cuda_worker_filename',
                                )
                        delete_saved_cuda_worker_settings_file = st.button(
                            label='delete saved cuda_worker settings file',
                            key='delete_saved_cuda_worker_settings_file',
                            )

                        if delete_saved_cuda_worker_settings_file:
                            app_settings.delete_saved_cuda_worker_settings_file(delete_saved_cuda_worker_filename)
                            st.empty()
                    else:
                        st.write("no saved cuda_worker settings file(s)")
                        st.empty()

            cuda_worker_cli_command = 'dask-cuda-worker'
            for cur in app_settings.dask_cuda_worker_options_selected:
                cur_type = cur['type']
                cur_arg = cur['arg']
                cur_options = cur['options']
                cur_default = cur['default']
                cur_desc = cur['description']

                if cur_default != None:
                    if cur_type == 'binary':
                        cuda_worker_cli_command += f" --{cur_default}"
                    else:
                        cuda_worker_cli_command += f" --{cur_arg}={cur_default}"

            st.write("#### cuda_worker CLI command")
            st.write(f"```{cuda_worker_cli_command}```")
            st.code(cuda_worker_cli_command)

            st.write("#### cuda environment variables")

            st.write("##### load cuda environment variables settings")

            do_load_saved_cuda_env_vars_settings = st.checkbox(
                label='load saved cuda_env_vars settings?',
                value=False,
                key='do_load_saved_cuda_env_vars_settings',
                )

            if do_load_saved_cuda_env_vars_settings:
                cuda_env_vars_settings_files = app_settings.list_cuda_env_vars_settings_files()
                if len(cuda_env_vars_settings_files) > 0:
                    selected_cuda_env_vars_settings_file = st.selectbox(
                        label='select cuda_env_vars file',
                        options=cuda_env_vars_settings_files,
                        key='selected_cuda_env_vars_settings_file',
                        )

                    load_cuda_env_vars_settings = st.button(
                        label='load saved cuda_env_vars settings',
                        key='load_cuda_env_vars_settings')

                    if load_cuda_env_vars_settings:
                        app_settings.load_cuda_env_vars_settings(selected_cuda_env_vars_settings_file)
                        st.empty()
                else:
                    st.write("no saved cuda_env_vars settings file(s)")

            do_load_default_cuda_env_vars_settings = st.checkbox(
                label='load default cuda_env_vars settings?',
                value=False,
                key='do_load_default_cuda_env_vars_settings',
                )

            if do_load_default_cuda_env_vars_settings:

                load_default_cuda_env_vars_settings = st.button(
                    label='load default cuda_env_vars settings',
                    key='load_default_cuda_env_vars_settings',
                    )
                if load_default_cuda_env_vars_settings:
                    app_settings.load_default_cuda_env_vars_settings()
                    # st.empty()

            st.write("**cuda visible devices**")

            do_select_cuda_devices = st.checkbox(
                label="select specific cuda devices (otherwise will use all available)?",
                value=app_settings.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['used'],
                )
            app_settings.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['used'] = do_select_cuda_devices

            if do_select_cuda_devices:
                selected_cuda_devices = st.multiselect(
                    label='select cuda devices (GPUs)',
                    options=app_settings.cuda_devices_df['device'].tolist(),
                    default=app_settings.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['names'],
                    key='selected_cuda_devices',
                    )

                app_settings.update_selected_cuda_device_names(selected_cuda_devices)
                app_settings.update_selected_cuda_device_ids()
                app_settings.cuda_env_vars_selected['CUDA_DEVICE_ORDER']['used'] = True

            else:
                app_settings.cuda_env_vars_selected['CUDA_VISIBLE_DEVICES']['used'] = False
                app_settings.cuda_env_vars_selected['CUDA_DEVICE_ORDER']['used'] = False

            if do_select_cuda_devices:
                st.write("**cuda device order**")
                selected_cuda_device_order = st.selectbox(
                    label="select cuda device order",
                    options=['PCI_BUS_ID'],
                    index=0,
                    help="This variable cannot be changed. It ensures that Dask uses the cuda devices that you specified.",
                    disabled=True,
                    )
                app_settings.cuda_env_vars_selected['CUDA_DEVICE_ORDER']['val'] = selected_cuda_device_order
                    
            show_cuda_env_options = st.checkbox(
                label='Show cuda environment options',
                value=False,
                key='show_cuda_env_options',
                )

            if show_cuda_env_options:
                
                st.write("**Delay RAPIDS cuda context creation**")
                do_rapids_no_intialization = st.checkbox(
                    label='set RAPIDS_NO_INITIALIZE?',
                    value=app_settings.cuda_env_vars_selected['RAPIDS_NO_INITIALIZE']['used'],
                    help="Dask-CUDA must create worker CUDA contexts during cluster initialization, and properly ordering that task is critical for correct UCX configuration. If a CUDA context already exists for this process at the time of cluster initialization, unexpected behavior can occur. To avoid this, it is advised to initialize any UCX-enabled clusters before doing operations that would result in a CUDA context being created.",
                    key='do_rapids_no_intialization',
                    )
                app_settings.cuda_env_vars_selected['RAPIDS_NO_INITIALIZE']['used'] = do_rapids_no_intialization
                if do_rapids_no_intialization:
                    selected_rapids_no_intialization = st.selectbox(
                        label='RAPIDS_NO_INITIALIZE',
                        options=["1"],
                        index=0,
                        help="For some RAPIDS libraries (e.g. cuDF), setting RAPIDS_NO_INITIALIZE=1 at runtime will delay or disable their CUDA context creation, allowing for improved compatibility with UCX-enabled clusters and preventing runtime warnings.",
                        key='selected_rapids_no_intialization')
                    app_settings.cuda_env_vars_selected['RAPIDS_NO_INITIALIZE']['val'] = selected_rapids_no_intialization

                st.write("**create cuda context**")
                do_create_cuda_context = st.checkbox(
                    label='create cuda context before UCX?',
                    value=app_settings.cuda_env_vars_selected['DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT']['used'],
                    help="For automatic UCX configuration, we must ensure a CUDA context is created on the scheduler before UCX is initialized. This can be satisfied by specifying the DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT=True environment variable when creating the scheduler.",
                    key='do_create_cuda_context',
                    )
                app_settings.cuda_env_vars_selected['DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT']['used'] = do_create_cuda_context
                if do_create_cuda_context:
                    selected_create_cuda_context = st.selectbox(
                        label='DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT',
                        options=["True"],
                        index=0,
                        key='selected_create_cuda_context')
                    app_settings.cuda_env_vars_selected['DASK_DISTRIBUTED__COMM__UCX__CREATE_CUDA_CONTEXT']['val'] = selected_create_cuda_context

                st.write("**JIT unspill compatibility mode**")
                do_jit_compatability = st.checkbox(
                    label='set JIT unspill to compatibility mode?',
                    value=app_settings.cuda_env_vars_selected['DASK_JIT_UNSPILL_COMPATIBILITY_MODE']['used'],
                    help="JIT-Unspill wraps CUDA objects, such as cudf.Dataframe, in a ProxyObject. Objects proxied by an instance of ProxyObject will be JIT-deserialized when accessed. The instance behaves as the proxied object and can be accessed/used just like the proxied object. ProxyObject has some limitations and doesn’t mimic the proxied object perfectly. Most noticeable, type checking using instance() works as expected but direct type checking doesn’t:",
                    key='do_jit_compatability',
                    )
                app_settings.cuda_env_vars_selected['DASK_JIT_UNSPILL_COMPATIBILITY_MODE']['used'] = do_jit_compatability
                if do_jit_compatability:
                    selected_jit_compatability = st.selectbox(
                        label='DASK_JIT_UNSPILL_COMPATIBILITY_MODE',
                        options=["True"],
                        index=0,
                        help="Thus, if encountering problems remember that it is always possible to use unproxy() to access the proxied object directly, or set DASK_JIT_UNSPILL_COMPATIBILITY_MODE=True to enable compatibility mode, which automatically calls unproxy() on all function inputs.",
                        key='selected_jit_compatability',
                        )
                    app_settings.cuda_env_vars_selected['DASK_JIT_UNSPILL_COMPATIBILITY_MODE']['val'] = selected_jit_compatability

                st.write("**UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES**")
                do_mem_alloc_type = st.checkbox(
                    label='set UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES?',
                    value=app_settings.cuda_env_vars_selected['UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES']['used'],
                    help="By defining UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES=cuda (default in UCX >= 1.12.0), UCX enables registration cache based on a buffer’s base address, thus preventing multiple time-consuming registrations for the same buffer. This is particularly useful when using a CUDA memory pool, thus requiring a single registration between two ends for the entire pool, providing considerable performance gains, especially when using InfiniBand.",
                    key='do_mem_alloc_type',
                    )
                app_settings.cuda_env_vars_selected['UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES']['used'] = do_mem_alloc_type
                if do_mem_alloc_type:
                    selected_mem_alloc_type = st.selectbox(
                        label='UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES',
                        options=["cuda"],
                        index=0,
                        key='selected_mem_alloc_type',
                        )
                    app_settings.cuda_env_vars_selected['UCX_MEMTYPE_REG_WHOLE_ALLOC_TYPES']['val'] = selected_mem_alloc_type

                st.write("##### Save/delete cuda environment variables settings")
                do_save_cuda_env_vars_settings = st.checkbox(
                    label='save current cuda_env_vars settings?',
                    value=False,
                    key='do_save_cuda_env_vars_settings')

                if do_save_cuda_env_vars_settings:
                    cuda_env_vars_save_filename = st.text_input(
                        label='enter a name for your cuda_env_vars settings',
                        key='new_cuda_env_vars_save_filename',
                        )
                    if len(cuda_env_vars_save_filename) > 0:
                        save_cuda_env_vars_settings = st.button(
                            label='save cuda_env_vars settings',
                            key='save_cuda_env_vars_settings',
                            )
                        if save_cuda_env_vars_settings:
                            app_settings.save_cuda_env_vars_settings(cuda_env_vars_save_filename)
                            do_save_cuda_env_vars_settings = False
                    else:
                        st.write('cuda_env_vars settings filename cannot be blank')

                do_delete_saved_cuda_env_vars_settings_file = st.checkbox(
                    label='delete saved cuda_env_vars settings file?',
                    value=False,
                    key='do_delete_saved_cuda_env_vars_settings_file')

                if do_delete_saved_cuda_env_vars_settings_file:
                    cuda_env_vars_settings_files = app_settings.list_cuda_env_vars_settings_files()
                    cuda_env_vars_settings_files_no_ext = [x.split('.')[0] for x in cuda_env_vars_settings_files]

                    if len(cuda_env_vars_settings_files_no_ext) > 0:
                        delete_saved_cuda_env_vars_filename = st.selectbox(
                                label='select cuda_env_vars file',
                                options=cuda_env_vars_settings_files,
                                key='delete_saved_cuda_env_vars_filename',
                                )
                        delete_saved_cuda_env_vars_settings_file = st.button(
                            label='delete saved cuda_env_vars settings file',
                            key='delete_saved_cuda_env_vars_settings_file',
                            )

                        if delete_saved_cuda_env_vars_settings_file:
                            app_settings.delete_saved_cuda_env_vars_settings_file(delete_saved_cuda_env_vars_filename)
                            st.empty()
                    else:
                        st.write("no saved cuda_env_vars settings file(s)")
                        st.empty()

            env_cli_command = ''
            for (key, val) in app_settings.cuda_env_vars_selected.items():
                if val['used'] == True:
                    env_cli_command += key + '=' + val['val'] + ' '

            st.write("#### cuda environment CLI command")
            st.write(f"```{env_cli_command}```")
            st.code(env_cli_command)


        if worker_type == 'CPU':
            env_cli_command = None
            
            st.write("## worker options")

            st.write("#### load worker settings")

            do_load_saved_worker_settings = st.checkbox(
                label='load saved worker settings?',
                value=False,
                key='do_load_saved_worker_settings',
                )

            if do_load_saved_worker_settings:
                worker_settings_files = app_settings.list_worker_settings_files()
                if len(worker_settings_files) > 0:
                    selected_worker_settings_file = st.selectbox(
                        label='select worker file',
                        options=worker_settings_files,
                        key='selected_worker_settings_file',
                        )

                    load_worker_settings = st.button(
                        label='load saved worker settings',
                        key='load_worker_settings')

                    if load_worker_settings:
                        app_settings.load_worker_settings(selected_worker_settings_file)
                else:
                    st.write("no saved worker settings file(s)")

            do_load_default_worker_settings = st.checkbox(
                label='load default worker settings?',
                value=False,
                key='do_load_default_worker_settings',
                )

            if do_load_default_worker_settings:

                load_default_worker_settings = st.button(
                    label='load default worker settings',
                    key='load_default_worker_settings',
                    )
                if load_default_worker_settings:
                    app_settings.load_default_worker_settings()
                    st.empty()

            show_advanced_worker_options = st.checkbox(
                label='Show advanced worker options',
                value=False,
                key='show_advanced_worker_options',
                )

            if show_advanced_worker_options:

                st.write("#### worker options")
                for i, cur in enumerate(app_settings.dask_worker_options_selected):
                    cur_type = cur['type']
                    cur_arg = cur['arg']
                    cur_options = cur['options']
                    cur_default = cur['default']
                    cur_desc = cur['description']

                    if type(cur_arg) == list:
                        cur_label = 'toggle ' + '"' + '/'.join(cur_arg) + '"' + ' worker option'
                    else:
                        cur_label = 'toggle ' + '"' + cur_arg + '"' + ' worker option'

                    if cur_default == None:
                        cur_display = st.checkbox(
                            label=cur_label,
                            value=False,
                            key=cur_label,
                            )
                    else:
                        cur_display = st.checkbox(
                            label=cur_label,
                            value=True,
                            key=cur_label,
                            )

                    if cur_display: 
                        cur_selection = get_st_inp_obj(cur, 'worker')
                        app_settings.dask_worker_options_selected[i]['default'] = cur_selection
                    else:
                        app_settings.dask_worker_options_selected[i]['default'] = None

                st.write("#### Save/delete worker settings")
                do_save_worker_settings = st.checkbox(
                    label='save current worker settings?',
                    value=False,
                    key='do_save_worker_settings')

                if do_save_worker_settings:
                    worker_save_filename = st.text_input(
                        label='enter a name for your worker settings',
                        key='new_worker_save_filename',
                        )
                    if len(worker_save_filename) > 0:
                        save_worker_settings = st.button(
                            label='save worker settings',
                            key='save_worker_settings',
                            )
                        if save_worker_settings:
                            app_settings.save_worker_settings(worker_save_filename)
                    else:
                        st.write('worker settings filename cannot be blank')

                do_delete_saved_worker_settings_file = st.checkbox(
                    label='delete saved worker settings file?',
                    value=False,
                    key='do_delete_saved_worker_settings_file')

                if do_delete_saved_worker_settings_file:
                    worker_settings_files = app_settings.list_worker_settings_files()
                    worker_settings_files_no_ext = [x.split('.')[0] for x in worker_settings_files]

                    if len(worker_settings_files_no_ext) > 0:
                        delete_saved_worker_filename = st.selectbox(
                                label='select worker file',
                                options=worker_settings_files,
                                key='delete_saved_worker_filename',
                                )
                        delete_saved_worker_settings_file = st.button(
                            label='delete saved worker settings file',
                            key='delete_saved_worker_settings_file',
                            )

                        if delete_saved_worker_settings_file:
                            app_settings.delete_saved_worker_settings_file(delete_saved_worker_filename)
                            st.empty()
                    else:
                        st.write("no saved worker settings file(s)")
                        st.empty()

            worker_cli_command = 'dask-worker'
            for cur in app_settings.dask_worker_options_selected:
                cur_type = cur['type']
                cur_arg = cur['arg']
                cur_options = cur['options']
                cur_default = cur['default']
                cur_desc = cur['description']

                if cur_default != None:
                    if cur_type == 'binary':
                        worker_cli_command += f" --{cur_default}"
                    else:
                        worker_cli_command += f" --{cur_arg}={cur_default}"

            st.write("#### worker CLI command")
            st.write(f"```{worker_cli_command}```")
            st.code(worker_cli_command)

    with st.expander("Cluster control"):

        app_settings.make_scheduler_selections_df()
        app_settings.make_worker_selections_df()
        app_settings.make_cuda_worker_selections_df()
        
        scheduler_df = app_settings.scheduler_df
        scheduler_scheduler_file = scheduler_df.loc['scheduler-file'].tolist()[0]
        

        if worker_type == 'CPU':
            worker_df = app_settings.worker_df
        if worker_type == 'GPU':
            worker_df = app_settings.cuda_worker_df
        worker_scheduler_file = worker_df.loc['scheduler-file'].tolist()[0]
        

        do_scheduler_files_match = scheduler_scheduler_file == worker_scheduler_file

        if do_scheduler_files_match:

            start_cluster = st.button(
                label='Start cluster',
                key='start_cluster',
                )

            if start_cluster:
                if worker_type == 'CPU':
                    start_a_cluster(scheduler_cli_command, worker_cli_command)
                if worker_type == 'GPU':
                    start_a_cluster(scheduler_cli_command, cuda_worker_cli_command, env_cli_command)

        else:
            st.write("scheduler file locations do not match in scheduler and worker settings. these fields must match before a cluster can be created")
            st.write(f"scheduler file location from **scheduler** settings:  \n  {scheduler_scheduler_file}")
            st.write(f"scheduler file location from **worker** settings:  \n  {worker_scheduler_file}")


        stop_cluster = st.button(
            label='Stop cluster',
            key='stop_cluster',
            )

        if stop_cluster:
            does_scheduler_file_exists = Path(scheduler_scheduler_file).is_file()
            if does_scheduler_file_exists: 
                stop_a_cluster(scheduler_scheduler_file)
                st.empty()
            else:
                st.write(f"file '{scheduler_scheduler_file}' does not exist. Please start a cluster.")

    with st.expander("Cluster connection"):
        st.write("After starting a cluster, you can connect to is in your **Jupyter Notebook** with this code:")
        jupyter_code = f"from dask.distributed import Client\nclient = Client(scheduler_file='{scheduler_scheduler_file}')\nclient #this will display the URL for accessign the dashboard\n\n#your dask operations here\n\nclient.close()\ndel client"
        st.code(jupyter_code, language='python')

        st.write("If you are performing your operations in a **python scrip**, you will need sctructure your code like this:")
        jupyter_code = f"from dask.distributed import Client\n\ndef main()\n\tclient = Client(scheduler_file='{scheduler_scheduler_file}')\n\n\t#your dask operations here\n\n\tclient.close()\n\tdel client\n\nif __name__ == '__main__':\n\tmain()"
        st.code(jupyter_code, language='python')


if __name__ == '__main__':
    main()
