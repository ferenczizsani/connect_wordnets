# WordNet Connector

Connecting Finnish and Hungarian WordNets using synset offsets.

### Synset offset

Offset in the Finnish WordNet:
`fi:yXXXXXXXX`

Offset in the Hungarian WordNet:
`ENG30-XXXXXXXX-y`

Where XXXXXXXX is an 8 digit, zero-filled decimal integer used in Princeton WordNet 3.0 and y is a POS tag.

### POS tags in WordNets:

- n - noun
- v - verb
- a - adjective
- r - adverb (Hungarian uses b instead of r)

### Definitions and example sentences

Only the Hungarian WordNet contains definitions and examples sentences. These can be extracted using the actions described below.

### Usage

The script supports five actions: `translations`, `synsets`, `definitions`, `examples` and `all`.
When using the `--console` option, the output will be put on the console, instead of files.

```
connect_wordnets.py translations [--console]
connect_wordnets.py synsets [--console]
connect_wordnets.py definitions [--console]
connect_wordnets.py examples [--console]
connect_wordnets.py all [--console]
```

1. translations: connects the two WordNets and outputs the word pairs of the connected synsets. The file is saved in the output directory as wordnet_wordpairs.tsv.

2. synsets: outputs the offset, part of speech tag, language code and the elements of a synset. The file is saved in the output directory as wordnet_synsets.tsv.

3. definitions: saves the Hungarian definitions into a file. The file is saved in the output directory as wordnet_hu_defs.tsv.

4. examples: saves the Hungarian example sentences into a file. The file is saved in the output directory as wordnet_hu_examps.tsv.

5. all: do all of the above.


### Output


The output is always a tab-separated file.
When using `translations`, the file looks like below:

```
lang1_word  lang2_word  pos_tag offset
```

The output of the `synsets` action looks like the following:

```
pos_tag offset  lang_code   synset
```

The output of the `definitions` and `examples` actions looks like this:

```
pos_tag offset  word    sentence
```

