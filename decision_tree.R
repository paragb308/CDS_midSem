
ip_all <- c(ip1, ip2, ip3)
formula <- as.formula(paste("op ~ ", paste(ip_all, collapse= "+")))

#---------------------------------------------------------------
require(tree)
tree_model <- tree(formula, data = train)
plot(tree_model)
text(tree_model)
iris.tree
summary(iris.tree)
#----------------------------------------------------------------
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

tree_model <- rpart(formula, data=train)
fancyRpartPlot(tree_model)

#----------------------------------------------------------------
library(party)

ctree_model <- tree(formula, data = train)
plot(ctree_model)
#----------------------------------------------------------------



