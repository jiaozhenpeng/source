1、本用例分别包含看涨期权权利方义务方开仓，看跌期权权力方义务方开仓，义务方备兑开仓种场景
2、义务方备兑开仓在sq_jsmx中bdsl为现券备兑锁定数量
3、在sjsjg文件中有相应的QQSD和DJ00的数据,没有DJBG数据（不进行处理，DJ00调整冻结数量时，会除掉QQSD）
time=2021-05-09 14:08:48.074, nano=16939581024986, cost=10.465, sid=23, index=0, sql=SELECT exchId, deskId, offerRegId, stkId, SUM(occurQty ) occurQty, MIN(knockTime) knockTime,MAX(dbfId) dbfId,Max(reckoningTime) reckoningTime  FROM( SELECT exchId, deskId, offerRegId, stkId, (CASE WHEN orderType IN ('B2','DJ00') THEN occurQty       WHEN orderType IN ('B1','FGSD') THEN -occurQty      WHEN orderType IN ('QQXQ','QQSP','QQSD') THEN -occurQty END ) occurQty, knockTime, dbfId, reckoningTime  FROM exchangeRights  WHERE reckoningTime >= 20210509000000 AND reckoningTime <= 20210509235959 AND  orderType IN ('B0','B1','B2','DJKS','FGSD','DJ00','QQXQ','QQSP','QQSD')  AND (exchId,knockTime) IN (SELECT exchId, MAX(knockTime) FROM exchangeRights WHERE reckoningTime >= 20210509000000 AND reckoningTime <= 20210509235959 AND dbfId IN ('QYK_GF', 'QYK_SJSJG', 'QYK_BJSJG') AND exchId IN ('1','3', '6', '7') GROUP BY exchId )  AND recordtype = '00' AND listedstatus = '0' UNION ALL SELECT exchId, deskId, offerRegId, stkId, - exchFrozenQty occurQty,20210509000000 knockTime ,'QYK_GF', 20210509000000 reckoningTime  FROM STKLIST WHERE exchFrozenQty<>0 AND  exchId IN (SELECT exchId FROM  exchangeRights  WHERE reckoningTime >= 20210509000000 AND reckoningTime <= 20210509235959 AND dbfId IN ('QYK_GF', 'QYK_SJSJG', 'QYK_BJSJG'))) GROUP BY exchId, deskId, offerRegId, stkId ;

4、sjsdz中为全数量，没有冻结数量
5、sq_ccbd中会来C01（开仓）的数据，系统不处理
6、sq_hycc中会有当日持仓数量



