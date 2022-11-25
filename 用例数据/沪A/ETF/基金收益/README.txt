
1、上海文件为cil，zjlx=02.etftbk文件，zjlx=203
2、当etfbaseinfo无法获取时，按基金收益处理
3、当有etfbaseinfo，并且etfbaseinfo.categoryId = '1' 并且 etftype是2或4时，处理为基金收益
4、T日测试cil文件，T+1日测试etftbk文件，cil是老接口，退补款是新接口，基金公司可选择任一接口