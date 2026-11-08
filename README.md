# youtube-transcript-analyser
This project test various algorithms for analysis transcripts downloaded from youtube. 
As a test-case, we used the cut-the-clutter series of videos from the new channel the print. 

Here, we download the transcripts using the youtube-transcript-api.
We use the spacy library and sentence-transformers to analyze the transcripts.

What we are testing:
- Algorithms to summarise the transcripts. This includes td-idf, graph centroid based algorithms.
- Querying about a certain information in the transcript. For example, if we want to know does the speaker mention a specific topic.
