#!/usr/bin/env python
# coding: utf-8

# # Import software libraries

# In[1]:


# Import required libraries.
import sys           # Read system parameters.
import pandas as pd  # Manipulate and analyze data.
import sqlite3       # Manage SQL databases.

# Summarize software libraries used.
print('Libraries used in this project:')
print('- Python {}'.format(sys.version))
print('- pandas {}'.format(pd.__version__))
print('- sqlite3 {}'.format(sqlite3.sqlite_version))


# # Examine the database

# In[3]:


# Connect to SQLite database.
conn = sqlite3.connect('data/prod_sample.db')
conn


# In[12]:


# List all the tables in the database.
query='''SELECT * FROM online_retail_history orh
                   INNER JOIN stock_description sd
                   ON orh.StockCode=sd.StockCode 
    '''

users=pd.read_sql(query, conn)
users.head()



# # Read data from the `online_retail_history` table

# In[24]:


# Write the query to be executed that selects everything from the online_retail_history table.
query='''SELECT * 
         FROM online_retail_history'''





# Use the read_sql function in pandas to read a query into a DataFrame.

online=pd.read_sql(query, conn)

# Preview the first five rows of the data.

online.head()


# In[25]:


# Get the shape of the data.
online.shape


# # Read data from the `stock_description` table

# In[22]:


# Write the query to be executed that selects everything from the online_retail_history table.

query='''SELECT * 
         FROM stock_description'''






# Use the read_sql function in pandas to read a query into a DataFrame.

stock=pd.read_sql(query, conn)

# Preview the first five rows of the data.
stock.head()


# In[48]:


# Get the shape of the data.
stock.shape


# # Aggregate the `online_retail_history` and `stock_description` datasets

# In[50]:


# Write a query to aggregate the two datasets so that you have the stock descriptions as well as the stock code.

query='''SELECT  * FROM online_retail_history orh
                   LEFT JOIN stock_description sd
                   ON orh.StockCode=sd.StockCode 
    '''








# Use the read_sql function in pandas to read a query into a DataFrame.

combine=pd.read_sql(query, conn)

# Preview the first five rows of the data.

combine.head()


# In[55]:


# Get the shape of the data.

combine.shape


# # Identify and fix corrupt or unusable data

# In[52]:


# Check the value counts of the "Description" field.
combine.shape


# In[57]:


# Remove rows where "Description" is just a question mark (?).
combine_cleaned= combine[combine.Description != '?']

combine_cleaned









# Preview the first five rows of the data.
combine_cleaned.shape


# # Identify and remove duplicates

# In[60]:


# Identify all duplicated data.
combine_cleaned_2=combine_cleaned.copy()
duplicated_data = combine_cleaned_2[combine_cleaned_2.duplicated(keep = False)]

print('Number of rows with duplicated data:',
       duplicated_data.shape[0])


# In[61]:


# Print the duplicated data.
duplicated_data


# In[75]:


# Remove duplicates based on all columns
combine_cleaned_final = combine_cleaned_2[~combine_cleaned_2.duplicated()]

# Now, remove duplicates based on the 'CustomerId' column
combine_cleaned_final = combine_cleaned_final.drop_duplicates(subset=['CustomerID'])

# Check the shape of the resulting DataFrame
print(combine_cleaned_final.shape)

# Preview the first five rows of the data
print(combine_cleaned_final.head())


# # Correct date formats

# In[76]:


# Get the data types for every column in the DataFrame.
combine_cleaned_final.info()


# In[79]:


# Convert "InvoiceDate" to a "%Y-%m-%d" datetime format.
combine_cleaned_final_2 = combine_cleaned_final.copy()

combine_cleaned_final_2['InvoiceDate'] = pd.to_datetime(combine_cleaned_final_2['InvoiceDate'],
              format = '%Y-%m-%d')




# In[81]:


# Get the data types for every column in the converted DataFrame.
combine_cleaned_final_2.info()


# # Examine the table before finishing

# In[82]:


# Preview the first five rows of the data.

combine_cleaned_final_2.head()


# # Load the dataset into a pickle file

# In[83]:


# Save the dataset as a pickle file named online_history_cleaned.pickle.

combine_cleaned_final_2.to_pickle('online_cleaned.pickle')


# In[84]:


# Close any connections to the database.
conn.close

