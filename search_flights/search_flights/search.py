from django.shortcuts import render
from django.forms import FlightSearchForm
import requests
from bs4 import BeautifulSoup

def get_flights(origin, destination, start_date, end_date):
    """
    Scrape flight data from a publicly accessible flight aggregator website.
    """
    # Construct the URL based on the target website's parameters (example URL structure)
    url = (
        f"https://www.example-flight-aggregator.com/search?"
        f"origin={origin}&destination={destination}&depart={start_date}&return={end_date}"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    flights = []

    # Replace the following selectors with the actual structure of the website
    for flight_card in soup.select('.flight-card'):
        try:
            airline = flight_card.select_one('.airline-name').text.strip()
            price = flight_card.select_one('.price').text.strip().replace('$', '')
            departure_time = flight_card.select_one('.departure-time').text.strip()
            arrival_time = flight_card.select_one('.arrival-time').text.strip()
            link = flight_card.select_one('.booking-link')['href']

            flights.append({
                'airline': airline,
                'price': float(price),
                'departure': departure_time,
                'arrival': arrival_time,
                'link': link
            })
        except AttributeError:
            # Skip incomplete or malformed flight cards
            continue

    return flights

def sort_flights_by_price(flights):
    """
    Sort flights by price in ascending order.
    """
    return sorted(flights, key=lambda x: x['price'])

def flight_search(request):
    """
    Handles the flight search form and renders search results.
    """
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            flights = get_flights(origin, destination, start_date, end_date)
            sorted_flights = sort_flights_by_price(flights)

            return render(request, 'flights/results.html', {'flights': sorted_flights})
    else:
        form = FlightSearchForm()

    return render(request, 'flights/search.html', {'form': form})

