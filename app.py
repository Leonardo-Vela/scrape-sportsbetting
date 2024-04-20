import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load predefined CSV data
@st.cache
def load_data():
    return pd.read_csv("./scraped_data.csv")

# Main function to run the Streamlit app
def main():
    st.title("CSV Data Plotter")

    data = load_data()

    # Create dropdown for match keys
    selected_match_key = st.selectbox("Select Match Key", data['match_key'].unique())

    # Filter data based on selected match key
    filtered_data = data[data['match_key'] == selected_match_key]

    # Convert timestamp to datetime
    filtered_data['timestamp'] = pd.to_datetime(filtered_data['time_of_day'])

    # Assign team names
    selected_team_A = filtered_data['name_team_A'][0]
    selected_team_B = filtered_data['name_team_B'][0]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_win_team_A'], label=("Win " + selected_team_A))
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_draw'], label="Draw")
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_win_team_B'], label=("Win " + selected_team_B))
    plt.xlabel('Timestamp')
    plt.ylabel('Win probability')
    plt.title('Outcome probability of ' + selected_team_A + ' vs. ' + selected_team_B +' over Time')
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot()

if __name__ == "__main__":
    main()