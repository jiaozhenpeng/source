1、支持限售股对账
2、不支持非流通对账，当stklistextend表中listedstatus不是0时，对账会有问题，转入时固定填的0.
3、stkauditingerror会在初始化时删除对账平衡的记录


        tablePara_stkAuditing =
            new String[][]{
                {
                    "stkAuditingError",
                    "occurTime >= " + tradeDate + " AND (auditingErrorMsg IS NULL OR dataStatus <> 2)",
