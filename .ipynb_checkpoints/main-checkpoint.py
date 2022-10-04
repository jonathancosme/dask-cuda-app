import streamlit as st
from AppSettings import AppSettings


def main():
    
    @st.cache
    app_settings = AppSettings()
    
    for cur in app_settings.dask_scheduler_options:
    cur_type = cur['type']
    print(cur_type)
    cur_arg = cur['arg']
    cur_options = cur['options']
    cur_default = cur['default']
    cur_desc = cur['description']
    
    if cur_type == str:
        cur_selection = st.text_input(
            label=cur_arg,
            value=cur_default,
            help=cur_desc
        )
    
    user_selections.append(cur_selection)

if __name__ == '__main__':
    main()
