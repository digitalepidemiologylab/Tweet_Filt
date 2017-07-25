from tweet_filt import run_all, fanout_gzworker

run_all("Sample/", "(monkey OR banana)", "text", True, "text")
# fanout_gzworker("Sample/20140417/", "(monkey OR banana)", "text", True)
