delete from Rc_lenddeskapply where lendertype='0';

insert into Rc_lenddeskapply (EXCHID, DESKID, ACCTID, OPTID, OPTTIME, EXPOPTID, EXPTIME, FULLNAME, SETTLECODE, SETTLECODEORG, PRODUCTNAME, PRODUCT, PRODUCTCUSTODIAN, PARTICIPANTCODE1, PARTICIPANTCODE2, LENDERTYPE, OPTRESULT)
values ('0', '20140', 'A117212000', '99990', '20230722160410', '99990', '20230722143457', '1', null, '1', '1', '1', '1', null, '1', '0', 'N');

insert into Rc_lenddeskapply (EXCHID, DESKID, ACCTID, OPTID, OPTTIME, EXPOPTID, EXPTIME, FULLNAME, SETTLECODE, SETTLECODEORG, PRODUCTNAME, PRODUCT, PRODUCTCUSTODIAN, PARTICIPANTCODE1, PARTICIPANTCODE2, LENDERTYPE, OPTRESULT)
values ('1', '277300', '0117212000', '99990', '20230722173153', '99990', '20230722143457', 'ubs', null, null, null, null, null, null, null, '0', 'N');

update Rc_lenddeskapply a set  a.OPTTIME=(select    substr(b.tradedate,0,8)||substr(a.OPTTIME,9,14)       from sysconfig b );
update Rc_lenddeskapply a set  a.EXPTIME=(select    substr(b.tradedate,0,8)||substr(a.EXPTIME,9,14)       from sysconfig b );

