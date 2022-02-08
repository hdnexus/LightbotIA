from queue import Queue


openList = Queue()

def func():
    openList.put(1)
    openList.put(2)

func()
number = openList.get()
print(number)
if(openList.empty() == True):
    print('empty')
else:
    print('not empty')

