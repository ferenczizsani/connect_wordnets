# WordNet Connector

Connecting Finnish and Hungarian WordNets using offsets.

### Offset

Offset in the Finnish WordNet:
`fi:yXXXXXXXX`

Offset in the Hungarian WordNet:
`ENG30-XXXXXXXX-y`

Where XXXXXXXX is the WordNet 3.0 offset and y is a POS tag.

### POS tags in WordNets:

- n - noun
- v - verb
- b - adverb (Finnish uses r instead of b)
- a - adjective

### Usage

The script supports five actions: `translations`, `synsets`, `definitions`, `examples` and `all`.
When using the `--console` option, the output will be put on the console, instead of files.

```python3 connect_wordnets.py translations [--console]```

```python3 connect_wordnets.py synsets [--console]```

```python3 connect_wordnets.py definitions [--console]```

```python3 connect_wordnets.py examples [--console]```

```python3 connect_wordnets.py all [--console]```

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

The wordnet_synsets.tsv file looks like the following:

```
pos_tag offset  lang_code   synset
```

The wordnet_hu_defs.tsv and the wordnet_hu_examp.tsv look like this:

```
pos_tag offset  word    sentence
```

