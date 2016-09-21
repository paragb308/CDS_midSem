#Random Forest function
#randomForest



ip_all <- c(ip1, ip2, ip3)
formula <- as.formula(paste("op ~ ", paste(ip_all, collapse= "+")))

# Conventional Random Forest
set.seed(415)
fit_forest <- randomForest(formula, data=train, importance=TRUE, ntree=200)
plot(fit_forest)

#Variable Importance
varImpPlot(fit_forest, sort = T, main="Variable Importance", n.var=10)


#cForest: conditional inference trees
set.seed(415)
fit_cforest <- cforest(formula, data = train, controls = cforest_unbiased(ntree=50, mtry=3)) 

#Variable Importance
# imp_by_Gini <- "MeanDecreaseGini" 
imp_Gini <- importance(fit_cforest, type=1)

#imp_by_Accuracy <- "MeanDecreaseAccuracy"
imp_Accu <- importance(fit_cforest, type=2)


#Prediction: 
predict_ <- predict(fit_forest ,test)
predict_ <- predict(cforest ,test)


#-----------------------------------------------------
#References:
#https://www.kaggle.com/binilkuriachan/titanic/titanic-random-forest

