import collections, itertools
import pylab as pl
import matplotlib.pyplot as plt
import numpy as np

## This function works with data from the first run 
def feature_stat():
	
	prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	path = prefix+"/upwork/data/"
	## Data file to extract stat of features
	f_r = open(path+"appt_dump_transformed_continent.csv", "r")
	## Plot folder
	plotpath = prefix+"/upwork/results/plot/"
	
	if original: ## the original app_dump file
		f_r = open(path+"appt_dump_rewritten.csv", "r")
 		att_name = ["ID", "AllowAccessPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
	"AllowGeo","AllowFeaturePush","ScreenHeight","AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
	"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
	"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount","Timezone","sdk","UserType","Questions",
	"CorrectQuestion"]
	
	else: ## a processed file obtained from calling checkFile() and transformFeature() in extractUtil.py
		
		f_r = open(path+"appt_dump_transformed_continent.csv", "r")	
		att_name = ['ID', 'AllowPush', 'AdOptedIn', 'NumCampaignMatch', 'Carrier', 'AppVersion', 
	'AllowiBeacon', 'AllowGeo', 'AllowFeaturePush', 'ScreenHeight', 'AllowBT', 'HaveUniqueGlobalID', 
	'NumCrash', 'DailyUsage','Country', 'LastUpdateDays', 'DeviceModel', 'BlockPushTF', 'BlockPushSameday', 'BlockPushAfterDays', 
	'OS', 'OSVersion', 'RevokePushTF', 'RevokePushBefore', 'RevokePushSameday', 'RevokePushAfterDays', 'SignIn', 
	'UninstalledTF', 'UninstalledSameday', 'UninstalledAfter', 'ScreenWidth', 'EmailExist', 'EmailAddress', 
	'InstallDays', 'PushCount', 'Timezone', 'UserType', 'Questions', 'CorrectQuestion']
	
 
	## Boolean feature list
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress","BlockPushTF", "RevokePushTF",
	"RevokePushBefore", "RevokePushSameday", "UninstalledTF" ]
	
	## Categorical feature list
	category_arr_list = ["AppVersion", "DeviceModel","OS","UserType", "OSVersion","Timezone","ScreenWidth","ScreenHeight","Country" ] 
 	
 	## Integer feature list
	integer_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", "BlockPushAfterDays", "RevokePushAfterDays", "UninstalledAfter", "LastUpdateDays"]
	
 	## Low variance features
	Uni_arr_list = ["AdOptedIn", "AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"]


	num_att = len(att_name)
  
	data = dict()
	for i in range(0, num_att):
		data[i] = []
		
	extra_att = set() 
	num_extra_rows = 0
	for line in f_r.readlines()[1::]:
		arr = line.strip().split(",") 
		
		for i in range(0, num_att):
			if att_name[i] in integer_arr_list:
				data[i].append(int(arr[i])) 
			else:
				data[i].append(arr[i]) 
			 
 	for i, arr in data.items():
		if i==0: continue		
		print "\n"+str(i)+": "+ att_name[i]
		att_freqs = collections.OrderedDict(sorted(collections.Counter(data[i]).items()))
		if  att_name[i] in boolean_arr_list:  # T/F features - make pie  chart
			 
			isbool = True
			makePie(att_freqs,  att_name[i], isbool, plotpath)
		elif att_name[i] in category_arr_list+integer_arr_list+Uni_arr_list:
			isbool = False
		 
			if len(att_freqs.keys())>5: ## make bar chart if there are many values 
				makeBar(att_freqs,  att_name[i], plotpath)
			else: ## make pie chart if there are a few values 
 				makePie(att_freqs,  att_name[i], isbool, plotpath)
		 
		else:
			 print att_name[i] +" not in arr list"

	makePie(att_freqs, "RevokePushStat", False, plotpath)
	f_r.close()
 
	
def makeBar(att_freqs,  attname, path):
 
	labels = att_freqs.keys()
	values = att_freqs.values()
	ax =  pl.figure()
	ax = pl.subplot(111)
	ind = np.arange(len(labels))
	width = 0.8
	ax.bar(ind,values, width=width)
	ax.set_xticks(np.arange(len(labels))+width/2)
	ax.set_xticklabels(labels, rotation=90)
	ax.set_title(attname)
	plt.savefig(path+attname+".png")
 

def makePie(att_freqs, attname, isbool, path):
	
	
	ax = pl.figure()
	ax = pl.subplot(111)
	if  isbool:
		print att_freqs.keys()
		labels = ["True" if v.strip()=="1" else "False"  if v.strip()=='0' else "Missing" for v in att_freqs.keys()]
	else:
		labels = att_freqs.keys()
	values = att_freqs.values()
	explode=(0, 0.05, 0, 0)
	pl.pie(values,  labels=labels,  autopct='%1.1f%%', shadow=True, startangle=90)
	pl.title(attname, bbox={'facecolor':'0.8', 'pad':5})
	pl.savefig(path+attname+".png")
	
feature_stat()
