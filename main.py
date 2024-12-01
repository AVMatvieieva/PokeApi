import streamlit as st
import html
import pandas as pd
import matplotlib.pyplot as plt
from Api import fetch_data, abilities, pokemon_list, weight, height, image, abilities_url, ability_description, get_pokemon_stats

st.set_page_config(
        page_title="Pills UI Example",
        layout="wide",
    )
# Erstelle eine Seitenleiste für die Navigation im Projekt
def plot_stats(stats, pokemon_name):
    # Convert stats into a Pandas DataFrame
    df = pd.DataFrame(list(stats.items()), columns=["Stat", "Base Value"])
    df = df.sort_values("Base Value", ascending=True)  # Sort for better visual clarity

    # Define custom colors for the bars
    custom_colors = ['#FF9999', '#FFCC99', '#FFFF99', '#99FF99', '#99CCFF', '#CC99FF']  # Pastel palette

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 5), facecolor = None)  # Set the figure background
    bars = ax.barh(
        df["Stat"], df["Base Value"], 
        color=custom_colors[:len(df)], edgecolor="black"
    )  # Use custom colors and black borders

    # Add values to the bars
    for bar in bars:
        width = bar.get_width()  # Get the width of each bar (the value)
        ax.text(
            width + 2,  # Slightly offset from the end of the bar
            bar.get_y() + bar.get_height() / 2,  # Center vertically on the bar
            f"{int(width)}",  # Display the value as an integer
            va='center',  # Vertically align text to the center of the bar
            ha='left',  # Horizontally align text slightly to the right of the bar
            fontsize=10, color='black'
        )

    # Customize chart appearance
    #ax.set_title(f"{pokemon_name.capitalize()} Stats", fontsize=16, fontweight='bold')
    #ax.set_xlabel("Base Value", fontsize=12)
    #ax.set_ylabel("Stat", fontsize=12)
    ax.spines['top'].set_visible(False)  # Hide top border
    ax.spines['right'].set_visible(False)  # Hide right border
    ax.spines['left'].set_visible(False)  # Hide left border
    ax.spines['bottom'].set_color('black')  # Keep the bottom border for alignment
    ax.tick_params(axis='x', colors='black')  # Set x-axis tick colors
    ax.tick_params(axis='y', colors='black')  # Set y-axis tick colors
    plt.grid(axis="x", linestyle="--", alpha=0.5)  # Add a subtle grid for clarity
    plt.tight_layout()  # Adjust layout for better fitting
    
    return fig

st.sidebar.markdown(f"""
    <h1 style="color: #ff0000;">
        Pokemons
    </h1>
""", unsafe_allow_html=True)

if "last_input" not in st.session_state:
    st.session_state.last_input = None  # Speichern welches Element ist letzte

#Nach eingegebenen Name
input_name = st.sidebar.text_input('Name des Pokemons', 'ditto')

ability_des = {}

#Nach Multiselect Pokemons
selected_pokemons = st.sidebar.selectbox(
    "Hier kannst du ein Pokemon auswählen:",
    pokemon_list(),
)

#Prüfen, was sich geänderte
if input_name != st.session_state.last_input:
    st.session_state.last_input = input_name
    name = input_name
elif selected_pokemons != st.session_state.last_input:
    st.session_state.last_input = selected_pokemons
    name = selected_pokemons
else:
    # wenn nichts geänderte
    name = input_name


st.markdown(f"""
    <h1 style="color: #ffde00;">
        {name}
    </h1>
""", unsafe_allow_html=True)


# Daten von der API abfragen
data = fetch_data(name)

st.sidebar.json(data, expanded=True)

# Daten visualisieren
if data:
    
   
#Create 2 areas        
    col1, col2 = st.columns(2)    

    with col1:
        st.image(image(name),width=150 ) 
        
        st.markdown(f"""
        <h2 style="color: #ff0000;">
         Eigenschaften:
            </h2>
        """, unsafe_allow_html=True)
        
        for ability in abilities(data):
            ability_des = ability_description(ability, name)
    
            # Удаляем лишние пробелы и символы новой строки
            cleaned_ability_des = ability_des.strip().replace("\n", " ")  # Удаление переводов строки
            
            # Экранируем текст описания
            escaped_description = html.escape(cleaned_ability_des)
            
            # Формируем HTML с подсказкой
            tooltip_text = f"""
            <span style="text-decoration: underline; cursor: pointer;" title="{escaped_description}">
                {ability}
            </span>
            """
            
            # Отображаем текст в Streamlit
            st.markdown(tooltip_text, unsafe_allow_html=True)
            

    with col2:       
        
        st.markdown(f"""
        <h2 style="color: #ff0000;">
        Merkmalle:
        </h2>
        """, unsafe_allow_html=True)
        # Erstellen 2 Spalten
        col3, col4 = st.columns(2)
        with col3:
            st.write("Gewicht: ")
            st.write("Große:")
        with col4:    
            st.write(weight(name))
            st.write(height(name))   
            
        st.markdown(f"""
        <h2 style="color: #ff0000;">
        Base Stats for {name.capitalize()}:
        </h2>  """, unsafe_allow_html=True)
        
        stats = get_pokemon_stats(name)
        fig = plot_stats(stats, name)
        st.pyplot(fig)
        
        
else:
    st.write("Keine Daten verfügbar.")     

