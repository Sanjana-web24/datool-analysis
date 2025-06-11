import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import plotly.graph_objs as go
from io import BytesIO

st.title("Data Analysis Dashboard")

# UI Styling
st.markdown("""
<style>
    .stApp {
        background-color: #dbd3e85c;
        font-family: 'Times New Roman', sans-serif;
    }
    h1 {
        color: #000000;
        font-size: 5.5em;
        text-align: center;
    }
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
    }
    .stSelectbox {
        font-size: 1.2em;
    }
    .raw-button-container {
        text-align: center;
        margin: 10px 0 20px 0;
    }
    .raw-button {
        background-color: #007bff;
        border-radius: 50%;
        color: white !important;
        font-weight: bold;
        width: 70px;
        height: 70px;
        border: none;
        font-size: 1.2em;
        cursor: pointer;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        user-select: none;
        transition: background-color 0.3s ease;
        margin: 0 auto;
    }
    .raw-button:hover {
        background-color: #0056b3;
    }
    .raw-label {
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 1.1em;
        text-align: center;
        color: #000000;
        cursor: pointer;
    }
    .back-button-container {
        text-align: center;
        margin-top: 20px;
    }
    .back-button {
        background-color: #28a745;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 10px 40px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .back-button:hover {
        background-color: #1e7e34;
    }
</style>
""", unsafe_allow_html=True)

# Base URL for SVN (change this link according to where you want to extract data from)
BASE_URL = "http://tpms.cypress.com/tpmslib/Char_CCD/PSOC/Projects/TEMP/"

def list_directories(url):
    """Returns a list of directories from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        dirs = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('/') and href != '../':
                dirs.append(href.strip('/'))
        return dirs
    except Exception as e:
        st.error(f"Failed to fetch directories from {url}: {e}")
        return []

def list_excel_files(url):
    """Returns a list of Excel files from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        files = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and (href.endswith('.xls') or href.endswith('.xlsx')):
                files.append(href)
        return files
    except Exception as e:
        st.error(f"Failed to fetch files from {url}: {e}")
        return []

def fetch_excel_file(url):
    """Fetch Excel file content from url and load as pd.ExcelFile."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        filedata = BytesIO(response.content)
        xls = pd.ExcelFile(filedata, engine='openpyxl')
        return xls
    except Exception as e:
        st.error(f"Failed to load Excel file from {url}: {e}")
        return None

def safe_float_conversion(value):
    """Convert a string to float, handling fractions."""
    try:
        if isinstance(value, str) and '/' in value:
            return eval(value)  
        return float(value)
    except ValueError:
        return None  

def calculate_bubble_sizes(df, x_cols, y_col, min_size=10, max_size=60):
    """Calculate bubble sizes for the plot based on the values in the DataFrame."""
    values = pd.Series(dtype='float')
    for x_col in x_cols:
        if x_col in df.columns:
            values = pd.concat([values, df[x_col].dropna().apply(safe_float_conversion)], ignore_index=True)
    if y_col in df.columns:
        values = pd.concat([values, df[y_col].dropna().apply(safe_float_conversion)], ignore_index=True)
    if values.empty or values.nunique() == 1:
        return [min_size] * len(df)
    min_val = values.min()
    max_val = values.max()
    sizes = []
    for _, row in df.iterrows():
        local_vals = []
        for x_col in x_cols:
            if x_col in row and pd.notna(row[x_col]):
                local_vals.append(safe_float_conversion(row[x_col]))
        if y_col in row and pd.notna(row[y_col]):
            local_vals.append(safe_float_conversion(row[y_col]))
        if not local_vals:
            sizes.append(min_size)
            continue
        local_vals = [val for val in local_vals if val is not None]
        if not local_vals:
            sizes.append(min_size)
            continue
        val = max(local_vals)
        norm = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
        size = norm * (max_size - min_size) + min_size
        sizes.append(size)
    return sizes

#parameter selection
if 'data_view' not in st.session_state:
    st.session_state.data_view = "summary"
if 'selected_param' not in st.session_state:
    st.session_state.selected_param = None
if 'selected_param_raw' not in st.session_state:
    st.session_state.selected_param_raw = None

#step - 1
project_options = list_directories(BASE_URL)
selected_project = st.selectbox("Choose a Project:", project_options)

if selected_project:
    #step - 2
    ip_url = BASE_URL + selected_project + "/"
    ip_options = list_directories(ip_url)
    selected_ip = st.selectbox("Choose IP/Module:", ip_options)

    if selected_ip:
        #step - 3 
        summary_url = ip_url + selected_ip + "/Summary/"
        summary_files = list_excel_files(summary_url)

        # Checking combined_excel_file (you can rename here according to your file requirment)
        combined_excel_file = "combined_excel_file.xlsx"
        combined_file_exists = combined_excel_file in summary_files

        if not summary_files:
            st.warning(f"No Excel summary files found in {summary_url}. Redirecting to Raw folder...")
            raw_url = ip_url + selected_ip + "/Raw/"
            raw_files = list_excel_files(raw_url)
            if raw_files:
                selected_raw_file = st.selectbox("Choose a Raw Excel file", raw_files)
                raw_file_url = raw_url + selected_raw_file
                xls = fetch_excel_file(raw_file_url)
                if xls is None:
                    st.stop()
                raw_sheet = next((s for s in xls.sheet_names if "raw" in s.lower()), None)
                if raw_sheet:
                    df_raw = xls.parse(raw_sheet)
                    df_raw.columns = [col.strip() for col in df_raw.columns]
                    st.dataframe(df_raw)
                else:
                    st.error("No raw sheet found in the selected raw file.")
            else:
                st.error("No raw files found in the Raw folder.")
            st.stop()

        else:
            if combined_file_exists:
                selected_summary_file = combined_excel_file
            else:
                selected_summary_file = st.selectbox("Choose a Summary Excel file", summary_files)

            summary_file_url = summary_url + selected_summary_file

            xls = fetch_excel_file(summary_file_url)
            if xls is None:
                st.stop()

            summary_sheets = [s for s in xls.sheet_names if "summary" in s.lower()]
            if not summary_sheets:
                st.warning("No 'Summary' sheet found in Excel file. Redirecting to Raw folder...")
                raw_url = ip_url + selected_ip + "/Raw/"
                raw_files = list_excel_files(raw_url)
                if raw_files:
                    selected_raw_file = st.selectbox("Choose a Raw Excel file", raw_files)
                    raw_file_url = raw_url + selected_raw_file
                    xls = fetch_excel_file(raw_file_url)
                    if xls is None: 
                        st.stop()
                    raw_sheet = next((s for s in xls.sheet_names if "raw" in s.lower()), None)
                    if raw_sheet:
                        df_raw = xls.parse(raw_sheet)
                        df_raw.columns = [col.strip() for col in df_raw.columns]
                        st.dataframe(df_raw)
                    else:
                        st.error("No raw sheet found in the selected raw file.")
                else:
                    st.error("No raw files found in the Raw folder.")
                st.stop()
            summary_sheet = summary_sheets[0]

            # Raw sheet priority
            raw_sheet_priority = ['edited_raw', 'raw', 'corner_raw', 'RAW_TYP', 'RAW_CORNER']
            raw_sheet = None
            for rs in raw_sheet_priority:
                matching_sheets = [s for s in xls.sheet_names if rs in s.lower()]
                if matching_sheets:
                    raw_sheet = matching_sheets[0]
                    break

            df_summary = xls.parse(summary_sheet)
            df_summary.columns = [col.strip() for col in df_summary.columns]

            df_raw = None
            if raw_sheet:
                df_raw = xls.parse(raw_sheet)
                df_raw.columns = [col.strip() for col in df_raw.columns]

            rename_map = {
                "specification": "Spec_min",
                "unnamed: 7": "Spec_avg",
                "unnamed: 8": "Spec_max",
                "typical": "Typical_Min",
                "unnamed: 13": "Typical_Max",
                "unnamed: 12": "Typical_Avg",
                "unnamed: 14": "Typical_Stdev",
                "ff": "FF_min",
                "fs": "FS_min",
                "sf": "SF_min",
                "ss": "SS_min",
                "unnamed: 17": "FF_max",
                "unnamed: 19": "FS_max",
                "unnamed: 21": "SF_max",
                "unnamed: 23": "SS_max"
            }
            df_summary.rename(columns={col: rename_map.get(col.lower(), col) for col in df_summary.columns}, inplace=True)

            param_col = next((col for col in df_summary.columns if "parameter" in col.lower()), None)
            if not param_col:
                st.error("No 'parameter' column found in summary data.")
                st.stop()

            param_col1, param_col2, param_col3, param_col4 = st.columns([4, 4, 4, 1])

            with param_col1:
                parameters = df_summary[param_col].dropna().unique().tolist()
                if st.session_state.data_view == "summary":
                    st.session_state.selected_param = st.selectbox("Select Parameter", parameters)
                    st.session_state.selected_param_raw = st.session_state.selected_param
                else:
                    st.markdown(f"**Selected Parameter:** {st.session_state.selected_param_raw}")

            with param_col2:
                typical_values = [
                    "Typical_Min", "Typical_Max", "Typical_Avg", "Typical_Stdev",
                    "Typ_Min", "Typ_Max", "Typ_Avg", "Typ_Stdev",
                    "TYP_MIN", "TYP_MAX", "TYP_AVG", "TYP_STD"
                ]
                corner_values = ["FF_max", "FS_max", "SF_max", "SS_max", "FF_min", "FS_min", "SF_min", "SS_min"]
                cpk_analysis = ["CPK"]
                sample_size = ["Sample Size"]

                category_options = {
                    "Typical Values": typical_values,
                    "Corner Values": corner_values,
                    "CPK": cpk_analysis,
                    "Sample Size": sample_size
                }
                x_category = st.selectbox("Select X-Axis Category", list(category_options.keys()))

            with param_col3:
                y_category = st.selectbox("Select Y-Axis Category", list(category_options.keys()))

            with param_col4:
                st.markdown('<div class="raw-label">Raw Data</div>', unsafe_allow_html=True)
                if st.button("RAW", key="raw_btn", help="Click to view Raw Data"):
                    st.session_state.data_view = "raw_data"

            if st.session_state.data_view == "summary":
                selected_param = st.session_state.selected_param
                x_axis_cols = category_options[x_category]
                y_axis_cols = category_options[y_category]

                color_map = {
                    'FF_min': 'red', 'FF_max': 'red',
                    'FS_min': 'green', 'FS_max': 'green',
                    'SF_min': 'blue', 'SF_max': 'blue',
                    'SS_min': 'yellow', 'SS_max': 'yellow',
                    'Typical_Min': 'pink', 'Typical_Max': 'pink',
                    'TYP_MIN': 'pink', 'TYP_MAX': 'pink', 'TYP_AVG': 'pink', 'TYP_STD': 'pink',
                    'Typical_Avg': 'pink', 'Typical_Stdev': 'pink'
                }

                filtered_summary_df = df_summary[df_summary[param_col] == selected_param]

                st.subheader(f"Summary Data for Parameter: {selected_param}")

                result_col = next((col for col in filtered_summary_df.columns if "result" in col.lower()), None)

                def highlight_fails(row):
                    if result_col and str(row[result_col]).strip().lower() == "fail":
                        return ['background-color: red'] * len(row)
                    return [''] * len(row)

                st.dataframe(filtered_summary_df.style.apply(highlight_fails, axis=1), use_container_width=True)

                bubble_sizes = calculate_bubble_sizes(filtered_summary_df, x_axis_cols, y_axis_cols[0])

                fig = go.Figure()
                added_legend = set()

                for x_col in x_axis_cols:
                    if x_col in filtered_summary_df.columns:
                        for y_col in y_axis_cols:
                            if y_col in filtered_summary_df.columns:
                                show_legend = y_col not in added_legend
                                if show_legend:
                                    added_legend.add(y_col)
                                fig.add_trace(go.Scatter(
                                    x=filtered_summary_df[x_col],
                                    y=filtered_summary_df[y_col],
                                    mode='markers',
                                    marker=dict(
                                        size=bubble_sizes,
                                        color=color_map.get(y_col, 'gray'),
                                        opacity=0.7,
                                        line=dict(width=1, color='black')
                                    ),
                                    name=y_col,
                                    legendgroup=y_col,
                                    showlegend=show_legend
                                ))

                if 'Spec_min' in filtered_summary_df.columns and not filtered_summary_df['Spec_min'].isnull().all():
                    spec_min = filtered_summary_df['Spec_min'].values[0]
                    fig.add_shape(type='line', x0=spec_min, x1=spec_min,
                                   y0=0, y1=1, xref='x', yref='paper',
                                   line=dict(color='black', width=4, dash='dash'))
                if 'Spec_max' in filtered_summary_df.columns and not filtered_summary_df['Spec_max'].isnull().all():
                    spec_max = filtered_summary_df['Spec_max'].values[0]
                    fig.add_shape(type='line', x0=spec_max, x1=spec_max,
                                   y0=0, y1=1, xref='x', yref='paper',
                                   line=dict(color='black', width=4, dash='dash'))

                fig.update_layout(
                    title="Bubble Chart",
                    xaxis_title=f"{x_category}",
                    yaxis_title=f"{y_category}",
                    height=600,
                    margin=dict(l=40, r=40, t=80, b=40),
                    showlegend=True,
                    legend_title_text="Color Mapping",
                    legend=dict(
                        itemsizing='constant',
                        bgcolor='rgba(255,255,255,0.5)',
                        bordercolor='black',
                        borderwidth=1
                    ),
                    dragmode='zoom',
                    annotations=[
                        dict(
                            text="(Double-click and drag to zoom in values)",
                            x=0.5, y=1.02,
                            xref='paper', yref='paper',
                            showarrow=False,
                            font=dict(
                                size=12,
                                color="#5d5858",
                                family="Arial, sans-serif"
                            ),
                            xanchor='center',
                            yanchor='bottom'
                        )
                    ]
                )

                st.plotly_chart(fig, use_container_width=True)

                # Edited raw data view
                if df_raw is not None:
                    st.subheader("Edited Raw Data")
                    filtered_raw_df = df_raw.copy()
                    if param_col in df_raw.columns:
                        filtered_raw_df = df_raw[df_raw[param_col] == selected_param]

                    result_col = next((col for col in filtered_raw_df.columns if 'result' in col.lower()), None)

                    def highlight_fails_raw(row):
                        if result_col and isinstance(row[result_col], str) and row[result_col].lower() == 'fail':
                            return ['background-color: red'] * len(row)
                        return [''] * len(row)

                    st.dataframe(filtered_raw_df.style.apply(highlight_fails_raw, axis=1), use_container_width=True)

            elif st.session_state.data_view == "raw_data":
                st.subheader("Raw Data")

                if df_raw is not None:
                    param_col_raw = None
                    for col in df_raw.columns:
                        if "parameter" in col.lower():
                            param_col_raw = col
                            break

                    if param_col_raw:
                        parameters_raw = df_raw[param_col_raw].dropna().unique().tolist()
                        if st.session_state.selected_param_raw is None or st.session_state.selected_param_raw not in parameters_raw:
                            st.session_state.selected_param_raw = st.selectbox("Select Parameter", parameters_raw)
                        else:
                            st.markdown(f"**Selected Parameter:** {st.session_state.selected_param_raw}")
                        filtered_raw_df = df_raw[df_raw[param_col_raw] == st.session_state.selected_param_raw]
                    else:
                        st.info("Parameter column not found in raw data.")
                        filtered_raw_df = df_raw.copy()

                    result_col_raw = next((col for col in filtered_raw_df.columns if 'result' in col.lower()), None)

                    def highlight_fails_raw(row):
                        if result_col_raw and isinstance(row[result_col_raw], str) and row[result_col_raw].lower() == 'fail':
                            return ['background-color: red'] * len(row)
                        return [''] * len(row)

                    styled_raw_df = filtered_raw_df.style.apply(highlight_fails_raw, axis=1)
                    st.dataframe(styled_raw_df, use_container_width=True)

                    voltage_cols = [col for col in filtered_raw_df.columns if col.lower().startswith('v')]
                    temperature_cols = [col for col in filtered_raw_df.columns if col.lower() == 'temp']

                    y_axis_options = [col for col in filtered_raw_df.columns if col.lower() not in ['parameter', 'result']]
                    
                    #x and y axis selection
                    col_voltage, col_y_axis = st.columns(2)
                    
                    with col_voltage:
                        selected_voltage = st.selectbox("Select one Voltage column:", voltage_cols, index=0)

                    with col_y_axis:
                        y_axis = st.selectbox("Select Y-Axis Column", y_axis_options)

                    if not voltage_cols or not temperature_cols:
                        st.error("Both voltage columns (starting with 'V'/'v') and 'Temp' column must be present in raw data for combined plotting.")
                    else:
                        required_cols = [selected_voltage] + temperature_cols + [y_axis]
                        filtered_raw_df_clean = filtered_raw_df.dropna(subset=required_cols)

                        # combining temp and voltage and naming as temp/voltage
                        filtered_raw_df_clean['Temp_Voltage'] = filtered_raw_df_clean[temperature_cols[0]].astype(str) + '/' + filtered_raw_df_clean[selected_voltage].astype(str)

                        bubble_sizes = calculate_bubble_sizes(filtered_raw_df_clean, [selected_voltage], y_axis)

                        spec_min = None
                        spec_max = None
                        if 'spec_min' in filtered_raw_df_clean.columns:
                            vals = filtered_raw_df_clean['spec_min'].dropna().unique()
                            if len(vals) > 0:
                                spec_min = vals[0]
                        if 'spec_max' in filtered_raw_df_clean.columns:
                            vals = filtered_raw_df_clean['spec_max'].dropna().unique()
                            if len(vals) > 0:
                                spec_max = vals[0]

                        fig = go.Figure()

                        fig.add_trace(go.Scatter(
                            x=filtered_raw_df_clean['Temp_Voltage'],
                            y=filtered_raw_df_clean[y_axis],
                            mode='markers',
                            marker=dict(
                                size=bubble_sizes,
                                color='blue',
                                opacity=0.7,
                                line=dict(width=1, color='black')
                            ),
                            name=f"{y_axis} vs Temp/Voltage",
                        ))

                        # Highlighting the results which are failed
                        for index, row in filtered_raw_df_clean.iterrows():
                            if result_col_raw and isinstance(row[result_col_raw], str) and row[result_col_raw].lower() == 'fail':
                                fig.add_trace(go.Scatter(
                                    x=[row['Temp_Voltage']],
                                    y=[row[y_axis]],
                                    mode='markers',
                                    marker=dict(
                                        size=15,
                                        color='red',
                                        line=dict(width=2, color='black')
                                    ),
                                    name='Fail',
                                    showlegend=False
                                ))

                        if spec_min is not None:
                            fig.add_hline(
                                y=spec_min,
                                line=dict(color='black', dash='dot', width=4),
                                annotation_text='Spec Min',
                                annotation_position='bottom left'
                            )
                        if spec_max is not None:
                            fig.add_hline(
                                y=spec_max,
                                line=dict(color='black', dash='dot', width=4),
                                annotation_text='Spec Max',
                                annotation_position='top left'
                            )

                        fig.update_layout(
                            xaxis=dict(
                                title='Temperature / Voltage',
                                tickangle=45,
                                automargin=True,
                            ),
                            yaxis=dict(
                                title=y_axis,
                            ),
                            height=600,
                            margin=dict(l=50, r=50, t=50, b=120),
                            title=f"{y_axis} vs Temp/Voltage (Parameter: {st.session_state.selected_param_raw})"
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        if st.button("Back to Summary", key="back_from_raw_btn", help="Go back to Summary View"):
                            st.session_state.data_view = "summary"

                #searches the file with same name as that of the selected parameter in a folder named {selected sheet}_rawdata
                if not raw_sheet:
                    base_name = selected_summary_file.split('.')[0]
                    specific_raw_folder = f"{base_name}_rawdata"
                    specific_raw_url = summary_url + specific_raw_folder + "/"
                    specific_raw_files = list_excel_files(specific_raw_url)

                    if specific_raw_files:
                        parameter_file_name = f"{st.session_state.selected_param}.xlsx"
                        if parameter_file_name in specific_raw_files:
                            parameter_file_url = specific_raw_url + parameter_file_name
                            xls = fetch_excel_file(parameter_file_url)
                            if xls is None:
                                st.stop()
                            param_sheet = next((s for s in xls.sheet_names if "RAW_TYP" in s.upper() or "RAW_CORNERS" in s.upper()), None)
                            if param_sheet:
                                df_param = xls.parse(param_sheet)
                                df_param.columns = [col.strip() for col in df_param.columns]
                                st.dataframe(df_param)

                                voltage_cols_param = [col for col in df_param.columns if col.lower().startswith('v')]
                                temperature_cols_param = [col for col in df_param.columns if col.lower() == 'temp']

                                if voltage_cols_param and temperature_cols_param:
                                    selected_voltage_param = st.selectbox("Select Voltage Column for Parameter Data", voltage_cols_param, index=0)

                                    df_param['Temp_Voltage'] = df_param[temperature_cols_param[0]].astype(str) + '/' + df_param[selected_voltage_param].astype(str)

                                    y_axis_param = st.selectbox("Select Y-Axis for Parameter Data", df_param.columns)
                                    if y_axis_param:
                                        bubble_sizes_param = calculate_bubble_sizes(df_param, ['Temp_Voltage'], y_axis_param)

                                        fig_param = go.Figure()
                                        fig_param.add_trace(go.Scatter(
                                            x=df_param['Temp_Voltage'],
                                            y=df_param[y_axis_param],
                                            mode='markers',
                                            marker=dict(
                                                size=bubble_sizes_param,
                                                color='blue',
                                                opacity=0.7,
                                                line=dict(width=1, color='black')
                                            ),
                                            name=f"{y_axis_param} vs Temp/Voltage",
                                            
                                        ))

                                        fig_param.update_layout(
                                            xaxis_title='Temperature / Voltage',
                                            yaxis_title=y_axis_param,
                                            height=600,
                                            margin=dict(l=50, r=50, t=50, b=120),
                                            title=f"{y_axis_param} vs Temp/Voltage (Parameter: {st.session_state.selected_param_raw})"
                                        )
                                        st.plotly_chart(fig_param, use_container_width=True)

                            if st.button("Back to Summary", key="back_from_param_btn", help="Go back to Summary View"):
                                st.session_state.data_view = "summary"
                        else:
                            st.error(f"No file named {parameter_file_name} found in {specific_raw_folder}.")
                    else:
                        st.error(f"No folder named {specific_raw_folder} found in the Summary folder.")

                if st.button("Back to Summary", key="back_from_raw_btn_2", help="Go back to Summary View"):
                    st.session_state.data_view = "summary"








