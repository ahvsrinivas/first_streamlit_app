import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * from fruit_load_list")
          return my_cur.fetchall()
        
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)

#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))


#my_fruit_list = my_fruit_list.set_index('Fruit')
#fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.dataframe(fruits_to_show)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)
streamlit.header("Fruityvice Fruit Advice!")

def getfruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
   
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   if not fruit_choice:
       streamlit.error("please select a fruit to get info")
   else:
       back_from_function = getfruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
except URLError as e:
      streamlit.error()

#streamlit.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

streamlit.write('The user entered ', fruit_choice)

def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
          return "Thanks for adding " + new_fruit

fruit_choice1 = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
       back_from_function = insert_row_snowflake(fruit_choice1)
       streamlit.text(back_from_function)

#streamlit.stop()

#fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice1)
#streamlit.text(fruityvice_response)
#fruityvice_normalized1 = pandas.json_normalize(fruityvice_response1.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized1)
