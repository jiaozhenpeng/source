1、日间转入abcsj，冻结资金，进行申报
2、日终通过业务回报处理申报结果，仅将失败的记录处理到IndividualDividendTax。ywhb中只要有成功的，就认为成功。
先将成功记录处理returnFlag = 2 ，表明成功数据
UPDATE IndividualDividendTax SET  returnFlag = 2  WHERE exchId = '2'      AND offerRegId = 'B185135000'      AND knockCode = '2020042600000001'      AND date2 = 20230214000000;
3、日终jsmx文件会来资金扣款的数据，按结算编号只给一条记录，资金为申报成功的汇总资金。
--查询当日成功记录
SELECT * FROM IndividualDividendTax WHERE exchId='0' AND settleDeskId='JS610' AND sendDate=20230215000000 AND validFlag=2 AND returnFlag=2 AND sendFlag=1;
处理后再更新IndividualDividendTax
UPDATE IndividualDividendTax SET validFlag=0,returnFlag=0,returnDate=20230215000000 WHERE exchId='0' AND messageType='HLS' AND knockCode='2020042600012555' AND date4=20230215000000;
