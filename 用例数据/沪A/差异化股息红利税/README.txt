1、日间转入abcsj，冻结资金，进行申报
2、日终通过业务回报处理申报结果，仅将失败的记录处理到IndividualDividendTax。ywhb中只要有成功的，就认为成功。
UPDATE IndividualDividendTax   SET returnCode = '0002'    , returnFlag = 1,       returnDate = 20200426000000 WHERE exchId = '0'      AND offerRegId = 'A117203000'      AND knockCode = '2020042600012557'      AND date2 = 20200425000000;
3、日终jsmx文件会来资金扣款的数据，按结算编号只给一条记录，资金为申报成功的汇总资金。
