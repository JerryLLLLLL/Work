#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

class WebLogGeneration(object):
	site_url_base = "http://www.xxx.com/"
	def __init__(self):
		#前面7条是IE浏览器,70%为IE浏览器,接入类型上,20%为移动设备,分别为7和8,5%为空
		self.user_agent_dist = {0.0:"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
                                0.1:"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
                                0.2:"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)",
                                0.3:"Mozilla/4.0 (compatible; MSIE6.0; Windows NT 5.0; .NET CLR 1.1.4322)",
                                0.4:"Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
                                0.5:"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
                                0.6:"Mozilla/4.0 (compatible; MSIE6.0; Windows NT 5.0; .NET CLR 1.1.4322)",
                                0.7:"Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53",
                                0.8:"Mozilla/5.0 (Linux; Android 4.2.1; Galaxy Nexus Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
                                0.9:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                                1:" "}
		self.ip_slice_list = [10,29,30,46,57,62,73,77,83,92,98,101,110,121,131,142,148,157,198,211,231,244]
		self.url_path_list = ["login.php","view.php","list.php","upload.php","admin/login.php","edit.php","index.html"]
		self.http_refer = ["http://www.baidu.com/s?wd={query}","http://www.google.cn/search?q={query}","http://www.sogou.com/web?query={query}","http://one.cn.yahoo.com/s?p={query}","http://cn.bing.com/search?q={query}"]
		self.search_key_word = ["spark","hadoop","scala","hive","spark sql"]

	def sample_ip(self):
		slice = random.sample(self.ip_slice_list,1)
		return "10.163.100."+str(slice[0])
	
	def sample_url(self):
		return random.sample(self.url_path_list,1)[0]

	def sample_user_agent(self):
		dist_uppon = random.uniform(0,1)
		return self.user_agent_dist[float("%0.1f"%dist_uppon)]

	def sample_refer(self):
		if random.uniform(0,1) > 0.2: #只有20%的流量有refer
			return "-"
		refer_str = random.sample(self.http_refer,1)
		key_word = random.sample(self.search_key_word,1)
		return refer_str[0].format(query=key_word[0])
	
	def sample_one_log(self,count = 3):
		time_str = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		while count > 1:
			query_log = "{ip} -- [{localtime}] \"Get /{url} Http/1.1\" 200 0 \"{refer}\" \"{user_agent}\" \"-\"".format(ip=self.sample_ip(),localtime=time_str,url=self.sample_url(),refer=self.sample_refer(),user_agent=self.sample_user_agent())
			print query_log
			count = count - 1

if __name__ == "__main__":
	web_log_generate = WebLogGeneration()

	web_log_generate.sample_one_log(random.uniform(10,100))
			
