

3、冻结证券组合费
UPDATE Account a
   SET a.usableamt      = a.usableAmt -
                          (SELECT b.amt
                             FROM (SELECT ROUND(SUM(r.stkValue *
                                                    (f.rate / 365) * 2.05282),
                                                2) amt,
                                          acctId,
                                          currencyId
                                     FROM Registration r, HK_STKValueFee f
                                    WHERE r.stkValue >= f.beginAmt
                                      AND (r.stkValue < f.endAmt OR
                                          f.endAmt = -1)
                                      AND r.exchId = f.exchId
                                      AND (r.exchId in ('4', '5'))
                                    GROUP BY acctId, currencyid) b
                            WHERE b.acctId = a.acctId
                              AND b.currencyId = a.currencyId),
       a.tradeFrozenAmt = a.tradeFrozenAmt +
                          (SELECT b.amt
                             FROM (SELECT ROUND(SUM(r.stkvalue *
                                                    (f.rate / 365) * 2.05282),
                                                2) amt,
                                          acctId,
                                          currencyId
                                     FROM Registration r, HK_STKValueFee f
                                    WHERE r.stkValue >= f.beginAmt
                                      AND (r.stkValue < f.endAmt OR
                                          f.endAmt = -1)
                                      AND r.exchId = f.exchId
                                      AND (r.exchId in ('4', '5'))
                                    GROUP BY acctId, currencyid) b
                            WHERE b.acctId = a.acctId
                              AND b.currencyId = a.currencyId)
 WHERE EXISTS (SELECT 'x'
          FROM registration r, HK_STKValueFee f
         WHERE r.stkValue >= f.beginAmt
           AND (r.stkValue < f.endAmt OR f.endAmt = -1)
           AND EXISTS (SELECT 'x'
                  FROM CUSTOMER c
                 WHERE c.custid = a.custid
                   AND c.custodymode != '1')
           AND r.exchId = f.exchId
           AND (r.exchId in ('4', '5'))
           AND a.acctId = r.acctId
           AND a.currencyId = r.currencyId);
           
