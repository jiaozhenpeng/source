delete from globalpara where sortserial in(2111,2119);
insert into globalpara (SORTSERIAL, PARAID, PARANAME, DATATYPE, MAXLEN, MINLEN, DECLEN, PARAVALUE, VALUESCOPE, CONTENTS, DESCRIPTION, OPTFLAG, GLOBALPARATYPE, GRANTOPTLIST)
values (2111, 'StkOptionSHPropAcctId', '上海个股期权自营保证金账户', 0, 80.0, 0.0, 0.0, '041000000000107065', 'TEXT', null, '设置个股期权自营的券商保证金账户,注意:系统启用了个股期权自营业务才需设置', 1, '9', null);

insert into globalpara (SORTSERIAL, PARAID, PARANAME, DATATYPE, MAXLEN, MINLEN, DECLEN, PARAVALUE, VALUESCOPE, CONTENTS, DESCRIPTION, OPTFLAG, GLOBALPARATYPE, GRANTOPTLIST)
values (2119, 'StkOptionSHPropSpecialAcctId', '上海个股期权自营保留账户', 0, 80.0, null, null, '000000001215', 'TEXT', null, '设置系统内上海个股期权自营券商保留资金账户,用于存放op_zjbd中自营保证金账户上发生的结息/返佣的金额,依赖于全局参数2111', 1, '9', null);
