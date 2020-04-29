USE master
IF (EXISTS(SELECT * FROM sysdatabases WHERE name ='bmg'))		
	DROP DATABASE bmg											
GO
CREATE DATABASE bmg											
ON PRIMARY            
(
	NAME = bmg,												--�������ļ��߼�����
	FILENAME = 'F:\2020����\���ݿ�ϵͳ\ʵ��5\db\bmg.mdf',				--�����ļ�·������������(·�������)
	SIZE = 5MB,                                                 --��ʼ��С
	MAXSIZE = UNLIMITED,										--���ߴ�
	FILEGROWTH = 1MB											--�Զ�����������
)
LOG ON
( 
	NAME = bmg_log,											--��־�ļ��߼�����
	FILENAME = 'F:\2020����\���ݿ�ϵͳ\ʵ��5\db\bmg.ldf',			--��־�ļ�·������������(·�������)
	SIZE = 2MB,                                                 --��ʼ��С
	MAXSIZE = 4MB,                                              --���ߴ�
	FILEGROWTH = 10%											--�Զ�����������
)