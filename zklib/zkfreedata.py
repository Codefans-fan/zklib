# -*- coding: utf-8 -*-
from struct import pack, unpack

from zkconst import CMD_FREE_DATA,MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,CMD_FINAL_AWS


def zkfreedata(self):
	"""Tell device to free data for transmisison"""
	command = CMD_FREE_DATA
	command_string =  'A014'.decode('hex')  #'8012'.decode('hex')
	chksum = 0
	session_id = unpack('HHHH', self.data_recv[8:16])[2]
	reply_id = unpack('HHHH', self.data_recv[8:16])[3]

	client_length= 10
	buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
	
	buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
	buf = buf_b + buf_a
	self.zkclient.send(buf)
	try:
		#testres ='5050827D09000000D007B8DE63190B0009'.decode('hex')
		self.data_recv = self.zkclient.recv(1024)
		return self.data_recv[16:]
	except Exception as e:
		print e
		self.disconnect()
		return False
	

def zkfinalaws(self):
	command = CMD_FINAL_AWS
	command_string = 'FFFF0000'.decode('hex')  
	chksum = 0
	session_id = unpack('HHHH', self.data_recv[8:16])[2]
	reply_id = unpack('HHHH', self.data_recv[8:16])[3]

	client_length= 12
	buf_b = self.createtop(MACHINE_PREPARE_DATA_1,MACHINE_PREPARE_DATA_2,client_length,0)
	
	buf_a = self.createHeader(command, chksum, session_id,reply_id,command_string)
	buf = buf_b + buf_a
	self.zkclient.send(buf)
	try:
		#testres ='5050827D09000000D007B8DE63190B0009'.decode('hex')
		self.data_recv =  self.zkclient.recv(1024)
		return self.data_recv[16:]
	except Exception as e:
		print e
		self.disconnect()
		return False