import streamlit as st
from AppSettings import AppSettings
from utils.functions import get_st_inp_obj


def main():

    @st.cache(allow_output_mutation=True)
    def load_app_settings():
        app_settings = AppSettings()
        return app_settings
    app_settings = load_app_settings()

    # app_settings = AppSettings()

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
        else:
            st.write("no saved scheduler settings file(s)")

    do_load_default_scheduler_settings = st.checkbox(
        label='load default scheduler settings?',
        value=False,
        key='do_load_default_scheduler_settings',
        )

    show_advanced_scheduler_options = st.checkbox(
        label='Show advanced scheduler options',
        value=False,
        key='show_advanced_scheduler_options',
        )

    if show_advanced_scheduler_options:

        if do_load_default_scheduler_settings:

            load_default_scheduler_settings = st.button(
                label='load default scheduler settings',
                key='load_default_scheduler_settings',
                )
            if load_default_scheduler_settings:
                app_settings.load_default_scheduler_settings()
                st.empty()

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


                # if cur_type == str:
                #     if cur_default != None:
                #         cur_selection = st.text_input(
                #             label=cur_arg,
                #             value=cur_default,
                #             help=cur_desc,
                #             key=cur_arg + '_scheduler',
                #         )
                #     else:
                #         cur_selection = st.text_input(
                #             label=cur_arg,
                #             placeholder=cur_default,
                #             help=cur_desc,
                #             key=cur_arg + '_scheduler',
                #         )
                #     scheduler_cli_command += f" --{cur_arg}={cur_selection}"
                #     app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

                # if cur_type == int:
                #     if cur_default != None:
                #         cur_selection = st.text_input(
                #             label=cur_arg,
                #             value=cur_default,
                #             help=cur_desc,
                #             key=cur_arg + '_scheduler',
                #         )
                #     else:
                #         cur_selection = st.text_input(
                #             label=cur_arg,
                #             placeholder=cur_default,
                #             help=cur_desc,
                #             key=cur_arg + '_scheduler',
                #         )
                #     scheduler_cli_command += f" --{cur_arg}={cur_selection}"
                #     app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

                # if cur_type == bool:
                #     if cur_default != None:
                #         cur_selection = st.checkbox(
                #                 label=cur_arg,
                #                 value=cur_default,
                #                 help=cur_desc,
                #                 key=cur_arg + '_scheduler',
                #             )
                #     else:
                #         cur_selection = st.checkbox(
                #                 label=cur_arg,
                #                 help=cur_desc,
                #                 key=cur_arg + '_scheduler',
                #             )
                #     scheduler_cli_command += f" --{cur_arg}={cur_selection}"
                #     app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

                # if cur_type == 'binary':
                #     if cur_default != None:
                #         cur_selection = st.radio(
                #                 label='/'.join(cur_arg),
                #                 options=cur_arg,
                #                 index=cur_arg.index(cur_default),
                #                 help=cur_desc,
                #                 key='/'.join(cur_arg) + '_scheduler',
                #             )
                #     else:
                #         cur_selection = st.radio(
                #                 label='/'.join(cur_arg),
                #                 options=cur_arg,
                #                 help=cur_desc,
                #                 key='/'.join(cur_arg) + '_scheduler',
                #             )
                #     scheduler_cli_command += f" --{cur_selection}"
                #     app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

                # if cur_type == 'single-select':
                #     if cur_default != None:
                #         cur_selection = st.selectbox(
                #                 label=cur_arg,
                #                 options=cur_options,
                #                 value=cur_options.index(cur_default),
                #                 help=cur_desc,
                #                 key=cur_arg + '_scheduler',
                #             )
                #     else:
                #         cur_selection = st.selectbox(
                #                 label=cur_arg,
                #                 options=cur_options,
                #                 help=cur_desc,
                #                 key=cur_arg + '_scheduler',
                #             )
                #     scheduler_cli_command += f" --{cur_arg}={cur_selection}"
                #     app_settings.dask_scheduler_options_selected[i]['default'] = cur_selection

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

        # if do_save_scheduler_settings:
        #     scheduler_settings_files = app_settings.list_scheduler_settings_files()
        #     scheduler_settings_files_no_ext = [x.split('.')[0] for x in scheduler_settings_files]

        #     scheduler_save_type = st.radio(
        #         label='save a new file or overwrite an old one?',
        #         options=['new', 'overwrite'],
        #         index=0,
        #         key='scheduler_save_type',
        #         )

        #     if scheduler_save_type == 'new':
        #         scheduler_save_filename = st.text_input(
        #             label='enter a name for your scheduler settings',
        #             key='new_scheduler_save_filename',
        #             )

        #     if scheduler_save_type == 'overwrite':
        #         if len(scheduler_settings_files) > 0:
        #             scheduler_save_filename = st.selectbox(
        #                 label='select scheduler file',
        #                 options=scheduler_settings_files,
        #                 key='overwrite_scheduler_save_filename',
        #                 )
        #         else:
        #             scheduler_save_filename = ''
        #             st.write("no saved scheduler settings file(s)")
        #     if len(scheduler_save_filename) > 0:
        #         does_scheduler_file_exists = scheduler_save_filename in scheduler_settings_files_no_ext
        #         if does_scheduler_file_exists & (scheduler_save_type == 'new'):
        #             st.write('this filename already exists')
        #         else:
        #             save_scheduler_settings = st.button(
        #                 label='save scheduler settings',
        #                 key='save_scheduler_settings',
        #                 )
        #             if save_scheduler_settings:
        #                 app_settings.save_scheduler_settings(scheduler_save_filename)
        #     else:
        #         st.write('scheduler settings filename cannot be blank')

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
    st.code(scheduler_cli_command)


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

        # for i, cur in enumerate(app_settings.dask_cuda_worker_options):
        #     cur_type = cur['type']
        #     # st.write(cur_type) 
        #     cur_arg = cur['arg']
        #     cur_options = cur['options']
        #     cur_default = cur['default']
        #     cur_desc = cur['description']

        #     if type(cur_arg) == list:
        #         cur_label = 'toggle ' + '/'.join(cur_arg) + ' cuda worker option'
        #     else:
        #         cur_label = 'toggle ' + cur_arg + ' cuda worker option'

        #     if cur_default == None:
        #         cur_display = st.checkbox(
        #             label=cur_label,
        #             value=False,
        #             key=cur_label,
        #             )
        #     else:
        #         cur_display = st.checkbox(
        #             label=cur_label,
        #             value=True,
        #             key=cur_label,
        #             )

        #     if cur_display: 

        #         if cur_type == str:
        #             if cur_default != None:
        #                 cur_selection = st.text_input(
        #                     label=cur_arg,
        #                     value=cur_default,
        #                     help=cur_desc,
        #                     key=cur_arg + '_cuda_worker',
        #                 )
        #             else:
        #                 cur_selection = st.text_input(
        #                     label=cur_arg,
        #                     placeholder=cur_default,
        #                     help=cur_desc,
        #                     key=cur_arg + '_cuda_worker',
        #                 )
        #             cuda_worker_cli_command += f" --{cur_arg}={cur_selection}"
        #             app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection

        #         if cur_type == int:
        #             if cur_default != None:
        #                 cur_selection = st.text_input(
        #                     label=cur_arg,
        #                     value=cur_default,
        #                     help=cur_desc,
        #                     key=cur_arg + '_cuda_worker',
        #                 )
        #             else:
        #                 cur_selection = st.text_input(
        #                     label=cur_arg,
        #                     placeholder=cur_default,
        #                     help=cur_desc,
        #                     key=cur_arg + '_cuda_worker',
        #                 )
        #             cuda_worker_cli_command += f" --{cur_arg}={cur_selection}"
        #             app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection

        #         if cur_type == bool:
        #             if cur_default != None:
        #                 cur_selection = st.checkbox(
        #                         label=cur_arg,
        #                         value=cur_default,
        #                         help=cur_desc,
        #                         key=cur_arg + '_cuda_worker',
        #                     )
        #             else:
        #                 cur_selection = st.checkbox(
        #                         label=cur_arg,
        #                         help=cur_desc,
        #                         key=cur_arg + '_cuda_worker',
        #                     )
        #             cuda_worker_cli_command += f" --{cur_arg}={cur_selection}"
        #             app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection

        #         if cur_type == 'binary':
        #             if cur_default != None:
        #                 cur_selection = st.radio(
        #                         label='/'.join(cur_arg),
        #                         options=cur_arg,
        #                         index=cur_arg.index(cur_default),
        #                         help=cur_desc,
        #                         key='/'.join(cur_arg) + '_cuda_worker',
        #                     )
        #             else:
        #                 cur_selection = st.radio(
        #                         label='/'.join(cur_arg),
        #                         options=cur_arg,
        #                         help=cur_desc,
        #                         key='/'.join(cur_arg) + '_cuda_worker',
        #                     )
        #             cuda_worker_cli_command += f" --{cur_selection}"
        #             app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection

        #         if cur_type == 'single-select':
        #             if cur_default != None:
        #                 cur_selection = st.selectbox(
        #                         label=cur_arg,
        #                         options=cur_options,
        #                         value=cur_options.index(cur_default),
        #                         help=cur_desc,
        #                         key=cur_arg + '_cuda_worker',
        #                     )
        #             else:
        #                 cur_selection = st.selectbox(
        #                         label=cur_arg,
        #                         options=cur_options,
        #                         help=cur_desc,
        #                         key=cur_arg + '_cuda_worker',
        #                     )
        #             cuda_worker_cli_command += f" --{cur_arg}={cur_selection}"
        #             app_settings.dask_cuda_worker_options_selected[i]['default'] = cur_selection
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

        cuda_worker_cli_command = 'dask-cuda_worker'
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
        st.code(cuda_worker_cli_command)

    if worker_type == 'CPU':
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
        st.code(worker_cli_command)
    # if worker_type == 'CPU':
    #     st.write("## Worker options")
    #     worker_cli_command = 'dask-worker'
    #     for i, cur in enumerate(app_settings.dask_worker_options):
    #         cur_type = cur['type']
    #         # st.write(cur_type) 
    #         cur_arg = cur['arg']
    #         cur_options = cur['options']
    #         cur_default = cur['default']
    #         cur_desc = cur['description']

    #         if type(cur_arg) == list:
    #             cur_label = 'toggle ' + '/'.join(cur_arg) + ' worker option'
    #         else:
    #             cur_label = 'toggle ' + cur_arg + ' worker option'

    #         if cur_default == None:
    #             cur_display = st.checkbox(
    #                 label=cur_label,
    #                 value=False,
    #                 key=cur_label,
    #                 )
    #         else:
    #             cur_display = st.checkbox(
    #                 label=cur_label,
    #                 value=True,
    #                 key=cur_label,
    #                 )

    #         if cur_display: 

    #             if cur_type == str:
    #                 if cur_default != None:
    #                     cur_selection = st.text_input(
    #                         label=cur_arg,
    #                         value=cur_default,
    #                         help=cur_desc,
    #                         key=cur_arg + '_worker',
    #                     )
    #                 else:
    #                     cur_selection = st.text_input(
    #                         label=cur_arg,
    #                         placeholder=cur_default,
    #                         help=cur_desc,
    #                         key=cur_arg + '_worker',
    #                     )
    #                 worker_cli_command += f" --{cur_arg}={cur_selection}"
    #                 app_settings.dask_worker_options_selected[i]['default'] = cur_selection

    #             if cur_type == int:
    #                 if cur_default != None:
    #                     cur_selection = st.text_input(
    #                         label=cur_arg,
    #                         value=cur_default,
    #                         help=cur_desc,
    #                         key=cur_arg + '_worker',
    #                     )
    #                 else:
    #                     cur_selection = st.text_input(
    #                         label=cur_arg,
    #                         placeholder=cur_default,
    #                         help=cur_desc,
    #                         key=cur_arg + '_worker',
    #                     )
    #                 worker_cli_command += f" --{cur_arg}={cur_selection}"
    #                 app_settings.dask_worker_options_selected[i]['default'] = cur_selection

    #             if cur_type == bool:
    #                 if cur_default != None:
    #                     cur_selection = st.checkbox(
    #                             label=cur_arg,
    #                             value=cur_default,
    #                             help=cur_desc,
    #                             key=cur_arg + '_worker',
    #                         )
    #                 else:
    #                     cur_selection = st.checkbox(
    #                             label=cur_arg,
    #                             help=cur_desc,
    #                             key=cur_arg + '_worker',
    #                         )
    #                 worker_cli_command += f" --{cur_arg}={cur_selection}"
    #                 app_settings.dask_worker_options_selected[i]['default'] = cur_selection

    #             if cur_type == 'binary':
    #                 if cur_default != None:
    #                     cur_selection = st.radio(
    #                             label='/'.join(cur_arg),
    #                             options=cur_arg,
    #                             index=cur_arg.index(cur_default),
    #                             help=cur_desc,
    #                             key='/'.join(cur_arg) + '_worker',
    #                         )
    #                 else:
    #                     cur_selection = st.radio(
    #                             label='/'.join(cur_arg),
    #                             options=cur_arg,
    #                             help=cur_desc,
    #                             key='/'.join(cur_arg) + '_worker',
    #                         )
    #                 worker_cli_command += f" --{cur_selection}"
    #                 app_settings.dask_worker_options_selected[i]['default'] = cur_selection

    #             if cur_type == 'single-select':
    #                 if cur_default != None:
    #                     cur_selection = st.selectbox(
    #                             label=cur_arg,
    #                             options=cur_options,
    #                             value=cur_options.index(cur_default),
    #                             help=cur_desc,
    #                             key=cur_arg + '_worker',
    #                         )
    #                 else:
    #                     cur_selection = st.selectbox(
    #                             label=cur_arg,
    #                             options=cur_options,
    #                             help=cur_desc,
    #                             key=cur_arg + '_worker',
    #                         )
    #                 worker_cli_command += f" --{cur_arg}={cur_selection}"
    #                 app_settings.dask_worker_options_selected[i]['default'] = cur_selection

    # st.write(scheduler_cli_command)
    # if worker_type == 'GPU':
    #     st.write(cuda_worker_cli_command)
    # if worker_type == 'CPU':
    #     st.write(worker_cli_command)
    # st.write(app_settings.dask_scheduler_options_selected)

if __name__ == '__main__':
    main()
