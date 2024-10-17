# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in tour custom smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie')

#get a snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients=st.multiselect('Choose upto 3 fruits'
    , my_dataframe
)



if ingredients:
    
   ingredients_string =''
   for fruit_choosen in ingredients:
       ingredients_string += fruit_choosen + ' '
       
   st.write(ingredients_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

   
   #st.write(my_insert_stmt)
   #st.stop
    
   time_to_insert = st.button('Submit Order') 

   if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

fruityvice_response = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyDGlAry0tpNXlgpMJyouELBKkxI71YFETI&cx=017576662512468239146:omuauf_lfve&q=lectures")
st.text(fruityvice_response)
