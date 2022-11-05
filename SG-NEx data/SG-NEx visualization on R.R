library(dplyr)
library(tidyverse)
library(ggplot2)

modified <- read_csv('modified.csv') #using modified_csv from jupyter notebook
modified <- subset(modified, select = -c(...1) )
modified_test <- subset(modified, select = c('1-mer', '2-mer', '5-mer'))

modified_test$`1-mer` <- recode(modified_test$`1-mer`, '1' = "A", '2' = "G", '3' = "U")
modified_test$`2-mer` <- recode(modified_test$`2-mer`, '1' = "A", '2' = "G")
modified_test$`5-mer` <- recode(modified_test$`5-mer`, '1' = "A", '2' = "C", '3' = "T")
q2 <- mutate(modified_test, `1-mer` = factor(`1-mer`, levels = c("A", "G", "U")))

ggplot(q2) + geom_bar(aes(x = `1-mer`))

ggplot(q2) + geom_bar(aes(x = `1-mer`, fill = Churn), position = "fill") +
  facet_wrap(~InternetService) +
  theme(legend.position = "bottom") +
  labs(title = "Proportion of churn is higher for fibre optic users.")


specie <- c(rep("sorgho" , 3) , rep("poacee" , 3) , rep("banana" , 3) , rep("triticum" , 3) )
condition <- rep(c("normal" , "stress" , "Nitrogen") , 4)
value <- abs(rnorm(12 , 0 , 15))
data <- data.frame(specie,condition,value)

positions <- c('first', 'second', 'fifth')
A <- c(2654, 3186, 4037)
G <- c(22584, 23238, 0)
U <- c(916, 0, 0)
C <- c(0,0,2313)
T <- c(0,0,20074)
df <- data.frame(positions, A, G, U, C, T)
df$positions = factor(df$positions,levels = c("first", "second", "fifth"))
df %>%
  pivot_longer(-positions, names_to = "Nucleotides") %>%
  ggplot(aes(positions, value, fill = Nucleotides)) +
  geom_col() + 
  scale_fill_brewer(palette="Set1") + 
  labs(title = 'Nucleotide counts of non-fixed positions modified by m6Anet', y = 'Counts', x = 'Positions')
