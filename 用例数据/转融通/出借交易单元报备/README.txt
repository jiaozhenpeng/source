1、操作见手册7.1节
2、日间申报及导出报备文件日志如下
3、日终转入


查询：
Socket=192.168.4.62@52317 clientId=11718 serialNum=301090904000019165 state=1 time=2019-03-01 09:19:32.337 cost=8.418 successflag=0 bcnt=1 ecnt=4
head:	type=1390, len=262, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@52317", checkSum="0", flags=1, serial="0", funcCode="03900371"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="af9c31e60f404582aa7c318f7330e7c1",  
	field_1:  optmode="A0",  optid="301528",  optpwd="+pmva2Q/",  exchid="",  
response:
	field_0:  successflg=0,  recordcnt=4,  
	field_1:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="1",  deskid="077011",  acctid="QW077011",  optid="42300",  opttime="2015-06-09 13:55:46",  expoptid="99990",  exptime="2019-02-28 14:14:42",  
	field_2:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="20140",  acctid="3089",  optid="45645",  opttime="2017-03-20 09:26:16",  expoptid="99990",  exptime="2019-02-28 14:14:42",  
	field_3:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00W40",  acctid="000000301528",  optid="301528",  opttime="2019-02-28 17:31:53",  expoptid="",  exptime="",  
	field_4:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00000",  acctid="自行车",  optid="99990",  opttime="2019-02-19 15:30:32",  expoptid="99990",  exptime="2019-02-28 14:14:42",  
--------------------------- 03900371 ：查询出借交易单元 <2019-03-01 09:19:32.329,serialNum:301090904000019165> begin ---------------------------;
time=09:19:32 337, cost=7.243, sn=301090904000019165, sid=385, index=0, sql=SELECT * FROM ( SELECT a1.*, rownum rn FROM ( SELECT c.settleCodeOrg, c.settleCode, g.paraValue, r.exchId, r.deskId, r.acctId, r.optId, r.optTime, r.expOptId, r.expTime FROM Rc_lenddeskapply r, Rc_config c, GlobalPara g WHERE g.paraId = 'securitiesName' ) a1 WHERE rownum<=100 ) a2 WHERE rn>=1;
--------------------------- 03900371 ：查询出借交易单元 <2019-03-01 09:19:32.337,serialNum:301090904000019165> end ---------------------------;

Socket=192.168.4.62@56069 clientId=467669 serialNum=228103901000475905 state=1 time=2019-02-28 13:56:12.017 cost=0.443 successflag=0 bcnt=1 ecnt=4
head:	type=1390, len=261, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@56069", checkSum="0", flags=1, serial="0", funcCode="03900371"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="3ab06fd22e2046af812606ca3b4f1e4d",  
	field_1:  optmode="A0",  optid="99990",  optpwd="V1UYU8PW",  exchid="",  
response:
	field_0:  successflg=0,  recordcnt=4,  
	field_1:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00W40",  acctid="EQQQ111",  optid="42300",  opttime="2015-06-09 13:55:33",  expoptid="99990",  exptime="2019-02-28 13:56:12",  
	field_2:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="1",  deskid="077011",  acctid="QW077011",  optid="42300",  opttime="2015-06-09 13:55:46",  expoptid="99990",  exptime="2019-02-28 13:56:12",  
	field_3:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="20140",  acctid="3089",  optid="45645",  opttime="2017-03-20 09:26:16",  expoptid="99990",  exptime="2019-02-28 13:56:12",  
	field_4:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00000",  acctid="自行车",  optid="99990",  opttime="2019-02-19 15:30:32",  expoptid="99990",  exptime="2019-02-28 13:56:12",  
--------------------------- 03900371 ：查询出借交易单元 <2019-02-28 13:56:10.148,serialNum:228103901000475823> begin ---------------------------;

time=13:56:10 148, cost=0.268, sn=228103901000475823, sid=655, index=0, sql=SELECT * FROM ( SELECT a1.*, rownum rn FROM ( SELECT c.settleCodeOrg, c.settleCode, g.paraValue, r.exchId, r.deskId, r.acctId, r.optId, r.optTime, r.expOptId, r.expTime FROM Rc_lenddeskapply r, Rc_config c, GlobalPara g WHERE g.paraId = 'securitiesName' ) a1 WHERE rownum<=100 ) a2 WHERE rn>=1;

--------------------------- 03900371 ：查询出借交易单元 <2019-02-28 13:56:10.148,serialNum:228103901000475823> end ---------------------------;


新增：	
Socket=192.168.4.62@50392 clientId=233320 serialNum=228161651000235986 state=1 time=2019-02-28 17:31:53.544 cost=5.953 successflag=0 bcnt=1 ecnt=0
head:	type=1390, len=295, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@50392", checkSum="0", flags=1, serial="0", funcCode="03900370"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="7492366353ae4dc9b45473a9890af6aa",  
	field_1:  optmode="A0",  optid="301528",  optpwd="UlMfUMfY",  actiontype="add",  exchid="0",  deskid="00W40",  acctid="000000301528",  
response:
	field_0:  successflg=0,  recordcnt=0,  	
--------------------------- 03900370 ：设置出借交易单元 <2019-02-28 17:31:53.538,serialNum:228161651000235986> begin ---------------------------;
time=17:31:53 538, cost=0.242, sn=228161651000235986, sid=504, index=0, sql=SELECT * FROM RC_LendDeskApply WHERE exchId='0' AND deskId='00W40';
time=17:31:53 539, cost=0.947, sn=228161651000235986, sid=504, sql=INSERT INTO RC_LendDeskApply(exchId,deskId,acctId,optId,optTime) values('0','00W40','000000301528','301528',2.0190228173153E13);
time=17:31:53 541, cost=0.962, sn=228161651000235986, sid=504, sql=INSERT INTO Syslog(occurTime,serialNum,optId,briefId,sysSetType,operationMAC,optLevel,optBranchId,memo) values(20190228173153,2076801,'301528','001_005_004_004_015',1,'FCAA14CB20CE|100003','A0','000001','增加[市场=0,席位=00W40,备付金账户=000000301528]');
--------------------------- 03900370 ：设置出借交易单元 <2019-02-28 17:31:53.544,serialNum:228161651000235986> end ---------------------------;

修改：
Socket=192.168.4.62@51540 clientId=80964 serialNum=301100943000081220 state=1 time=2019-03-01 10:39:46.039 cost=41.235 successflag=0 bcnt=1 ecnt=0
head:	type=1390, len=292, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@51540", checkSum="0", flags=1, serial="0", funcCode="03900370"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="2c36c5919df54b88951ac1487d994ce1",  
	field_1:  optmode="A0",  optid="301528",  optpwd="+pmva2Q/",  actiontype="modify",  exchid="0",  deskid="00W40",  acctid="000000",  
response:
	field_0:  successflg=0,  recordcnt=0,  

删除：
Socket=192.168.4.62@56918 clientId=480727 serialNum=305113304000481195 state=1 time=2019-03-05 14:10:55.388 cost=9.415 successflag=0 bcnt=1 ecnt=0
head:	type=1390, len=292, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@56918", checkSum="0", flags=1, serial="0", funcCode="03900370"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="b56631abcb1c479a9d2c11355aad72d5",  
	field_1:  optmode="A0",  optid="301528",  optpwd="8rPJXGyt",  actiontype="DELETE",  exchid="0",  deskid="00W40",  acctid="000000",  
response:
	field_0:  successflg=0,  recordcnt=0,  
--------------------------- 03900370 ：设置出借交易单元 <2019-03-05 14:10:55.379,serialNum:305113304000481195> begin ---------------------------;
time=14:10:55 382, cost=1.078, sn=305113304000481195, sid=1121, index=0, sql=SELECT * FROM RC_LendDeskApply WHERE exchId='0' AND deskId='00W40';
time=14:10:55 383, cost=1.221, sn=305113304000481195, sid=1121, sql=DELETE FROM RC_LendDeskApply WHERE exchId='0' AND deskId='00W40';
time=14:10:55 385, cost=0.808, sn=305113304000481195, sid=1121, sql=INSERT INTO Syslog(occurTime,serialNum,optId,briefId,sysSetType,operationMAC,optLevel,optBranchId,memo) values(20190305141055,1368498,'301528','001_005_004_004_015',3,'FCAA14CB20CE|100004','A0','000001','删除[市场=0,席位=00W40,备付金账户=000000]');
--------------------------- 03900370 ：设置出借交易单元 <2019-03-05 14:10:55.388,serialNum:305113304000481195> end ---------------------------;

导出：
Socket=192.168.4.62@51724 clientId=58152 serialNum=301141201000058220 state=1 time=2019-03-01 14:34:55.635 cost=11.522 successflag=0 bcnt=1 ecnt=1
head:	type=1390, len=266, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@51724", checkSum="0", flags=1, serial="0", funcCode="03900681"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="ec37551d5d1240179d5079b334341558",  
	field_1:  optmode="A0",  optid="301528",  optpwd="+pmva2Q/",  deskid="ZRT5",  
response:
	field_0:  successflg=0,  recordcnt=1,  
	field_1:  exchid="0",  dbfid="CJJYDYBB",  chinesename="证券出借交易单元报备库",  dbffullpath="E:\prop2000\CJJYDYBB.dbf",  
--------------------------- 03900681 ：取转入文件的路径 <2019-03-01 14:34:55.623,serialNum:301141201000058220> begin ---------------------------;
time=14:34:55 635, cost=3.809, sn=301141201000058220, sid=203, index=0, sql=SELECT * FROM TransdbfPath WHERE deskId='ZRT5';
--------------------------- 03900681 ：取转入文件的路径 <2019-03-01 14:34:55.635,serialNum:301141201000058220> end ---------------------------;
	
Socket=192.168.4.62@51733 clientId=58230 serialNum=301141201000058298 state=1 time=2019-03-01 14:34:57.687 cost=0.479 successflag=0 bcnt=1 ecnt=4
head:	type=1390, len=262, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@51733", checkSum="0", flags=1, serial="0", funcCode="03900371"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="ec37551d5d1240179d5079b334341558",  
	field_1:  optmode="A0",  optid="301528",  optpwd="+pmva2Q/",  exchid="",  
response:
	field_0:  successflg=0,  recordcnt=4,  
	field_1:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="1",  deskid="077011",  acctid="QW077011",  optid="42300",  opttime="2015-06-09 13:55:46",  expoptid="301528",  exptime="2019-03-01 14:34:57",  
	field_2:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="20140",  acctid="3089",  optid="45645",  opttime="2017-03-20 09:26:16",  expoptid="301528",  exptime="2019-03-01 14:34:57",  
	field_3:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00W40",  acctid="000000",  optid="301528",  opttime="2019-02-28 17:31:53",  expoptid="301528",  exptime="2019-03-01 14:34:57",  
	field_4:  settlecodeorg="999",  settlecode="58",  securitiesname="北京根网科技有限公司（开发测试环境）",  exchid="0",  deskid="00000",  acctid="自行车",  optid="99990",  opttime="2019-02-19 15:30:32",  expoptid="301528",  exptime="2019-03-01 14:34:57",  
--------------------------- 03900371 ：查询出借交易单元 <2019-03-01 14:34:57.687,serialNum:301141201000058298> begin ---------------------------;
time=14:34:57 687, cost=0.243, sn=301141201000058298, sid=967, index=0, sql=SELECT * FROM ( SELECT a1.*, rownum rn FROM ( SELECT c.settleCodeOrg, c.settleCode, g.paraValue, r.exchId, r.deskId, r.acctId, r.optId, r.optTime, r.expOptId, r.expTime FROM Rc_lenddeskapply r, Rc_config c, GlobalPara g WHERE g.paraId = 'securitiesName' ) a1 WHERE rownum<=100 ) a2 WHERE rn>=1;
--------------------------- 03900371 ：查询出借交易单元 <2019-03-01 14:34:57.687,serialNum:301141201000058298> end ---------------------------;

	
Socket=192.168.4.62@51731 clientId=58226 serialNum=301141201000058294 state=1 time=2019-03-01 14:34:57.671 cost=11.757 successflag=0 bcnt=1 ecnt=0
head:	type=1390, len=266, MAC="FCAA14CB20CE", srcAddr="192.168.4.62@51731", checkSum="0", flags=1, serial="0", funcCode="03900372"
request:
	field_0:  recordcnt=1,  apitype="StockCS",  apiversion="4.0.6883.24577",  terminalinfo="PC;IIP:192.168.4.254;LIP:192.168.4.62;MAC:FCAA14CB20CE;HD:Z9APTJTF;PCN:WANGHAIDONG-PC;CPU:BFEBFBFF000306C3;PI:C,NTFS,200.00;PVOL:308ECB7A",  compressflag=1,  guid="ec37551d5d1240179d5079b334341558",  
	field_1:  optmode="A0",  optid="301528",  optpwd="+pmva2Q/",  opttype=2,  
response:
	field_0:  successflg=0,  recordcnt=0,  
--------------------------- 03900372 ：更新出借交易单元导出信息 <2019-03-01 14:34:57.66,serialNum:301141201000058294> begin ---------------------------;
time=14:34:57 663, cost=0.129, sn=301141201000058294, sid=1121, index=0, sql=SELECT (SYSDATE-TO_DATE('19700101','yyyymmdd'))*24*60*60*1000 FROM dual;
time=14:34:57 664, cost=0.815, sn=301141201000058294, sid=355, sql=UPDATE Rc_lendDeskApply SET expOptId='301528',expTime=20190301143457;
time=14:34:57 666, cost=0.653, sn=301141201000058294, sid=355, sql=INSERT INTO Syslog (occurTime,serialNum,optId,briefId,sysSetType,operationMAC,optLevel,optBranchId,memo) VALUES(20190301143457,2304005,'301528','001_004_002_008',0,'FCAA14CB20CE|100003','A0','000001','转融通出借交易单元报备');
--------------------------- 03900372 ：更新出借交易单元导出信息 <2019-03-01 14:34:57.671,serialNum:301141201000058294> end ---------------------------;




[2023-07-22 12:40:38.292]Socket=173.168.64.238@60407 clientId=525 serialNum=722123150000001721 state=0 time=2023-07-22 12:40:38.292
head:	type=1390, len=676, MAC="70B5E8707235", srcAddr="173.168.64.238@60407", checkSum="17545", flags=2, serial="183", funcCode="03900683"
request:
	field_0:  recordcnt=4,  apitype="Stock",  apiversion="2.2.8.0",  terminalinfo="PC;IIP=NA;IPORT=NA;LIP=173.168.64.238;MAC=70B5E8707235;HD=417AZRZMS;PCN=JIAOZHENPENG;CPU=BFEBFBFF000A0671;PI=C^NTFS^138.25G;VOL=0005-2FC7",  compressflag=1,  
	field_1:  dbfid="ZRTCJJYDYBBQR",  settlementcode="000099",  brokername="瑞银证券有限责任公司",  orderdate="20230722",  registrarcode="100226",  exchid="1",  deskid="00W40",  acctid="040000000000236072",  checkresult="成功",  sendtime=20230722,  optmode="A0",  optid="99990",  optpwd="GEdw7+Vh ",  
	field_2:  settlementcode="000099",  brokername="瑞银证券有限责任公司",  orderdate="20230722",  registrarcode="100226",  exchid="0",  deskid="077011",  acctid="B001205100",  checkresult="成功",  sendtime=20230722,  
	field_3:  settlementcode="000099",  brokername="瑞银证券有限责任公司",  orderdate="20230722",  registrarcode="100226",  exchid="1",  deskid="20140",  acctid="040000000000235987",  checkresult="成功",  sendtime=20230722,  
	field_4:  settlementcode="000099",  brokername="瑞银证券有限责任公司",  orderdate="20230722",  registrarcode="100226",  exchid="0",  deskid="277300",  acctid="B001052400",  checkresult="成功",  sendtime=20230722,  

--------------------------- 03900683 ：导入转融通清算数据 <2023-07-22 12:40:38.292, nano:76705484107800, serialNum:722123150000001721> begin ---------------------------;

time=2023-07-22 12:40:38.293, nano=76705485498600, cost=0.007, sn=722123150000001721, sid=204, sqlPrepare=@3ba86faf, sql=INSERT INTO RC_LendDeskCFM(settlecode,settlecodeOrg,participantcode,fullName,brokername,productName,product,productregid,productCustodian,orderdate,exchId,deskId,acctId,optresult,senddate,lenderType) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

time=2023-07-22 12:40:38.294, nano=76705486094100, cost=0.563, sn=722123150000001721, sid=204, sqlExecute=@3ba86faf;

time=2023-07-22 12:40:38.294, nano=76705486130900, cost=0.004, sn=722123150000001721, sid=204, sqlPrepare=@2f530c5c, sql=INSERT INTO RC_LendDeskCFM(settlecode,settlecodeOrg,participantcode,fullName,brokername,productName,product,productregid,productCustodian,orderdate,exchId,deskId,acctId,optresult,senddate,lenderType) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

time=2023-07-22 12:40:38.294, nano=76705486255000, cost=0.117, sn=722123150000001721, sid=204, sqlExecute=@2f530c5c;

time=2023-07-22 12:40:38.294, nano=76705486272400, cost=0.003, sn=722123150000001721, sid=204, sqlPrepare=@54a3b8ce, sql=INSERT INTO RC_LendDeskCFM(settlecode,settlecodeOrg,participantcode,fullName,brokername,productName,product,productregid,productCustodian,orderdate,exchId,deskId,acctId,optresult,senddate,lenderType) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

time=2023-07-22 12:40:38.294, nano=76705486358300, cost=0.081, sn=722123150000001721, sid=204, sqlExecute=@54a3b8ce;

time=2023-07-22 12:40:38.294, nano=76705486373900, cost=0.003, sn=722123150000001721, sid=204, sqlPrepare=@68b41e3a, sql=INSERT INTO RC_LendDeskCFM(settlecode,settlecodeOrg,participantcode,fullName,brokername,productName,product,productregid,productCustodian,orderdate,exchId,deskId,acctId,optresult,senddate,lenderType) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

time=2023-07-22 12:40:38.294, nano=76705486452700, cost=0.075, sn=722123150000001721, sid=204, sqlExecute=@68b41e3a;

time=2023-07-22 12:40:38.297, nano=76705488671900, cost=2.201, sn=722123150000001721, sid=204, sql= UPDATE rc_LendDeskApply a  SET optResult = 'Y'  WHERE EXISTS (SELECT 'x'  FROM rc_LendDeskCfm b  WHERE b.exchId = a.exchId  AND b.deskId = a.deskId  AND b.sendDate = '20230722'  AND b.lenderType <> 0) ;

--------------------------- 03900683 ：导入转融通清算数据 <2023-07-22 12:40:38.297, nano:76705488987100, serialNum:722123150000001721> end ---------------------------;

