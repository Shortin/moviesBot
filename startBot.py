import runpy
import time 
i = 0
while(True):
	try:
		runpy.run_module(mod_name="moviesBot")
	except:
		print("error")
		time.sleep(60)
		i += 1
		if(i == 10):
			i=0
			time.sleep(600)
