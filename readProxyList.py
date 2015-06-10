import pickle
with open('proxy.txt', 'r') as f:
	lines = f.readlines()

data = [line.split() for line in lines]
with open('proxy.dp', 'wb+') as f:
	pickle.dump(data, f)