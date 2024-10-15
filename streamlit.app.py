from snowflake.snowpark import Session
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Snowflake connection details
connection_parameters = {
    "account": "<your_account>",
    "user": "<your_user>",
    "password": "<your_password>",
    "role": "<your_role>",
    "warehouse": "<your_warehouse>",
    "database": "<your_database>",
    "schema": "<your_schema>"
}

# Create a new session
session = Session.builder.configs(connection_parameters).create()

# Capture the name for the smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

# Get the fruit options from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()

# Convert Snowflake Rows to a list of fruit names
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe]

# Create a multiselect widget for choosing fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list
)

# Check if the user has selected more than 5 ingredients
if len(ingredients_list) > 5:
    st.warning("You can only select up to 5 ingredients.")

if ingredients_list:
    # Concatenate fruit names into a single string
    ingredients_string = ' '.join(ingredients_list)  

    # Prepare the SQL insert statement to include both the ingredients and the name
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Display the SQL for debugging purposes
    st.write(my_insert_stmt)

    # Fetch fruit data using an API
    fruit_chosen = ingredients_list[0]  # Example, based on the first fruit
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Button to submit the order
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()  # Execute the insert query
        st.success('Your Smoothie is ordered!', icon="✅")
