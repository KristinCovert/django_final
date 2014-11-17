from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.gis.geos import Point
from .models import FruitLocation
from .forms import AddFruitForm

@login_required
def add_fruit(request):

    if request.method == 'POST':
        form = AddFruitForm(request.POST)
        if form.is_valid():
            new_point = FruitLocation()
            cd = form.cleaned_data
            coordinates = cd['coordinates'].split(',')
            new_point.geom = Point(float(coordinates[0]), float(coordinates[1]))
            new_point.fruit_variety = cd['Fruit Variety']

            new_point.save()

            return render_to_response('AddFruit_success.html')

        else:
            return render_to_response('AddFruit_error.html')
    else:
        form = AddFruitForm()

    token = {}
    token.update(csrf(request))
    token['form'] = AddFruitForm()

    return render_to_response('fruitlocations/add_fruit.html', token)