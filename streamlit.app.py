# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched  # Import when_matched

# Initialize the Snowflake session
session = get_active_session()

# Filter orders that are not yet filled (ORDER_FILLED = FALSE)
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).collect()

# Display the filtered data (optional)
st.dataframe(my_dataframe)

# Create an editable DataFrame
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset,(og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']),[when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])
            
            st.success('Order(s) updated!', icon='👍')
        except:
            st.write('Something went wrong')

else:
    st.success('There are no pending orders right now', icon='👍')
    # Perform the merge operation
   
    
   # st.success('Merge operation completed successfully!', icon='👍')
