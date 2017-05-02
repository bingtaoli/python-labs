#!/usr/bin/env python
# encoding: utf-8
import re
from collections import defaultdict

re_exp_1 = re.compile('.+\s+(\d+)\s+\d+\s+[A-Za-z]+\s+/topic/(\d+) .+') 


def parse_line(log_line):
	g = re_exp_1.match(log_line)
	if g is not None:
		return (g.group(1), g.group(2))
	return None


def parse_log_file(file_name):
	user_to_topic = defaultdict(set)
	topic_to_user = defaultdict(set)
	with open(file_name, 'r') as log_file:
		for log_line in log_file:
			t = parse_line(log_line)
			if t is None:
				continue
			user_id = t[0]
			topic_id = t[1]
			user_to_topic[user_id].add(topic_id)
			topic_to_user[topic_id].add(user_id)
	return user_to_topic, topic_to_user


def get_every_day_user():
	"""
	users who visit more than two topics every day
	"""
	# log_file: hhhh-mm-dd-hh.log
	files = ['log/2017-05-%s.log' % x for x in range(1, 31)]
	every_day_user_list = set()
	every_day_topic_list = set()
	topic_list = []
	for file_name in files:
		this_day_user_set = set()
		user_to_topic, topic_to_user = parse_log_file(file_name)
		for user_id in user_to_topic:
			if len(user_to_topic.get(user_id)) >= 2:
				this_day_user_set.add(user_id)
		every_day_user_list = every_day_user_list.intersection(this_day_user_set)
		topic_list.append(topic_to_user)
	for topic_to_user in topic_list:
		this_day_topic_set = set()
		for topic_id in topic_to_user:
			user_set = topic_to_user[topic_id]
			if len(user_set.intersection(every_day_user_list)) >= 2:
				this_day_topic_set.add(topic_id)
		every_day_topic_list = every_day_topic_list.intersection(this_day_topic_set)
	return every_day_user_list, every_day_topic_list


def test():
	re_exp_1 = re.compile(re_exp_1) 
	line = "[I 130403 17:26:40] 1 200 GET /topic/456 (8.8.8.8) 300.85ms"
	m = re_exp_1.match(line)
	if m is not None:
		print "m.group() is %s" % str(m.group(0, 1, 2))
		user_id = m.group(1)
		topic_id = m.group(2)
		print user_id, topic_id


if __name__ == '__main__':
	every_day_user_list, every_day_topic_list = get_every_day_user()
	print "every_day_user_list: %s" % every_day_user_list
	print "every_day_topic_list: %s" % every_day_topic_list
