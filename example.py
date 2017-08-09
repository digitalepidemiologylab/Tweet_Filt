from tweet_filt import run_all, fanout_gzworker
# import time

condition = "(vaccine OR vaccinat) AND ((((((((((vaccine OR vaccinat) OR immunise) OR immunisation) OR jab) OR shot) OR shots) OR booster) OR boosters) AND (((((((((((((((((((((((((((((((((((((((((((((((((((((injection OR harm) OR danger) OR toxic) OR safe) OR safety) OR unsafe) OR unnecessary) OR ineffective) OR doubt) OR hesitant) OR hesitancy) OR concern) OR die) OR deaths) OR paralyse) OR paralysed) OR sick) OR infertile) OR fertility) OR injured) OR injuries) OR (side AND effects)) OR autism) OR autistic) OR link) OR proof) OR controversy) OR controversies) OR myth) OR hoax) OR scam) OR truth) OR lie) OR child) OR children) OR baby) OR babies) OR kid) OR kids) OR school) OR schools) OR consent) OR boycott) OR (drug AND companies)) OR (pharmaceutical AND companies)) OR (big AND pharma)) OR pfizer) OR (boko AND haram)) OR government) OR $WHO$) OR ((international AND health) AND agencies)) OR $NGO$) OR $NHS$)) OR ((((((((((meningitis) OR (yellow AND fever)) OR (herd"
condition = condition + " AND immunity)) OR $MenAfriVac$) OR (anti AND vaxxers)) OR vaxxed) OR wakefield) OR overvaccinate) OR undervaccinate) OR unvaccinated))"
# tic = time.time()
run_all("/mount/SDD/testbed/", condition, "text", True, None, "txt")
# toc = time.time()
# print(toc - tic)
# fanout_gzworker("Sample/20140417/", "(monkey OR banana)", "text", True)
