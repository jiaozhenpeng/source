delete from globalconstcust where globalconst ='ZX_MortgageVirtualAcct';
insert into globalconstcust (GLOBALCONST, INTERIORID, CONSTDISPLAYNAME, MEMO, SORTSERIAL, DISPLAYNAME, DEFAULTFLAG)
values ('ZX_MortgageVirtualAcct', '100397', '000000888888', '', 1, '非货币充抵保证金虚拟账户', 'N');

insert into globalconstcust (GLOBALCONST, INTERIORID, CONSTDISPLAYNAME, MEMO, SORTSERIAL, DISPLAYNAME, DEFAULTFLAG)
values ('ZX_MortgageVirtualAcct', '11721010', '000011721010', '', 0, '非货币充抵保证金虚拟账户', 'N');

insert into globalconstcust (GLOBALCONST, INTERIORID, CONSTDISPLAYNAME, MEMO, SORTSERIAL, DISPLAYNAME, DEFAULTFLAG)
values ('ZX_MortgageVirtualAcct', '外部卡号', '资金帐号（多个之间使用^拼接）', '报盘交易编码（多个之间使用^拼接，与资金帐号配对）', 0, '非货币充抵保证金虚拟账户', 'N');

