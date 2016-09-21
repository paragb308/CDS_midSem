#Random Forest function
#randomForest



ip_all <- c(ip1, ip2, ip3)
formula <- as.formula(paste("op ~ ", paste(ip_all, collapse= "+")))

# Conventional Random Forest
set.seed(415)
fit_forest <- randomForest(formula, data=train, importance=TRUE, ntree=200)

#Variable Importance
varImpPlot(fit_forest, sort = T, main="Variable Importance", n.var=10)


#cForest: conditional inference trees
set.seed(415)
fit_cforest <- cforest(formula, data = train, controls = cforest_unbiased(ntree=50, mtry=3)) 

#Variable Importance
#
imp <- importance(fit_cforest, type=1)
imp <- importance(fit_cforest, type=2)

#plot for variable importance
varImportance <- data.frame(Variables = row.names(importance), 
                            Importance = round(importance[ ,'MeanDecreaseGini'],2))



#By Gini
#By Accuracy



#-----------------------------------------------------
#References:
#https://www.kaggle.com/binilkuriachan/titanic/titanic-random-forest

