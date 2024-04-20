import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Load predefined CSV data
@st.cache
def load_data():
    return pd.read_csv("./scraped_data.csv")

def draw_line_with_footballs():

    st.write(f"Event data on the match")
    # Plotting
    fig, ax = plt.subplots(figsize=(8, 3))

    # Draw line of length 10
    ax.plot([0, 10], [0, 0], color='black')

    # Load football icon
    football_icon = mpimg.imread('./football_icon.png')  # Load your football icon
    icon_height = 0.5  # Set the height of the football icon
    icon_width = icon_height * football_icon.shape[1] / football_icon.shape[0]  # Calculate width maintaining aspect ratio

    # Add football icons above and below the line
    ax.imshow(football_icon, extent=(5 - icon_width / 2, 5 + icon_width / 2, 0.5, 1.5), aspect='auto')
    ax.imshow(football_icon, extent=(5 - icon_width / 2, 5 + icon_width / 2, -1.5, -0.5), aspect='auto')

    ax.set_xlabel('Position')
    ax.set_title('Football Line')
    ax.set_xlim(0, 10)
    ax.set_ylim(-2, 2)
    ax.set_xticks(range(11))
    ax.set_yticks([])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Display the plot in Streamlit
    st.pyplot(fig)

def page_about():
    st.write("This is the About page.")

# Define the sidebar
def sidebar():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "About"])
    return selection


# Main function to run the Streamlit app

def page_home():
    st.title("Win Probabilities")

    data = load_data()

    # Create dropdown for match keys
    selected_match_key = st.selectbox("Select Match Key", data['match_key'].unique())

    # Filter data based on selected match key
    filtered_data = data[data['match_key'] == selected_match_key]

    # Convert timestamp to datetime
    filtered_data['timestamp'] = pd.to_datetime(filtered_data['time_of_day'])

    # Information text
    st.write(f"Plotting win counts for Match Key: {selected_match_key}")

    # Dynamically select team name
    if not filtered_data.empty:
        selected_team_A = filtered_data['name_team_A'].iloc[0]
        #st.write(f"Selected Team A: {selected_team_A}")
        selected_team_B = filtered_data['name_team_B'].iloc[0]
        #st.write(f"Selected Team B: {selected_team_B}")
    else:
        st.write("No data available for selected match key.")

    # Plotting

    colors = ["navy", "lightgray", "darkred"]

    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_win_team_A'], color=colors[0], label=("Win " + selected_team_A))
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_draw'], color=colors[1], label="Draw")
    plt.plot(filtered_data['time_of_day'], filtered_data['prob_win_team_B'], color=colors[2], label=("Win " + selected_team_B))
    plt.xlabel('Time')
    plt.ylabel('Win probability')
    plt.title('Outcome probability of ' + selected_team_A + ' vs. ' + selected_team_B +' over time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    st.pyplot()


    # Call the function to draw the line with football icons
    #draw_line_with_footballs()


def main():
    st.title("Streamlit App with Sidebar")

    # Get the selection from the sidebar
    selection = sidebar()

    # Display content based on the selection
    if selection == "Home":
        page_home()
    elif selection == "About":
        page_about()

if __name__ == "__main__":
    main()