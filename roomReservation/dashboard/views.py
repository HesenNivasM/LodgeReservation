from django.shortcuts import render, redirect
from .models import reservation
from datetime import datetime

# The dashboard with the dates
def index(request):
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    searchDate = str(day) + "-" + str(month) + "-" + str(year)
    data = reservation.objects.filter(date = searchDate)
    bookedRooms = []
    for datum in data:
        bookedRooms.append(datum.roomNumber)
    return render(request, 'dashboard/index.html', {
        'bookedRooms': bookedRooms
    } , content_type = 'text/html')

# To display the rooms and pass the room numbers
def rooms(request):     
    postData = request.POST.get("postData").split("-")
    day, month, year = postData
    request.session['day'] = day
    request.session['month'] = month
    request.session['year'] = year
    searchDate = str(day) + "-" + str(month) + "-" + str(year)
    data = reservation.objects.filter(date = searchDate)
    bookedRooms = []
    for datum in data:
        bookedRooms.append(datum.roomNumber)
    print(bookedRooms)
    return render(request, 'dashboard/rooms.html', {
        'day': day,
        'month': month,
        'year': year,
        'bookedRooms': bookedRooms
    } , content_type = 'text/html')

def book(request):
    # To get the first post when passing from rooms to book
    if request.method == "POST" and request.POST.get("postData"):
        roomNumber = request.POST.get("postData")
        request.session['roomNumber'] = roomNumber
        day = request.session.get("day")
        month = request.session.get("month")
        year = request.session.get("year")
        # Check whether the room is booked already
        searchDate = str(day) + "-" + str(month) + "-" + str(year)
        data = reservation.objects.filter(date = searchDate, roomNumber = roomNumber)
        if data:
            return render(request, 'dashboard/book.html', {
                'day': day,
                'month': month,
                'year': year,
                'roomNumber': roomNumber,
                'name': data[0].name,
                'time': data[0].bookedOn
            } , content_type = 'text/html')
        else:            
            return render(request, 'dashboard/book.html', {
                'day': day,
                'month': month,
                'year': year,
                'roomNumber': roomNumber
            } , content_type = 'text/html')
    # To book the room
    if request.method == "POST" and request.POST.get("name") and request.POST.get("numberOfDays"):
        # Get all the variables
        name = request.POST.get("name")
        numberOfDays = int(request.POST.get("numberOfDays"))
        day = int(request.session.get("day"))
        month = int(request.session.get("month"))
        year = int(request.session.get("year"))
        roomNumber = int(request.session.get("roomNumber"))
        # Additional variables
        noOfDaysInMonths = []
        if ((int(year) % 4 == 0 and int(year) % 100 != 0) or int(year) % 400 == 0):
            noOfDaysInMonths = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            noOfDaysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # To make an entry in the database for every day in the range of number of days
        for additionalDay in range(0,int(numberOfDays)):
            loopDay = day + additionalDay
            # If the day reaches the end of the month
            if loopDay > noOfDaysInMonths[month - 1]:
                # Update the day
                loopDay = loopDay - noOfDaysInMonths[month - 1]
                # Update the month
                loopMonth = month + 1
                # If the month reaches the year
                if(loopMonth > 12):
                    loopMonth = 1
                    # Update the year
                    loopyear = year + 1
                else:
                    loopyear = year
            else:
                loopMonth = month
                loopyear = year
            data = reservation()
            data.name = name
            data.date = str(loopDay) + "-" + str(loopMonth) + "-" + str(loopyear)
            data.roomNumber = roomNumber
            data.save()
        return redirect('index')