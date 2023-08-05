delete from Rc_lenddeskapply where lendertype='1';
insert into Rc_lenddeskapply (EXCHID, DESKID, ACCTID, OPTID, OPTTIME, EXPOPTID, EXPTIME, FULLNAME, SETTLECODE, SETTLECODEORG, PRODUCTNAME, PRODUCT, PRODUCTCUSTODIAN, PARTICIPANTCODE1, PARTICIPANTCODE2, LENDERTYPE, OPTRESULT)
values ('0', '00W40', '000001324165', '99990', '20230722095807', '99990', '20230722143457', null, null, null, null, null, null, null, null, '1', 'N');

insert into Rc_lenddeskapply (EXCHID, DESKID, ACCTID, OPTID, OPTTIME, EXPOPTID, EXPTIME, FULLNAME, SETTLECODE, SETTLECODEORG, PRODUCTNAME, PRODUCT, PRODUCTCUSTODIAN, PARTICIPANTCODE1, PARTICIPANTCODE2, LENDERTYPE, OPTRESULT)
values ('1', '077011', '999999999996', '99990', '20230722143819', '99990', '20230722143457', null, null, null, null, null, null, null, null, '1', 'N');

update Rc_lenddeskapply a set  a.OPTTIME=(select    substr(b.tradedate,0,8)||substr(a.OPTTIME,9,14)       from sysconfig b );
update Rc_lenddeskapply a set  a.EXPTIME=(select    substr(b.tradedate,0,8)||substr(a.EXPTIME,9,14)       from sysconfig b );

