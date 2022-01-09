#%% ############# Import & preprocess data #############

##  Import numpy & pandas to environment
import numpy as np
import pandas as pd

#%% Read the .csv file
df = pd.read_csv('CM4110_Survey.csv')

#%% Expore the column names
print(df.columns)
# Notice some column titles are very long, 
# so I will change them for Q1, Q2, etc...

#%% First, I create an empty dictionary to store the original questions
questions = {}
counter = 1

## Then, I do a for loop
for i in df.columns:
    if ' ' in i: # If there is a space then the title is long
        questions.update({i:'Q'+str(counter)})
        counter+=1
df = df.rename(columns=questions)
print(df)

#%% Explore the values in the "occupation" column
# See each entry
print(df['Occupation'])
# See all possible entries
print(set(df['Occupation']))

#%% Substitute data
# Substitute lecturer for staff
df = df.replace('Lecturer','Staff')

#%% Substitute non-academic for other
df = df.replace(('Housewife','Pensioner','Driver'),'Other')

#%% Verify change
print(set(df['Occupation']))

#%% Check the type of each column
print(df.dtypes)
# For "which design is the best" (Q11) answer should NOT be integer
# since these numbers correspond to the design names
# I must change them to objects before continuing

#%%
df['Q11'] = df['Q11'].astype('object')

## Now check again
print(df.dtypes)

#%% Create a sub-dataset only for students
df_students = df[df['Occupation']=='Student']

#%% Reset index
df_students = df_students.reset_index()

#%% Do the same for staff and others
df_staff = df[df['Occupation']=='Staff'].reset_index()
df_other = df[df['Occupation']=='Other'].reset_index()







#%% ############## Descriptive Statistics ################

##  Get the basic statistics
df_desc = df.describe() # only for numerical!
print(df_desc)
## There are some initial observations:
# 1. Quartiles are only infomrative for age, Q3, Q4, Q7 and Q8
# 2. There is an odd max for Q8 (780!)

#%%  First let's locate the "weird" entry
print(df[df['Q8']>=780]) # It's in index 11

#%%  What to do?
# a. Erase it
# b. Substitute it
# c. Put a nan
# Here I apply option c
df.iloc[11] = df.iloc[11].replace(780,np.nan)

#%%  And now I get statistics again
df_desc = df.describe()
print(df_desc)

#%%  Data has changed in the original DB for a staff member
# So lets create again `df_staff`
df_staff = df[df['Occupation']=='Staff'].reset_index()

#%%  Lets get statistics as well for students, staff & others
print('--------------------------Student Statistics--------------------------')
df_students_desc = df_students.describe()
print(df_students_desc)
print('---------------------------Staff Statistics---------------------------')
df_staff_desc = df_staff.describe()
print(df_staff_desc)
print('---------------------Other Occupation Statistics---------------------')
df_other_desc = df_other.describe()
print(df_other_desc)

#%%  Maybe you want to explore CORRELATION between two columns
# For example age and Q3 (colour scheme liking for D1)
# You can do this with the following command
print(np.corrcoef(df['Age'],df['Q4']))
# The result is -0.09, meaning that there is almost
#  no correlation. If you get
# values close to 1 or -1 in the top-right or the bottom left,
# then there is a high positive/negative correlation, but
#  as the number reduces, so does the correlation.







#%% ################### Plots ###################

#%%  Import matplotlib.pyplot, the most popular plotter in Python
import matplotlib.pyplot as plt
plt.xkcd() # This creates a "pencil-style" template for the plots

#%% Scatterplot to explore relation between Q7 & Q8
# First create three scatterplots, one for each occupation
# c is colour and s is size
# it is common to multiply the s so that differences are larger
students = plt.scatter(df_students['Q7'],df_students['Q8'],c='b',s=df_students['Age']*5)
staff = plt.scatter(df_staff['Q7'],df_staff['Q8'],c='g',s=df_staff['Age']*5)
other = plt.scatter(df_other['Q7'],df_other['Q8'],c='r',s=df_other['Age']*5)
## Then create a legend
plt.legend((students,staff,other),['Students','Staff','Others'],loc='upper right')
## Finally put labels to the axis and show
plt.xlabel('Partners found in D1')
plt.ylabel('Partners found in D2')
## Add some white space below the x axis
plt.gcf().subplots_adjust(bottom=0.15)
## Save the plot as a png image
plt.savefig('scatter.png')
## Plot the image in the console
plt.show()

#%% Pie/histogram chart to explore categoricals
# For instance by sex (create the two corresponding sub-dataframes)
df_male = df[df['Sex']=='M']
df_female = df[df['Sex']=='F']

#%% Select a question (so that I don't change a lot of things in the code)
questionplt = 'Q2'

#%% then create a subplot (i.e. a plot with two spaces inside)
fig,pie =  plt.subplots(1,2,figsize=(15,7))
## Do the two plots with the `value_counts` function
## Since no female answered "Never", we have to add this to the count!
pie[0].pie(df_male[questionplt].value_counts(),labels=set(df_male[questionplt]),autopct='%1.1f%%')
pie[1].pie(pd.concat([df_female[questionplt].value_counts(),pd.Series(data={'Never': 0}, index=['Never'])]),labels=set(df_male[questionplt]),autopct='%1.1f%%')
## Insert subtitles and titles
pie[0].set_title('Male')
pie[1].set_title('Female')
## With the following line, I get the actual question from the `questions` dictionary
# to put it as the plot title
fig.suptitle(list(questions.keys())[list(questions.values()).index(questionplt)])
## Save the plot as a png image
plt.savefig('pie.png')
## Plot the image in the console
plt.show()







#%% ################### Final Comments ###################
## MISSING VALUES
# When you do surveys, you risk having missing values
# You can either force people to answer all questions
# or deal with these missing values after preprocessing
# There are functions such as "fillna" that can help
# More info:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html