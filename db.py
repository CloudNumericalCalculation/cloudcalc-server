#coding: utf-8
import MySQLdb
import urllib
import json

webBasePath = '/home/guessever/Project/cloudcalc/cloudcalc-web/plugin'

def connect():
	return MySQLdb.connect(
			host = 'localhost',
			user = 'cloudcalc',
			passwd = 'MntCBCfpHfDGWY7y',
			db = 'cloudcalc',
			charset = 'utf8')

def fetchPluginData(pid):
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('SELECT `uid`, `folder`, `git` FROM `plugin` WHERE `pid` = %d' % (pid))
		cur = cursor.fetchall()
		pluginUid = long(cur[0][0])
		pluginFolder = urllib.unquote_plus(cur[0][1])
		path = webBasePath + '/' + str(pluginUid) + '/' + pluginFolder
		return path, cur[0][2]
	except:
		print 'System Error: Failed to get plugin information'
		return False
	conn.close()

def getGittingPid():
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('SELECT min(`pid`) FROM `plugin` WHERE `status` = 2 LIMIT 0, 1')
		cur = cursor.fetchall()
		pid = long(cur[0][0])
		return cid
	except:
		print 'No gitting mission'
		return False
	conn.close()

def fetchMissionData(cid):
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('SELECT `pid`, `input` FROM `calculation` WHERE `cid` = %d' % (cid))
		cur = cursor.fetchall()
		pid = long(cur[0][0])
		path, git = fetchPluginData(pid)
		# print 'path:', path
		data = dict(
				path = path,
				input = json.loads(urllib.unquote_plus(cur[0][1].encode('utf-8')))
				)
		return data
	except:
		print 'System Error: Failed to get mission data'
		return False
	conn.close()


def getMissionCid():
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('SELECT max(`priority`) FROM `calculation` WHERE `status` = 0')
		cur = cursor.fetchall()
		priority = long(cur[0][0])
		cursor.execute('SELECT min(`cid`) FROM `calculation` WHERE `priority` = %d AND `status` = 0 LIMIT 0, 1' % (priority))
		cur = cursor.fetchall()
		cid = long(cur[0][0])
		return cid
	except:
		print 'No calculating mission'
		return False
	conn.close()

def changeStatus(table, key, keyId, status):
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('UPDATE `%s` SET `status` = %d WHERE `%s` = %d' % (table, status, key, keyId))
		conn.commit()
		return True
	except:
		conn.rollback()
		print 'System Error: Failed to change status = %d of %s = %d in %s' % (status, key, keyId, table)
		return False

def writeResult(cid, result):
	try:
		conn = connect()
		cursor = conn.cursor()
	except:
		print 'Failed to connect mySQL...'
		return False
	try:
		cursor.execute('UPDATE `calculation` SET `result` = "%s" WHERE `cid` = %d' % (result, cid))
		conn.commit()
		return True
	except:
		conn.rollback()
		print 'System Error: Failed to write result to cid = %d in calculation' % (cid)
		return False
