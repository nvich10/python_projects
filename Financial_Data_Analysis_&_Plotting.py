def noah_q1 () :
  #import necessary libraries
  import pandas as pd
  import regex as re
  import matplotlib.pyplot as plt
  import seaborn as sns
  import numpy as np

  #extract SP500 prices
  def convert_lists_dict(averageS500_list, averageCPI_list) :
    convertSP500 = list()
    convertCPI = list()

    for value in averageS500_list:
      convertSP500.append(value[1])

    for value in averageCPI_list:
      convertCPI.append(value[1])

    years.append(2017)

    return convertSP500, convertCPI

  #percent of change in average S&P price from year before
  def percents_S500() :
    counter = 0
    percents_S500 = list()
    years = list()
    for index in averageS500_list :
      try :
        counter += 1
        hold_before_S500 = averageS500_list[counter - 1] #holds value before true index placement
        hold_past_S500 = averageS500_list[counter] #holds value of true index placement

        percent_diff_S500 = (hold_past_S500[1] / hold_before_S500[1]) - 1     #calculates % change in price from year before

        percents_S500.append(percent_diff_S500)
        years.append(int(hold_past_S500[0]))

      except IndexError :
        continue

    return percents_S500, years

  #percent of change in average CPI from year before
  def percents_CPI() :
    counter = 0
    percents_CPI = list()
    for index in averageCPI_list :
      try :
        counter += 1
        hold_before_CPI = averageCPI_list[counter - 1]  #same structure as SP500 calculation of % change
        hold_past_CPI = averageCPI_list[counter]

        percent_diff_CPI = (hold_past_CPI[1] / hold_before_CPI[1]) - 1

        percents_CPI.append(percent_diff_CPI)

      except IndexError :
        continue

    return percents_CPI




  #load data into pandas
  data_df = pd.read_csv('sp500_index_data.csv')

  #gather the average change in CPI and average change in S&P
  years = len(data_df) / 12 #amount of years included in the df (CPI and SP500 have same length)

  averageCPI_list = list()
  averageS500_list = list()

  x = 0  #our index holder
  is_twelve = 1
  total_CPI = 0
  total_S500 = 0
  for line in data_df.index:
    if x == 1764 : #once we get to the most recent complete year, break
      break


    total_CPI += data_df['Consumer Price Index'][x]   #running totals for the years
    total_S500 += data_df['SP500'][x]

    if is_twelve == 12 :
      is_twelve = 0
      average_CPI = total_CPI / 12      #find averages for the years
      average_S500 = total_S500 / 12

      year = data_df['Date'][x]
      extraction = r'\b\d{4}\b'     #extract the year
      year = re.search(extraction, year).group()


      averageCPI_list.append([year, average_CPI])    #storing list of lists with year : values as key-value pairs
      averageS500_list.append([year,average_S500])

      total_CPI = 0
      total_S500 = 0
      average_CPI = 0
      average_S500 = 0
      year = ''


    x += 1  #holds our index placement
    is_twelve += 1  #tracks when we hit 12 months in the dataset

  percents_SP500, years = percents_S500()
  percents_CPI = percents_CPI()

  start = len(years)
  start -= 50   #only access past 50 years
  percents_dict = {
      'Years' : years[start:],
      'SP500' : percents_SP500[start:],
      'CPI' : percents_CPI[start:]
  }
  dataframe_yearly_percent = pd.DataFrame.from_dict(percents_dict)


  start = len(years)
  start -= 50
  SP500_values, CPI_values = convert_lists_dict(averageS500_list, averageCPI_list)
  averages_dict = {
      'Years' : years[start:],
      "SP500" : SP500_values[start:],
      "CPI" : CPI_values[start:]

  }

  dataframe_yearly_avg = pd.DataFrame.from_dict(averages_dict)


  #PLOTTING
  plt.figure(figsize = (20,5))

  plt.subplot(1,2,1)
  correlation_percent = dataframe_yearly_percent['CPI'].corr(dataframe_yearly_percent['SP500'])    #find correlation between values, add to title
  sns.regplot(data = dataframe_yearly_percent, x = 'CPI', y = 'SP500').set(title=f'Correlation Between CPI & S&P500 Yearly % Change - (Corr. {correlation_percent:.3f})')

  plt.subplot(1,2,2)
  correlation_avg = dataframe_yearly_avg['CPI'].corr(dataframe_yearly_avg['SP500'])
  sns.regplot(data = dataframe_yearly_avg, x = 'CPI', y = 'SP500').set(title=f'Correlation Between CPI & S&P500 Yearly Average Value - (Corr. {correlation_avg:.3f})')



  #plot twin y-axis graph with shared x-axis. Helps visualize relationship over time.
  ax = dataframe_yearly_percent.plot(x='Years', y='SP500', legend=False)
  ax2 = ax.twinx()
  dataframe_yearly_percent.plot(x='Years', y='CPI', ax=ax2, legend=False, color='r')
  ax.figure.legend()
  ax.set_ylabel('SP500')
  ax2.set_ylabel('CPI')
  plt.title('Percent Change in S&P500 and CPI Over Time')
  plt.show()

  ax = dataframe_yearly_avg.plot(x='Years', y='SP500', legend=False)
  ax2 = ax.twinx()
  dataframe_yearly_avg.plot(x='Years', y='CPI', ax=ax2, legend=False, color='r')
  ax.figure.legend()
  ax.set_ylabel('SP500')
  ax2.set_ylabel('CPI')
  plt.title('S&P500 and CPI Over Time')
  plt.show()


def noah_q2() :
  from fredapi import Fred
  fred = Fred(api_key='*******************') #key access for FRED API
  import pandas as pd
  import matplotlib.pyplot as plt


  def dataframes (GNP_dict, SP500_dict) :
    df_GNP = pd.DataFrame.from_dict(GNP_dict)     #build our new dataframes
    df_SP500 = pd.DataFrame.from_dict(SP500_dict)
    return df_GNP, df_SP500

  GNP = fred.get_series('GNP') #get data from FRED api as a series

  SP500 = fred.get_series('SP500')


  #take out values, convert to dataframe
  years_GNP = GNP.index
  start = len(years_GNP) - 40
  GNP_values = GNP.values

  years_SP500 = SP500.index
  daily_SP500 = SP500.values


  GNP_dict = {
      'Years_GNP' : years_GNP[start:], #first quarter of 2013 to last quarter of 2022. SP500 only has prices for last 10 years, so we match GNP timeline.
      'GNP' : GNP_values[start:],
  }
  SP500_dict = {
      'Years_SP500' : years_SP500,
      'SP500' : daily_SP500
  }

  df_GNP, df_SP500 = dataframes(GNP_dict, SP500_dict)

  #PLOTTING
  #plotting twin y-axis graph with shared x-acis to show relationship over time
  plt.figure(figsize = (20,5))

  ax = df_SP500.plot(x='Years_SP500', y='SP500', legend = False)
  ax2= ax.twinx()
  df_GNP.plot(x='Years_GNP', y='GNP', ax=ax2, legend=False, color='r')
  ax.figure.legend()
  ax2.set_ylabel('GNP (in thousands of billions)')
  ax.set_ylabel('S&P (in thousands)')
  ax.set_xlabel('Years')
  correlation_percent = df_SP500['SP500'].corr(df_GNP['GNP'])   #find correlation between GNP and SP500 over past decade
  plt.title(f'S&P500 and GNP Over Time (r: {correlation_percent})')
  plt.show()


def noah_q3() :
  from fredapi import Fred
  key = '***************' #key access for FRED API
  import pandas as pd
  import matplotlib.pyplot as plt
  import requests
  from bs4 import BeautifulSoup
  import urllib.request
  import regex as re
  import numpy as np
  start_date = '2013-01-01' #want data for past decade from FRED API
  end_date = '2023-08-08'

#get subset dataframe from SP500 JSON
  def get_subset (key, start_date, end_date) :
    seriesID = 'SP500'
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={seriesID}&api_key={key}&file_type=json" + \
          f"&observation_start={start_date}&observation_end={end_date}&units=lin"

    SP500 = requests.get(url)
    SP500_json = SP500.json()  #FRED will return SP500 data in JSON which we convert to a dataframe below

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(SP500_json['observations'])

    # Rename columns for clarity
    df.rename(columns={'date': 'Date', 'value': 'Value'}, inplace=True)


    #re-arrange data in columnds for plotting purposes. We want dates and values in ascending order from L-R on the plot
    df['Date'] = df['Date'].iloc[::-1].reset_index(drop=True)
    df['Value'] = df['Value'].iloc[::-1].reset_index(drop=True)
    df_subset = df.iloc[::91, :] #creating a subset dataframe with every 91 value. 91 represents the amount of days per quarter in a year

    df_subset = df_subset.iloc[::-1].reset_index(drop=True)
    df_subset = df_subset.drop(22) #drop a value that was causing error. Value was a '.' instead of a SP500 price
    return df_subset


  def convert_SP500_float (df_subset) :
    #convert SP500 dataframe into legible float
    years_SP500 = list()
    date_list = df_subset['Date'].tolist()  #extract date column into list
    for value in date_list :
      pattern = r'^(\d{4})-\d{2}-\d{2}$' #extract years from the date format
      match = re.search(pattern, value)
      x = match.group(1)
      years_SP500.append(int(x))  #add extracted year into years_SP500 list

    values_SP500 = list()
    value_list = df_subset['Value'].tolist()  #extract SP500 prices into list and convert to float. Append to values_SP500 list
    for value in value_list :
      x = float(value)
      values_SP500.append(int(x))

    return years_SP500, values_SP500

  #webscrape for the data we need
  def webscrape (soup) :
    data = {} #holds prices of US Cruse Oil FPP with their decade. Data stored as key : list (decade : prices)

    for row in soup.find_all('tr'): #find all tr tags
        cells = row.find_all('td') #find rows with td tags
        if cells and len(cells) > 1:
            year = cells[0].text.strip() #extract year
            if year == "2010's" or year == "2020's": #only extract decades that can be used in correlation with SP500 timeline (past decade)
                try:
                    prices = [float(cell.text.strip()) if cell.text.strip() != '' else None for cell in cells[1:]] #extract prices with an exception if there is no value
                    data[year] = prices
                except ValueError:
                    pass
    return data


  #webscrape oil data from web
  url = 'https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=f000000__3&f=a'
  response = requests.get(url)
  mystr = response.content #holds html
  soup = BeautifulSoup(mystr, 'html.parser') #use beautiful soup to parse html
  data = webscrape(soup)


  years = list()
  values = list()
  year_counter = 2010

  #create years to match prices that exist in data{}
  for value in data.values() :
    for item in value:
      years.append(year_counter)
      values.append(item)

      year_counter += 1

  #only use years from past decade (2013-2023)
  oil_dict = {
      'Years' : years[3:13],
      'US FPP' : values[3:13],

  }


  oil_df = pd.DataFrame.from_dict(oil_dict)
  df_subset = get_subset(key, start_date, end_date)
  years_SP500, values_SP500 = convert_SP500_float(df_subset)


  SP500_dict = {
      'Years' : years_SP500,
      'SP500 Prices' : values_SP500
  }


  df_SP500 = pd.DataFrame.from_dict(SP500_dict)

  #PLOTTING
  # Plot both dataframes on the same x-axis with a secondary y-axis
  plt.figure(figsize=(20,5))

  ax = oil_df.plot(x='Years',y='US FPP',legend=False)
  ax2=ax.twinx()
  df_SP500.plot(x='Years',y='SP500 Prices', ax=ax2, legend=False, color='r')
  ax.figure.legend()
  ax.set_ylabel('US Crude Oil First Purchase Prices')
  ax.set_xlabel('Years')
  ax2.set_ylabel('SP500 Prices')
  correlation_percent = df_SP500['SP500 Prices'].corr(oil_df['US FPP'])  #correlation between US Crude Oil FPP and SP500 prices over past decade
  plt.title(f'US Crude Oil FPP and S&P 500 Over Time\n(r: {correlation_percent:.3f})')
  plt.show()

