
rm(list=ls())

setwd("~/github/rm-gardiner-java/dev/MCAL_data/RK/")

N = 25 # number of old or new items for each category (word/ non-word)

rk_files = list.files(pattern = ".csv")

rk_dat = data.frame()
for (f in rk_files){
  tmp = read.csv(f)
  tmp$file = f
  rk_dat = rbind(rk_dat, tmp)
}

#rk_dat = do.call("rbind", lapply(rk_files, read.csv))

# make sure there are no duplicate files
if (!all(table(rk_dat$ID) == 100)){
  rk_dat$ID = as.numeric(as.factor(rk_dat$file))
}
all(table(rk_dat$ID) == 100)

rk_dat$rating_resp=factor(rk_dat$rating_resp, levels=c("R", "K", "N"))

rk_rates = as.data.frame(with(rk_dat, table(rating_resp, item_type, test_type, ID)))

rk_rates$prop = rk_rates$Freq/N

rk_means = aggregate(prop ~ rating_resp+item_type+test_type, data = rk_rates, FUN = mean)

# plot
par(mfrow=c(2,2), mar=c(.5,.5,0,0), oma=c(4,4,2,2))

items = c("word", "nonword")
tests = c("old", "new")
ids = unique(rk_rates$ID)

for (i in 1:2){ # test
  for (j in 1:2){ # item
    plot(NA, xlim=c(.5, 3.5), ylim=c(0,1), xlab="", ylab="", axes=F)
    box()
    if (j==1){
      axis(2)
    }else{
        mtext(text = tests[i], side = 4)
      }
    if (i==2){
      axis(1, at = 1:3, labels = levels(rk_rates$rating_resp))
    } else{
      mtext(text = items[j], side = 3)
      }
    
    lapply(X = ids, function(x) with(subset(rk_rates, test_type==tests[i]&item_type==items[j]&ID==x), points(as.numeric(rating_resp), prop, type='b', col='grey')))
    
    with(subset(rk_means, test_type==tests[i]&item_type==items[j]), points(as.numeric(rating_resp), prop, type='b', pch=16))
    
    with(subset(rk_means, test_type==tests[i]&item_type==items[j]), text(x=1:3, y = .9, labels = round(prop, 2)))
  }
}
mtext(text = paste0("N = ", length(unique(rk_dat$ID))), side = 1, line = 2.5, outer=T)

dev.copy(pdf, paste0("MCAL_RK_plot", Sys.Date(), ".pdf"), width=5, height=5)
dev.off()
