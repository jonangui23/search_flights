from django.shortcuts import render, HttpResponse
import pandas as pd
from datetime import datetime

df = pd.read_csv('/Users/jonangui23/Desktop/itineraries.csv')
df['flightDate'] = pd.to_datetime(df['flightDate'], errors = 'coerce')
#filter for nonstop
df = df[df['isNonStop'] == True]
#adding in arrival date and time
df['segmentsArrivalTime'] = pd.to_datetime(df['segmentsArrivalTimeEpochSeconds'], unit = 's', utc = True)    
#creating seperate columns for date and time
df['date'] = df['segmentsArrivalTime'].dt.date
df['time'] = df['segmentsArrivalTime'].dt.time

#things to do:
#Include return date and time travel and price. Make sure to sort by the price before doing head to return the top 10 cheapest flights.
# Also make it search within months to find the cheapest months to travel
def flight_search(request):
    # Logic to handle flight search (example)
    origin = destination = start_date = end_date = None
    results = None
    
    if request.method == "POST":
      origin = request.POST.get('origin')
      destination = request.POST.get('destination')
      start_date = request.POST.get('start_date')
      end_date = request.POST.get('end_date')

    filtered_df = df 
    
    if origin:
        filtered_df = filtered_df[filtered_df['startingAirport'].str.contains(origin, case=False, na=False)]
    if destination:
        filtered_df = filtered_df[filtered_df['destinationAirport'].str.contains(destination, case=False, na=False)]
    if start_date:
        filtered_df = filtered_df[filtered_df['flightDate'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['flightDate'] <= end_date]

    #select relevant columns to display
    filtered_df = filtered_df[['startingAirport', 'destinationAirport', 'flightDate','date', 'time', 'totalFare']]

    #sort by price in ascending order
    filtered_df = filtered_df.sort_values(by = 'totalFare', ascending = True)

    #display top 10
    filtered_df = filtered_df.head(10)
    
    # convert the filtered dataframe to a list of dictionaries
    results = filtered_df.to_dict  (orient='records')

    return render(request, 'results.html', {
        'origin': origin,
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date, 
        'results': results
    })

def user_input(request):

    return render(request, 'userInput.html' )
