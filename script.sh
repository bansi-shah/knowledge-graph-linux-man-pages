java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../man7.org/linux/man-pages/man0/stdlib.h.0p.html -outputFormat tsv -outputFile ../std/stdlib.h.0p.tag
java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../man7.org/linux/man-pages/man0/ctype.h.0p.html -outputFormat tsv -outputFile ../std/ctype.h.0p.tag
java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../man7.org/linux/man-pages/man0/pthread.h.0p.html -outputFormat tsv -outputFile ../std/pthread.h.0p.tag
java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../man7.org/linux/man-pages/man0/signal.h.0p.html -outputFormat tsv -outputFile ../std/signal.h.0p.tag
java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../man7.org/linux/man-pages/man0/strings.h.0p.html -outputFormat tsv -outputFile ../std/strings.h.0p.tag


