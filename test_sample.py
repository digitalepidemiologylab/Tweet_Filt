from tweet_filt import strip_all_entities, strip_links

def test_strip():
    assert strip_all_entities(strip_links("This is a @test")) == "This is a"
