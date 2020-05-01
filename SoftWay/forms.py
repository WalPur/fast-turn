from django import forms

class REGIST(forms.Form):
	name = forms.CharField(label="Название предприятия")
	Period = forms.IntegerField(label="Период обновления очереди")
	OpenTime = forms.IntegerField(label="Время открытия", max_value=24)
	CloseTime = forms.IntegerField(label="Время закрытия", max_value=24)
	description = forms.CharField(label="Описание", widget=forms.Textarea)
class REG(forms.Form):
	user = forms.CharField(label="Имя пользователя")
	UserMail = forms.EmailField(label="Электронная почта")
	UserPassword = forms.CharField(label="Пароль", widget=forms.PasswordInput)
	UserType = forms.ChoiceField(choices=((1, "Предприниматель"), (2, "Пользователь")), label='Выберите тип аккаунта')
class Log(forms.Form):
	user = forms.CharField(label="Логин")
	password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
class queueId(forms.Form):
	id = forms.IntegerField(label='Введите id предприятия')