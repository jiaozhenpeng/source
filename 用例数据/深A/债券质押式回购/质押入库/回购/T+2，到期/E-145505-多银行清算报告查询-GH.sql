--E-145505-���������㱨���ѯ

DELETE FROM queryCondition WHERE moduleId='E' AND funcCode='145505';

DELETE FROM queryResult WHERE moduleId='E' AND funcCode='145505';

DELETE FROM queryCallFuncId WHERE moduleId='E' AND funcCode='145505';

DELETE FROM querySumResult WHERE moduleId='E' AND funcCode='145505';

INSERT INTO queryCallFuncId(moduleId,funcCode,funcName,callFuncId,callFuncType,executeMode,type,typeName,displayType,maxRowNum,sumMode,sumCallFuncId,sumCallFuncType,englishFuncName,chartFlag) values('E','145505','���������㱨���ѯ','00850170',1085,0,0,null,0,300,'0',null,0,null,'N');

INSERT INTO queryCondition(moduleId,funcCode,conditionId,interiorid,displayName,activeXType,valueType,valueLen,fractionLen,sortSerial,ownerTable,prikey,activeXNote,defaultValue,queryDisplayFlag,inputFlag) values('E','145505','occurTime','occurTime','������',4,0,19,0,1,null,null,null,null,1,1);

INSERT INTO queryCondition(moduleId,funcCode,conditionId,interiorid,displayName,activeXType,valueType,valueLen,fractionLen,sortSerial,ownerTable,prikey,activeXNote,defaultValue,queryDisplayFlag,inputFlag) values('E','145505','currencyId','currencyId','����',1,0,2,0,2,null,null,null,null,1,0);

INSERT INTO queryCondition(moduleId,funcCode,conditionId,interiorid,displayName,activeXType,valueType,valueLen,fractionLen,sortSerial,ownerTable,prikey,activeXNote,defaultValue,queryDisplayFlag,inputFlag) values('E','145505','bankIdList','bankId','���д����б�',2,0,50,0,3,null,null,null,null,1,0);

INSERT INTO queryCondition(moduleId,funcCode,conditionId,interiorid,displayName,activeXType,valueType,valueLen,fractionLen,sortSerial,ownerTable,prikey,activeXNote,defaultValue,queryDisplayFlag,inputFlag) values('E','145505','billType','billType','���ܷ�ʽ',1,0,2,0,4,null,null,null,'0-��ϸ',1,0);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','occurTime','��������',0,11,0,1,'L','0',1,1,'ALL',11,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','bankId','���д���',0,4,0,2,'L','0',1,1,'ALL',19,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','currencyId','����',0,2,0,3,'L','0',1,1,'ALL',7,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','title','��Ŀ����',0,100,0,4,'L','0',1,1,'ALL',20,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','thirdBalance','�ʻ����:�ͻ��ʽ������',1,15,3,5,'R','0',1,1,'ALL',21,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','bankBalance','�ʻ����:���д��ͻ�������',1,15,3,6,'R','0',1,1,'ALL',21,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','tradeBalance','�ʻ����:�������ܶ���',1,17,3,7,'R','0',1,1,'ALL',21,1);

INSERT INTO queryResult(moduleId,funcCode,resultId,columnName,valueType,valueLen,fractionLen,sortSerial,alignMode,sumMode,printLogFlag,displayFlag,optId,displayLen,showType) values('E','145505','needSettleAmt','�ʻ����:�轻�ս����',1,15,3,8,'R','0',1,1,'ALL',21,1);

