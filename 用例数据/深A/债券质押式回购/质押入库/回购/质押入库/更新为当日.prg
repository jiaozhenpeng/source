update zqjsxx set rq=dtos(date())
update sjsgb set gbrq=dtos(date())
update  sjsgb set gbrq1=dtos(date()+1) where gblb='MZ'
update  sjsgb set gbrq2=dtos(date()+1) where gblb='LX'
update  sjsgb set gbrq2=dtos(date()+2) where gblb='ZS'
update  sjsgb set gbrq1=dtos(date()+2) where gblb='ZS'
update  sjsjg set jgcjrq=dtos(date()) 
update  sjsjg set jgfsrq=dtos(date()) 
update  jsmx set jyrq=dtos(date()) 
update  jsmx set qsrq=dtos(date()) 