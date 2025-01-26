import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
text ="""Nature is an inherent character or constitution,[1] particularly of the ecosphere or the universe as a whole. In this general sense nature refers to the laws, elements and phenomena of the physical world, including life. Although humans are part of nature, human activity or humans as a whole are often described as at times at odds, or outright separate and even superior to nature.[2]
During the advent of modern scientific method in the last several centuries, nature became the passive reality, organized and moved by divine laws.[3][4] With the Industrial revolution, nature increasingly became seen as the part of reality deprived from intentional intervention: it was hence considered as sacred by some traditions (Rousseau, American transcendentalism) or a mere decorum for divine providence or human history (Hegel, Marx). However, a vitalist vision of nature, closer to the pre-Socratic one, got reborn at the same time, especially after Charles Darwin.[2]
Within the various uses of the word today, "nature" often refers to geology and wildlife. Nature can refer to the general realm of living plants and animals, and in some cases to the processes associated with inanimate objects—the way that particular types of things exist and change of their own accord, such as the weather and geology of the Earth. It is often taken to mean the "natural environment" or wilderness—wild animals, rocks, forest, and in general those things that have not been substantially altered by human intervention, or which persist despite human intervention. For example, manufactured objects and human interaction generally are not considered part of nature, unless qualified as, for example, "human nature" or "the whole of nature". This more traditional concept of natural things that can still be found today implies a distinction between the natural and the artificial, with the artificial being understood as that which has been brought into being by a human consciousness or a human mind. Depending on the particular context, the term "natural" might also be distinguished from the unnatural or the supernatural."""
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    #print(word_freq)
                
    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    print(word_freq)
    
    sent_tokens = [sent for sent in doc.sents]
    print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    #print(sent_scores)
                    
    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    #print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("Length of original text ",len(text.split(' ')))
    #print("Length of summary text ",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))