import tweet_filt as tf

def test_strip():
    assert tf.strip_all_entities(tf.strip_links("This is a @test")) == "This is a"
