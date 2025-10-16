#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from importlib import reload
import os
import re
import sys
import getopt
import shutil
import codecs
from abc import ABCMeta, abstractmethod

from src import res, version

if sys.version_info.major < 3:
	reload(sys)
	sys.setdefaultencoding('utf8')

g_strHelp = """\
用法: {} [项目路径名称]...
作用: 创建 c++ 项目
例如: {} testCpp
选项:
    -h --help       说明
    -v --version    版本
""".format(os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))

g_strCmdPath = ""
g_strProjectName = "aaa"  # test




#########################################################

class CmdHandle:
	__listArgs = []
	__listProjectName = []
	
	def __init__(self, args):
		self.__listArgs = args
	
	def handle(self):
		global g_strHelp
		global g_strCmdPath
		
		dictOp = {
			"version": "v",
			"help": "h",
		}
		listLongOp = [k for k, v in dictOp.items() if len(k) > 0]
		strShortOp = "".join([v for k, v in dictOp.items() if len(v) > 0])
		
		listArgs = self.__listArgs[1:]
		while len(listArgs) > 0:
			options, listArgs = getopt.getopt(listArgs, strShortOp, listLongOp)
			for op, v in options:
				if op in ["--version", "-v"]:
					print(version.__version__)
					os.chdir(g_strCmdPath)
					sys.exit(0)
				if op in ["--help", "-h"]:
					print(g_strHelp)
					os.chdir(g_strCmdPath)
					sys.exit(0)
			
			if len(listArgs) > 0:
				self.__listProjectName.append(listArgs[0])
				del listArgs[0]
			
			if len(listArgs) <= 0:
				break
		else:
			print(g_strHelp)
			sys.exit(0)
		
		if len(self.__listProjectName) == 0:
			print(g_strHelp)
		
		self.__makeProject()
		

	def __makeProject(self):
		global g_strHelp
		
		for strProjectName in self.__listProjectName:
			os.chdir(g_strCmdPath)
			try:
				if os.path.exists(strProjectName):
					print("项目目录已经存在,是否删除创建 创建: Y(y)/跳过:C(c)/退出：其它")
					strCmd = ""
					
					strCmd = input("请输入：")
						
					if strCmd in ('Y', 'y'):
						print("正在删除目录 " + strProjectName)
						shutil.rmtree(strProjectName)
						print("删除成功")
					elif strCmd in ('C', 'c'):
						continue
					else:
						print("退出创建项目 " + strProjectName)
						os.chdir(g_strCmdPath)
						sys.exit(0)

				self.__mkCpp(strProjectName)
				print("创建项目 %s 成功" % strProjectName)
			except OSError:
				print("创建项目 %s 失败 " % strProjectName)
				print(OSError.strerror)
				os.chdir(g_strCmdPath)
				shutil.rmtree(strProjectName)
				pass
			

	def __mkCpp(self, strProjectName: str):
		
		oldPath = os.getcwd()
		os.makedirs(strProjectName, 0o755)
		os.chdir(strProjectName)

		for n in res.listDirs:
			os.makedirs(n, 0o755)
		
		strFileName = strProjectName
		strFileName = strFileName[0].lower() + strFileName[1:]

		listTemp = result = re.split(r'[_-]', strProjectName)
		strClassName = ''.join([(n[0].upper() + n[1:]) for n in listTemp])

		strDefName = strProjectName.upper()
		strDefName = re.sub(r"[^A-Za-z]", '_', strDefName)

		for k, v in res.fileInfo.items():
			fileName = k.replace("cppAppTemplate", strFileName)
			with codecs.open(fileName, 'w', 'utf-8') as fw:
				srcCode = v.replace("cppAppTemplate", strFileName)
				srcCode = srcCode.replace("CppAppTemplate", strClassName)
				srcCode = srcCode.replace("CPPAPPTEMPLATE", strDefName)

				fw.write(srcCode)
		
		os.chdir(oldPath)


if __name__ == "__main__":
	
	g_strCmdPath = os.getcwd()

	CmdHandle(sys.argv).handle()

	os.chdir(g_strCmdPath)
