library(feather)
dir.create(".\\Temp\\", showWarnings = FALSE)
for (i in 2005 :2014 ) {
  print(i)
  df <- readRDS(paste('.\\Data\\bd.df.30firms.',i,'.Rds',sep = ""))
  path <- paste(".\\Temp\\",i,".feather",sep = "")
  write_feather(df, path)
}
rm(i)
rm(path)
rm(df)
