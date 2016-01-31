#coding: utf-8
import json
import urllib
import time
import db
import os
import shutil

serverBasePath = '/home/guessever/Project/cloudcalc/cloudcalc-server'

print '+-------------------------------------+'
print '|                                     |'
print '|              CLOUDCALC              |'
print '|                                     |'
print '|                                     |'
print '|            Current  Time            |'
print time.strftime('|         %Y-%m-%d %H:%M:%S         |', time.localtime(time.time()))
print '|                                     |'
print '|                                     |'
print '|             Now Running             |'
print '|                                     |'
print '|                                     |'
print '+-------------------------------------+\n\n\n\n\n\n'

def calculatingMission():
	cid = db.getMissionCid()
	if cid != False:
		print 'Processing cid = %d ...' % (cid)
		db.changeStatus('calculation', 'cid', cid, 1)

		data = db.fetchMissionData(cid)
		path = data['path']
		inputData = dict()
		for item in data['input']:
			inputData[item['name']] = item['value']
		
		print 'Copying plugin files into run/'
		if os.path.exists('run'):
			os.popen('rm -rf run')
		shutil.copytree(path, 'run')
		print 'Plugin copied.'
		
		filename = 'input_%d.json' % time.time()
		print 'Creating input file: %s into run/' % filename
		f = open('run/%s' % (filename), 'w')
		inputStr = f.write(json.dumps(inputData, ensure_ascii = False).encode('utf-8'))
		f.close()
		print 'Input file writed.'
		
		print 'Start running program...........'
		value = os.system('python run/core/main.py < run/%s > run/output' % (filename)) >> 8
		f = open('run/output', 'rb')
		output = f.read()
		f.close()
		print 'Returned value:', value
		print 'Output:', output
		
		print 'Deleting folder run/ ....'
		os.popen('rm -rf run')
		print 'Deleted'
		
		print 'Writing calculation result into MySQL ...'
		if value != 0:
			output = '[程序返回错误代码：' + str(value) + ']\n' + output
		output = urllib.quote_plus(output)
		db.writeResult(cid, output)
		print 'Writed'

		status = value
		if value == 0:
			status = 2
		else:
			if value == 1:
				status = 3
			else:
				status = 5
		db.changeStatus('calculation', 'cid', cid, status)
		print 'Calculation mission %d completed!' % (cid)

def gittingMission():
	pid = db.getGittingPid()

Flag = True
while True:
	print time.strftime('--------- %Y-%m-%d %H:%M:%S ---------', time.localtime(time.time()))
	if Flag:
		calculatingMission()
	else:
		gittingMission()
	Flag = not Flag
	time.sleep(2)
	print '\n\n\n'

