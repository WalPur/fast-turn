from django.shortcuts import render, redirect
from .models import comment
from .models import queue
from .models import people
from .models import Test
from .forms import REGIST
from .forms import REG as REG
from .forms import Log as log
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
import datetime 

def index(request):
	if request.user.is_authenticated:
		return redirect('/lk')
	else:
		return render(request, 'index.html')
def lk(request):
	if request.user.is_authenticated == False:
		return redirect('/')
	elif request.user.is_authenticated == True:
		queues = people.objects.get(user_id=request.user.id)
		Lqueues = []
		string = ''
		lqueues = queues.queues
		for i in range(len(lqueues)):
			if lqueues[i] == "#":
				Lqueues.append(queue.objects.get(id=int(string)))
				string = ''
			else:
				string += lqueues[i]
		times = []
		if request.user.get_short_name() == '1':
			for i in range(len(Lqueues)):
				times.append(Lqueues[i].last)
		else:
			timesQueues = queues.time
			for i in range(len(timesQueues)):
				if timesQueues[i] == '#':
					times.append(string)
					string = ''
				else:
					string += timesQueues[i]
		data = {"cometype": "cab", "name": request.user.get_username(), "type": request.user.get_short_name(), "queues": Lqueues, 'times': times}
		return render(request, "lk.html", context = data)
	else:
		print("here")
def monitoring(request, id=''):
	if request.method == "POST":
		return redirect('monitoring/' + request.POST.get('id'))
	if id == '':
		return render(request, 'writeIn.html')
	obj = queue.objects.get(id=id)
	arr1 = []
	arr2 = []
	if request.user.get_username() == obj.creator:
		def decr(inputS):
			string = ''
			arr = []
			for s in inputS:
				if s == "#":
					arr.append(string)
					string = ""
				else:
					string += s
			return arr
		arr1 = decr(obj.people)
		arr2 = decr(obj.time)
	data = {'name': obj.name, 'description': obj.description, 'Period': obj.period, 'OpenTime': obj.openTime, 'CloseTime': obj.closeTime, 'time': obj.last, 'arr1': arr1, 'arr2': arr2}
	return render(request, 'monitoring.html', context=data)
def create(request):
	if request.method == "POST":
		data = queue()
		data.name = request.POST.get('name')
		data.period = request.POST.get('Period')
		data.openTime = request.POST.get('OpenTime')
		data.closeTime = request.POST.get('CloseTime')
		data.creator = request.user.get_username()
		data.people = ""
		data.description = request.POST.get('description')
		data.last = str(data.openTime) + ':' + '00'
		data.save()
		pUpdate = people.objects.get(user_id=request.user.id)
		pUpdate.queues += str(data.id) + "#"
		pUpdate.save()
		tempData = {
			'name': data.name,
			'Period': data.period,
			'OpenTime': data.openTime,
			'CloseTime': data.closeTime,
			'ID': data.id,
			'description': data.description
		}
		return render(request, 'QUEUEgetPage.html', context=tempData)
	else:
		registForm = REGIST()
		data = {'forms': registForm}
		return render(request, 'create.html', context=data)
def writeIn(request):
	if request.method == "POST" and request.POST.get('time') != None:
			idnum = int(request.POST.get('idnum'))
			WriteInId = queue.objects.get(id=idnum)
			WriteInId.people += request.user.get_username() + "#"
			time = WriteInId.last
			print(time)
			Minutes = int(time[len(time) - 2] + time[len(time) - 1])
			if time[2] == ':':
				hours = int(time[0] + time[1])
			else:
				hours = int(time[0])
			print(hours, Minutes)
			Minutes += WriteInId.period
			if Minutes >= 60:
				Minutes = Minutes % 60
				hours += 1
				if hours > 24:
					hours = 0
			if Minutes < 10:
				Minutes = '0' + str(Minutes)
			else:
				Minutes = str(Minutes)
			if hours >= 24:
				hours = hours % 24
			if hours >= int(WriteInId.closeTime):
				hours = WriteInId.openTime
				Minutes = '00'
			time = str(hours) + ":" + Minutes
			WriteInId.last = time
			WriteInId.time += time + "#"
			WriteInId.save(update_fields=["people", 'last', 'time'])
			pUpdate = people.objects.get(user_id=request.user.id)
			pUpdate.queues += str(idnum) + "#"
			pUpdate.time += time + "#"
			pUpdate.save()
			return redirect('/lk')
	elif request.method == "POST":
		idnum = request.POST.get("id")
		WriteInId = queue.objects.get(id=idnum)
		data = {'IDinned': WriteInId.name, "OPT": WriteInId.openTime, "CT": WriteInId.closeTime, "Period": WriteInId.period, 'desc': WriteInId.description, 'idnm': idnum}
		return render(request, 'IDgetPage.html', context=data)
	else:
		return render(request, 'writeIn.html')
def logIn(request):
	if request.user.is_authenticated:
		return redirect('/lk')
	else:
		if request.method == "GET":
			data = {"forms": log}
			return render(request, 'log.html', context=data)
		else:	
			user = request.POST['user']
			password = request.POST['password']
			user = authenticate(username = user, password = password)
			if user != None:
				if user.is_active:
					login(request, user)
					data = {'name': user.get_username(), 'type': user.get_short_name()}
					return render(request, 'succes.html', context=data)
def regist(request):
	if request.user.is_authenticated:
		return redirect('/lk')
	else:
		if request.method == "GET":
			reg = REG()
			data = {'forms': reg}
			return render(request, 'reg.html', context=data)
		else:
			name = request.POST.get('user')
			email = request.POST.get('UserMail')
			typeU = request.POST.get('UserType')
			password = request.POST.get('UserPassword')
			data = {'name': name, 'email': email, 'type': typeU}
			user = User.objects.create_user(name, email, password) 
			user.first_name = typeU
			user.save()
			acc = people.objects.create(user=user, queues="")
			user = authenticate(username = name, password = password)
			login(request, user)
			return render(request, 'succes.html', context=data)
def logout(request):
	django_logout(request)
	return redirect('/')
def about(request):
	obj = Test.objects.all()
	times = []
	for i in obj:
		times.append(i.time)
	print(times)
	print(sorted(times))
	return render(request, 'about.html')
def test(request):
	times = Test()
	times.time = datetime.time(11, 70) 
	times.save()
	if request.method == "POST":
		comm = comment()
		comm.text = request.POST.get("text")
		comm.author = request.user.get_username()
		comm.save()
	return render(request, 'comm.html', {'comments': comment.objects.all()})