行权过户op_zqjs文件中有三种情况：
1、全部股份过户，此时为股份增加或减少
2、全部转现金交收，此时股份不处理，全部处理为资金
3、部分股份、部分转现金，此时现金和股份全部处理
以上为有op_zqjs的场景，按op_zqjs进行交收，关联条件如下
 condVec.setCondition("knocktime", settle.getKnockTime());
            condVec.setCondition("settleDate", settle.getSettledate());
            condVec.setCondition("exchId", settle.getExchId());
            condVec.setCondition("deskid", settle.getDeskId());
            condVec.setCondition("offerRegId", settle.getOfferRegId());
            condVec.setCondition("stkId", settle.getStkId());

没有op_zqjs的场景为：当日行权后，应收应付轧差后为0，此时不会来文件，按未交收表进行交收
处理条件为：settledate=当前交易日