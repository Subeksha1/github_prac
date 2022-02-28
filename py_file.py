#!/usr/bin/env python
# coding: utf-8

# #  Web scraping a Rotten Tomatoes page

# ## Import the relevant libraries

# This exercise is going to use web scraping techniques to extract data and store in a data frame using Pandas. The data that will needed to be included in the data frame will be as follows:
# - Title
# - Year
# - Score
# - Adjusted score
# - Director
# - Cast
# 
# As an exension task, then the following can be added also:
# 
#  - consensus
#  - synopsis
#  
# There will be placeholder headers and some notes to assist you but feel free to delete any of that and work in your own way on this. The completed data frame should be exported as a CSV at the end of the activity. You will need to use the pandas documentation to help with this.
# https://pandas.pydata.org/docs/
# 

# In[1]:


# load packages
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


# Define the URL of the site
base_site = "https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now"


# ## Check to see if the request was successful

# In[3]:


# sending a request to the webpage
response = requests.get(base_site)
response


# In[4]:


# get the HTML from the webpage
html_soup = response.content


# ## Choosing a parser

# ### lxml

# In[5]:


# convert the HTML to a BeatifulSoup object
soup = BeautifulSoup(html_soup, 'lxml')


# In[6]:


# Exporting the HTML to a file
with open('Rotten_tomatoes_page_2_LXML_Parser.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))


# ### Re: Parser choice

# In[7]:


# Beautiful Soup ranks the lxml parser as the best one.

# If a parser is not explicitly stated in the Beautiful Soup constructor,
# the best one available on the current machine is chosen.

# This means that the same piece of code can give different results on different computers.


# ## Finding an element containing all the data

# In[8]:


# Right click on the webpage and choose INSPECT to find out the divs of the part of the page that you would like to scrape.
# 
#Find all div tags on the webpage containing the information we want to scrape
divs = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
divs
#panel-body content_body


# # Extracting the title, year and score of each movie

# In[9]:


# The title, year and score of each movie are contained in the 'h2' tags


# In[10]:


# choose the first film to get a better idea of how the data is structured - use list indexing to achieve this.
divs[0].find("h2")


# In[11]:


# Extracting all 'h2' tags
headings = [div.find("h2") for div in divs]
headings


# In[12]:


# Inspecting the text inside the headings
[heading.text for heading in headings]


# In[13]:



#inspect one heading to see if there is a way to distinguish between them
headings[0]


# In[14]:



# The movie title is in the 'a' tag
# The year is in a 'span' with class 'start-year'
# The score is in a 'span' with class 'tMeterScore'


# ## Title

# In[15]:


# Let's check all heading links
[heading.find('a') for heading in headings]


# In[16]:


# Obtaining the movie titles from the links
movie_names = [heading.find('a').string for heading in headings]
movie_names


# ## Year

# In[17]:


# Filtering only the spans containing the year
[heading.find("span", class_ = 'start-year') for heading in headings]


# In[18]:


# Extracting the year string
years = [heading.find("span", class_ = 'start-year').string for heading in headings]
years


# In[19]:


years[0]


# ### Removing the brackets

# In[20]:


# Use the strip method to remove the parantheses


# In[21]:


# code for removing parantheses
years[0].strip('()')


# In[22]:


# Updating years with stripped values
years = [year.strip('()') for year in years]
years


# In[23]:


# Converting all the strings to integers
years = [int(year) for year in years]
years


# ## Score

# In[24]:




# Filtering only the spans containing the score
[heading.find("span", class_ = 'tMeterScore') for heading in headings]


# In[25]:


# Extracting the score string
scores = [heading.find("span", class_ = 'tMeterScore').string for heading in headings]
scores


# In[26]:


# Removing the '%' sign
scores = [s.strip('%') for s in scores]
scores


# In[27]:


# Converting each score to an integer
scores = [int(s) for s in scores]
scores


# # Extracting the rest of the information

# ## Critics Consensus

# In[28]:


# The critics consensus is located inside a 'div' tag with the class 'info critics-consensus'
# This can be found inside the original 'div's we scraped
divs


# In[29]:


# Getting the 'div' tags containing the critics consensus
consensus = [div.find("div", {"class": "info critics-consensus"}) for div in divs]
consensus


# In[30]:


# Inspecting the text inside these tags
[con.text for con in consensus]


# In[31]:


# Every consensus starts with the string 'Critics Consensus: '
# There are a couple of ways to remove it from the final text


# ### Way #2: Inspecting the HTML

# In[32]:


consensus[0]


# In[33]:


# When inspecting the HTML we see that the common phrase ("Critics Consensus: ")
# is located inside a span element
# The string we want to obtain follows that


# In[34]:


# We can use .contents to obtain a list of all children of the tag
consensus[0].contents


# In[35]:


# The second element of that list is the text we want
consensus[0].contents[1]


# In[36]:


# We can remove the extra whitespace (space at the beginning) with the .strip() method
consensus[0].contents[1].strip()


# In[37]:


# Processing all texts
consensus_text = [con.contents[1].strip() for con in consensus]
consensus_text


# In[38]:


# In my opinion, this method is closer to the BeautifulSoup approach


# ## Directors

# In[39]:


# Extracting all director divs
directors = [div.find("div", class_ = 'director') for div in divs]
directors


# In[40]:


# Inspecting a div
directors[0]


# In[41]:


# The director's name can be found as the string of a link

# Obtaining all director links
[director.find("a") for director in directors]


# In[42]:


# We can use if-else to deal with the None value should one exist

final_directors = [None if director.find("a") is None else director.find("a").string for director in directors]
final_directors


# ## Cast info

# In[43]:


cast_info = [div.find("div", class_ = 'cast') for div in divs]
cast_info


# In[44]:


cast_info[0]


# In[45]:


# Each cast member's name is the string of a link
# There are multiple cast members for a movie


# In[46]:




# Obtain all the links to different cast members
cast_links = cast_info[0].find_all('a')
cast_links


# In[47]:


# Extract the names from the links
cast_names = [link.string for link in cast_links]
cast_names


# In[48]:


# OPTIONALLY: We can stitch all names together as one string

# This can be done using the join method
# To use join, pick a string to use as a separator (in our case a comma, followed with a space) and
# pass the list of strings you want to merge to the join method

cast = ", ".join(cast_names)
cast


# In[49]:


# Now we need to do the above operations for every movie

# We can either use a for loop (clearer), or
# use a nested list compehension (more concise)


# ### Using a for loop

# In[50]:


# Initialize the list of all cast memners
casting = []

# Just put all previous operations inside a for loop
for c in cast_info:
    cast_links = c.find_all('a')
    cast_names = [link.string for link in cast_links]
    
    casting.append(", ".join(cast_names)) # Joining is optional

casting


# In[51]:



# The adjusted scores can be found in a div with class 'info countdown-adjusted-score'
adj_scores = [div.find("div", {"class": "info countdown-adjusted-score"}) for div in divs]
adj_scores


# In[52]:


# Inspecting an element
adj_scores[0]


# In[53]:


# By inspection we see that the string we are looking for is the second child of the 'div' tag
adj_scores[0].contents[1]  # Note the extra whitespace at the end


# In[54]:


# Extracting the string (without '%' sign and extra space)
adj_scores_clean = [score.contents[1].strip('% ') for score in adj_scores]
adj_scores_clean


# In[55]:


# Converting the strings to numbers
final_adj = [float(score) for score in adj_scores_clean] # Note that this time the scores are float, not int!
final_adj


# ## Synopsis

# In[56]:


# Homework

# The synopsis is located inside a 'div' tag with the class 'info synopsis'
synopsis = [div.find('div', class_='synopsis') for div in divs]
synopsis


# In[57]:


# Inspecting the element
synopsis[0]


# In[58]:


# The text is the second child
synopsis[0].contents[1]


# In[59]:


# Extracting the text
synopsis_text = [syn.contents[1] for syn in synopsis]
synopsis_text


# # Representing the data in structured form

# ## Creating a Data Frame

# In[60]:


# A dataframe is a tabular data type, frequently used in data science

movies_info = pd.DataFrame()
movies_info  # The dataframe is still empty, we need to fill it with the info we gathered


# ## Populating the dataframe

# In[61]:


# Populating the dataframe

movies_info["Movie Title"] = movie_names
movies_info["Year"] = years
movies_info["Score"] = scores
movies_info["Adjusted Score"] = final_adj  # Homework
movies_info["Director"] = final_directors
movies_info["Synopsis"] = synopsis_text    # Homework
movies_info["Cast"] = cast
movies_info["Consensus"] = consensus_text

# Let's see how it looks
movies_info


# In[62]:


# By default pandas abbreviates any text beyond a certain length (as seen in the Cast and Consensus columns)

# We can change that by setting the maximum column width to -1,
# which means the column would be as wide as to display the whole text
pd.set_option('display.max_colwidth', -1)
movies_info


# ## Exporting the data to CSV (comma-separated values) and excel files

# In[63]:


# Write data to excel file
movies_info.to_excel("movies_info.xlsx", index = False, header = True)


# In[64]:


# or write data to CSV file
movies_info.to_csv("movies_info.csv", index = False, header = True)


# In[65]:


# Index is set to False so that the index (0,1,2...) of each movie is not saved to the file (the index is purely internal)
# The header is set to True, so that the names of the columns are saved


# In[ ]:




