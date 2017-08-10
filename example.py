from tweet_filt import run_all
# import time

condition1 = "Banana AND (((Monkey OR Lemur) AND Pet))"

condition2 = "(Vaccinat AND $WHO$) OR (Flu OR Sick)"

run_all("Data/", [condition1, condition2])
