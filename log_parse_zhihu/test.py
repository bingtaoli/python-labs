#!/usr/bin/env python
# encoding: utf-8
import random

def write_random_data():
	for day in range(1, 31):
		log_name = "log/2017-05-%s.log" % day
		with open(log_name, 'w') as log_file:
			for hour in range(0, 24):
				log_num = random.randint(100, 200)
				for i in range(log_num):
					user_id = random.randint(0, 9999999)
					# log format: [I 130403 17:26:40] 1 200 GET /topic/456 (8.8.8.8) 300.85ms
					status = ['200', '302', '404']
					method = ['POST', 'GET', 'DELETE']
					path_base = ['topic', 'answer', 'question']
					line = '[I 1304%s %s:%s:%s] %s %s %s %s/%s (8.8.8.8) 300ms\n' % (
							day, hour, random.randint(1, 60), random.randint(1, 60),random.randint(1, 60), user_id, 
							status[random.randint(0, len(status)-1)], method[random.randint(0, len(method)-1)], 
							path_base[random.randint(0, len(path_base)-1)]
						)
					log_file.write(line)


if __name__ == '__main__':
	write_random_data()