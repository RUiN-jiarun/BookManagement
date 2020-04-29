USE master
IF (EXISTS(SELECT * FROM sysdatabases WHERE name ='bmg'))		
	DROP DATABASE bmg											
GO
CREATE DATABASE bmg											
ON PRIMARY            
(
	NAME = bmg,												--主数据文件逻辑名称
	FILENAME = 'F:\2020春夏\数据库系统\实验5\db\bmg.mdf',				--数据文件路径及物理名称(路径需存在)
	SIZE = 5MB,                                                 --初始大小
	MAXSIZE = UNLIMITED,										--最大尺寸
	FILEGROWTH = 1MB											--自动增长的增量
)
LOG ON
( 
	NAME = bmg_log,											--日志文件逻辑名称
	FILENAME = 'F:\2020春夏\数据库系统\实验5\db\bmg.ldf',			--日志文件路径及物理名称(路径需存在)
	SIZE = 2MB,                                                 --初始大小
	MAXSIZE = 4MB,                                              --最大尺寸
	FILEGROWTH = 10%											--自动增长的增量
)