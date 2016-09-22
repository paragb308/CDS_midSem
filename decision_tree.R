
ip_all <- c(ip1, ip2, ip3)
formula <- as.formula(paste("op ~ ", paste(ip_all, collapse= "+")))

#---------------------------------------------------------------
require(tree)
tree_model <- tree(formula, data = train)
plot(tree_model)
text(tree_model)
summary(tree_model)
predicted <- predict(tree_model, test)
#----------------------------------------------------------------
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

rtree_model <- rpart(formula, data=train)
fancyRpartPlot(rtree_model)
predicted <- predict(rtree_model, test)

#----------------------------------------------------------------
library(party)

ctree_model <- tree(formula, data = train)
plot(ctree_model)
predicted <- predict(ctree_model, test)
#----------------------------------------------------------------



