############################dividing the dataset###################
sampling_data=sample.split(LC_train,SplitRatio = 0.66) #splits training data
Train<-subset(LC_train,sampling_data==TRUE)  # 66% of the training data
CV<-subset(LC_train,sampling_data==FALSE) # remaining 34% of training data


#######################forming the variable array##############
DiseaseTreat <- paste("Disease", c(4,6),"Treat", sep="")
Ques <- paste("Ques", c(2,3,5), sep="")
Smoke <- paste("Smoke", c(2,3,4), sep="")

allvar_clust1 <- c(Factor,DiseaseHis,DiseaseHisTimes,DiseaseStage, LungFunct, Disease,DiseaseTimes, DiseaseTreat, Ques, Smoke)
fmla <- as.formula(paste("Lung_Cancer ~ ", paste(allvar_clust1, collapse= "+")))
#OR
features.na <- setdiff(names(train), c("Id","SalePrice", "Alley","PoolQC","Fence","MiscFeature","FireplaceQu","LotFrontage"))
train_na <- train[features.na]

#######################logistic regression######################
log2 = glm(fmla, data = LC, family=binomial)
summary(log2)
ptest2 = predict(log2, type="response", newdata=test)

########################pca###############################
LC_pca <- LC[,colnames(LC)%in%allvar]
princ <- prcomp(LC_pca,center = TRUE,scale. = TRUE) #remove the respose variable
Train <- as.data.frame(predict(princ,LC_pca),stringsAsFactors = FALSE)
Train$y <- LC$Lung_Cancer

Test <- as.data.frame(predict(princ,test_pca), stringsAsFactors = FALSE)
Test$y <- test$Lung_Cancer


###############################liblinear#######################
model <- LiblineaR(LC_train[allvar], LC_train[,2], type = 6)

#applying the above model on test dataset and setting the 'proba' parameter as TRUE
#to return the probabilities
test_predict <- predict(model,LC_test[allvar],proba=TRUE)

#save the probabilities in separate dataset
probabilities <- test_predict$probabilities


######################clustering#######################

km=kmeans(LC[3:62],centers = 2)
str(km)

km.kcca = as.kcca(km, LC[3:62])
clusterTrain = predict(km.kcca)

mean(km$cluster)
mean(clusterTrain)

clusterTest = predict(km.kcca, newdata=test[3:62])
str(clusterTest)
table(clusterTest)
