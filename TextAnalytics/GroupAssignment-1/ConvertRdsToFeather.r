library(feather)
for (i in 2005 :2014 ) {
  print(i)
  df <- readRDS(paste('bd.df.30firms.',i,'.Rds',sep = ""))
  path <- paste(i,".feather",sep = "")
  write_feather(df, path)
}
rm(i)
rm(path)
rm(df)
