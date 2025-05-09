import streamlit as st
import app as csm
import json


def st_upload_file() -> dict:
    """_
    Create a widget that upload a JSON file
    Returns:
        data (dict): a dict containing the json file data
    """
    uploaded_file = st.file_uploader("Choose the JSON to analyze : ", type="json")
    if uploaded_file is not None:
        return json.load(uploaded_file)


def st_dowload_file() -> None:
    """
    Create a widget that dowload the data 
    that has be enriched to a JSON file
    Args:
        none
    """
    data = st.session_state.base_data
    json_file = json.dumps(data, indent=4)
    origin_file = "files/"

    st.download_button(
        label="Download JSON with new data",
        data=json_file,
        file_name=origin_file+"employees_data_download_auto.json",
        mime="application/json",
        icon=":material/download:",
    )


def st_add_button():
    """
    We add three buttons to toogle each way to display datas
    Args:
        None
    """
    if 'button_1' not in st.session_state:
        st.session_state.button_1 = False
        
    if 'button_2' not in st.session_state:
        st.session_state.button_2 = False
        
    if 'button_3' not in st.session_state:
        st.session_state.button_3 = False

    def click_button_1():
        st.session_state.button_1 = not st.session_state.button_1
        st.session_state.button_2 = False
        st.session_state.button_3 = False
        
    def click_button_2():
        st.session_state.button_2 = not st.session_state.button_2
        st.session_state.button_1 = False
        st.session_state.button_3 = False
    
    def click_button_3():
        st.session_state.button_3 = not st.session_state.button_3
        st.session_state.button_1 = False
        st.session_state.button_2 = False

    st.button("Selection by subsidiary", on_click=click_button_1)
    st.button("Selection by employee", on_click=click_button_2)
    st.button("display Name Job", on_click=click_button_3)

    if st.session_state.button_1:
        display_options_in_streamlit()
    elif st.session_state.button_2:
        display_selection_by_employee()
    elif st.session_state.button_3:
        st_interactive_board()


def st_interactive_board():
    """
    display a widget, not quite finished
    """
    data = st.session_state.base_data
    sub_names = csm.get_subsidiary_name(data)
    option_subsidiary = st.selectbox(
        'Which subsidiary?',
        sub_names,
        index=None,
        placeholder="Select subsidiary..",)
    # name_or_job_input = st.text_input(
    #     "Enter the name or the job of your employee : "
    # )
    
    col_header_name, col_header_job = st.columns(2)
    col_header_name.header("Name")
    col_header_job.header("Job")
    for sub in sub_names:
        if option_subsidiary == sub: 
            for employee in data[sub]['employees']:
                # if name_or_job_input == employee["name"]:
                col_name, col_job, = st.columns(2)
                col_name.markdown(employee["name"])
                col_job.markdown(employee["job"])
    

def display_data_for_streamlit():
    """
    display data in streamlit
    parameters:
        none
    Returns:
        none
    """
    st_add_button()
    
    st_dowload_file()


def display_options_in_streamlit():
    """
    we offer a selection by subsidiary 
    with checkbox to select employees or statistics
    parameters:
        none
    Returns:
        none : 
    """
    data = st.session_state.base_data
    sub_names = csm.get_subsidiary_name(data, True)
    
    option = st.selectbox(
        'Which subsidiary?',
        sub_names,
        index=None,
        placeholder="Select subsidiary..",)
    
    for sub in sub_names:
        if sub == option: 
            # if st.checkbox(f'show subsidiary {sub}'):
            st.write(sub)
            if "employees" in data[sub].keys():
                if st.checkbox(f'show employees for {sub}'):
                    st.write(data[sub]["employees"])
            if st.checkbox(f'show statistics for {sub}'):
                st.write(data[sub]["statistics"])


def display_selection_by_employee():
    """
    we offer a selection by textinput
    to look for a specific employee
    parameters:
        none
    Returns:
        none : 
    """
    data = st.session_state.base_data
    sub_names = csm.get_subsidiary_name(data)
    name_input = st.text_input(
        "Enter the name of your employee : "
    )

    for sub in sub_names:
        sub_displayed = False
        for employee in data[sub]["employees"]:
            if employee['name'].lower() == name_input.lower():
                if not sub_displayed:
                    st.write(sub)
                st.write(employee)
                sub_displayed = True


def main():
    """
    we run the script to enrich the data with statistics on the salaries of the employees
    and we display it via streamlit
    parameters:
        none
    Returns:
        none : 
    """
    st.title('Salary Visualisation')
    st.session_state.base_data = st_upload_file()
    if st.session_state.base_data != None:
        if csm.check_data_integrity(st.session_state.base_data):
            st.session_state.corporate_data = csm.generate_enriched_data(st.session_state.base_data)
            display_data_for_streamlit()
        else:
            st.write("JSON not valid")
    

if __name__ == "__main__":
    main()