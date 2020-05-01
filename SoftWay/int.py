l = [4, 7, 1, 3, 5]
for i in range(len(l)):
	for j in range(len(l) - 1, i, -1):
		if l[j - 1] > l[j]:
			l[j - 1], l[j] = l[j], l[j - 1]
print(l)
l.reverse()
print(l, -1)