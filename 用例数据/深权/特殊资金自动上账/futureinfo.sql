delete from          globalconstcust where globalconst='SQ_ZJBD_AutoBook';
insert into globalconstcust (GLOBALCONST, INTERIORID, CONSTDISPLAYNAME, MEMO, SORTSERIAL, DISPLAYNAME, DEFAULTFLAG)
values ('SQ_ZJBD_AutoBook', 'ZJ11', '208_002_042', '佣金划入自营', 2, '深圳期权资金变动字段上账的业务', 'N');
insert into globalconstcust (GLOBALCONST, INTERIORID, CONSTDISPLAYNAME, MEMO, SORTSERIAL, DISPLAYNAME, DEFAULTFLAG)
values ('SQ_ZJBD_AutoBook', '业务类别(ywlb)', '系统摘要', '业务说明', 0, '深圳期权资金变动字段上账的业务', 'N');
delete from globalpara where sortserial in(2123,2126);

insert into globalpara (SORTSERIAL, PARAID, PARANAME, DATATYPE, MAXLEN, MINLEN, DECLEN, PARAVALUE, VALUESCOPE, CONTENTS, DESCRIPTION, OPTFLAG, GLOBALPARATYPE, GRANTOPTLIST)
values (2123, 'StkOptionSZLegalPersonAudit', '是否支持深圳个股期权法人核对业务', 2, 1.0, null, null, 'Y', 'COMBOX', 'Y-支持^N-不支持', '当参数设置为Y时，系统支持深圳个股期权法人核对业务', 1, '9', null);

insert into globalpara (SORTSERIAL, PARAID, PARANAME, DATATYPE, MAXLEN, MINLEN, DECLEN, PARAVALUE, VALUESCOPE, CONTENTS, DESCRIPTION, OPTFLAG, GLOBALPARATYPE, GRANTOPTLIST)
values (2126, 'StkOptionSZPropSpecialAcctId', '深圳个股期权自营保留账户', 0, 80.0, null, null, '000000001215', 'TEXT', null, '设置系统内深圳个股期权自营券商保留资金账户,用于存放sq_zjbd中自营保证金账户上发生的结息/返佣的金额,依赖于全局参数2113', 1, '9', null);
update account set previousamt=1000000,currentamt=1000000,usableamt=1000000,TUSABLEAMT=1000000,DEPOSITSUM=0,EXCHANGECOMMISION=0 where acctid ='000000001215' and currencyid='00';