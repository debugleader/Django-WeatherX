from django.shortcuts import render, redirect
from .models import City
import requests
from .forms import CityForm 

# Paste your API key.
API_KEY_VAR = ""

def index_name(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    error = ''
    msg = ''
    msg_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            count = City.objects.filter(name = new_city).count()
            if count == 0:
                r = requests.get(url.format(new_city, API_KEY_VAR)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error = "City doesn't exist in the world"
            else:
                error = 'City already posted down below!'

        if error:
            msg = error
            msg_class = 'is-danger'
        else:
            msg = 'City added successfully!..'
            msg_class = 'is-success'
    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    city_obj = []
    countero = 0
    for city in cities:
        countero += 1
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'].title(),
            'icon': r['weather'][0]['icon'],
            'humidity': r['main']['humidity'],
            'countero': countero,
        }
        weather_data.append(city_weather)
    context = {'weather_data' : weather_data, 'form' : form, 'msg' : msg, 'msg_class' : msg_class}
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('indexo')