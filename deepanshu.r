#start-------------------------------------------------------------------------------------------

read_csv<-function(filepath){
  data_retrived<-read.csv(filepath)
  return(data_retrived)
}

load_library<-function(lib_name){   #check before calling library() whether package is installed
  if(!is.element(lib_name, installed.packages()[,1])){
    install.packages(lib_name)
  }
  else{
    library(lib_name,character.only = TRUE)
  }
}
######
#missing_value<-function(dataset){   #Dummy function
#}
######

data_split<-function(dataset){
  return(sample.split(dataset,SplitRatio = 0.70))
}

na_test <-  function (data_set) {
  w <- sapply(x, function(x)all(is.na(x)))
  if (any(w)) {
    stop(paste("All NA in columns", paste(which(w), collapse=", ")))
  }
}
cat_2_num<-function(train){
      train$FRONTAGE_ROAD<- as.character(train$FRONTAGE_ROAD)
      train$FRONTAGE_ROAD[train$FRONTAGE_ROAD == "Yes"] <- 1
      train$FRONTAGE_ROAD[train$FRONTAGE_ROAD == "No"] <- 0
      train$FRONTAGE_ROAD[train$FRONTAGE_ROAD == "Unable to determine"] <- 11/1170
      train$FRONTAGE_ROAD<- as.numeric(train$FRONTAGE_ROAD)
      
      train$NUM_PARKING_SPACES<- as.character(train$NUM_PARKING_SPACES)
      train$NUM_PARKING_SPACES[train$NUM_PARKING_SPACES == "Greater than 10"] <- 2
      train$NUM_PARKING_SPACES[train$NUM_PARKING_SPACES == "0 (e.g., street parking, structure/lot more than 2 doors down, parking in back)"] <- 0
      train$NUM_PARKING_SPACES[train$NUM_PARKING_SPACES == "Between 1 and 10"] <- 1
      train$NUM_PARKING_SPACES[train$NUM_PARKING_SPACES == "Unable to determine"] <- ((2*893)+(1*193))/(893+77+193)
      train$NUM_PARKING_SPACES <- as.numeric(train$NUM_PARKING_SPACES)
      
      train$SIGNAGE_VISIBILITY_IND<-as.character(train$SIGNAGE_VISIBILITY_IND)
      train$SIGNAGE_VISIBILITY_IND[train$SIGNAGE_VISIBILITY_IND == "Yes"] <- 1
      train$SIGNAGE_VISIBILITY_IND[train$SIGNAGE_VISIBILITY_IND == "No"] <- 0
      train$SIGNAGE_VISIBILITY_IND[train$SIGNAGE_VISIBILITY_IND %in% c("Unable to determine","Yes No") ] <- 42/1170
      train$SIGNAGE_VISIBILITY_IND <- as.numeric(train$SIGNAGE_VISIBILITY_IND)
      return(train)
}

###################################################################################################

fileTrain<-"S:/Datasets/CDS/midsem/storeTrain.csv"
fileTest<-"S:/Datasets/CDS/midsem/storeTest.csv"

# load_library("caTools")
# load_library("corrplot")
# load_library("xgboost")
# load_library("hydroGOF")
train<-read_csv(fileTrain)
test<-read_csv(fileTest)
train<-cat_2_num(train)
train<-na.omit(df_train)

sampling_data=data_split(train) #splits training data
train<-subset(train,sampling_data==TRUE)  # 66% of the training data
cv<-subset(train,sampling_data==FALSE) # remaining 34% of training data
cat_vars<-c("U_CITY","U_STATE","CENSUS_REGION","CENSUS_DIVISION","URBANICITY")
features<-setdiff(names(train),cat_vars)
train<-train[features]
cv<-cv[features]
