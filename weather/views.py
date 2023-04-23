from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=iperia;&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    
    err_msg = ''
    message = ''
    message_class = ''


    if request.method == 'POST':
        form = CityForm(request.POST)


        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r= requests.get(url.format(new_city)).json()
                if r['cod']== 200:
                    form.save()
                else:
                    err_msg = 'City does not exist!' 
            else:
                err_msg = 'City already exist in list!'    
        if err_msg:
                message = err_msg
                message_class = 'is-danger'
        else:
                message = 'City added sucessfully!'   
                message_class = 'is-success'

    print(err_msg)
    form = CityForm()
        
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        
        r= requests.get(url.format(city)).json()


        city_weather = {
        'city': city.name,
        'temperature' :r['main']['temp'],
        'ftemperature' :r['main']['feels_like'],
        'description': r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
        'country': r['sys']['country'], 
        }
        weather_data.append(city_weather)
    
     
    context = {
        'weather_data':weather_data,
        'form':form,
        'message' : message,
        'message_class' : message_class
     }
    return render(request,'weather/home.html',context)
        
def delete_city(request, city_name):
     City.objects.get(name=city_name).delete()
     return redirect('home')