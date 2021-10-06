# WordNet Connector

Connecting Finnish and Hungarian WordNets using synset offsets.

### WordNets

In order to connect them, the [Hungarian](https://github.com/dlt-rilmta/huwn) and [Finnish WordNets](https://www.kielipankki.fi/corpora/finnwordnet/) are needed.
Here, we use the [huwn.xml](https://github.com/dlt-rilmta/huwn/blob/master/huwn.xml) and the [data/rels/fiwn-transls.tsv](https://github.com/frankier/fiwn/blob/master/data/rels/fiwn-transls.tsv) files to create the wordpairs. You can find these files in the `wordnets/` folder in this repository.


### Synset offset

Offset in the Finnish WordNet:
`fi:yXXXXXXXX`

Offset in the Hungarian WordNet:
`ENG30-XXXXXXXX-y`

Where `XXXXXXXX` is an 8 digit, zero-filled decimal integer used in Princeton WordNet 3.0 and `y` is a POS tag.

### POS tags

In WordNet, the POS tag of a synset is marked with one of the following characters:
- n - noun
- v - verb
- a - adjective
- r - adverb (Hungarian uses b instead of r)

The script maps these tags to the Universal POS tag set (https://universaldependencies.org/u/pos/).

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

3. definitions: saves the Hungarian definitions into a file. The file is saved in the output directory as wordnet_definitions_hu.tsv.

4. examples: saves the Hungarian example sentences into a file. The file is saved in the output directory as wordnet_examples_hu.tsv.

5. all: do all of the above.


### Output


The output is always a tab-separated file.
When using `translations`, the file looks like below:

```
lang1_word  <tab>  lang2_word <tab>  pos_tag  <tab>  offset
```

The output of the `synsets` action looks like the following:

```
pos_tag  <tab>  offset  <tab>  lang_code  <tab>  synset
```

The output of the `definitions` and `examples` actions looks like this:

```
pos_tag  <tab>  offset  <tab>  word  <tab>  sentence
```


### License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
The Hungarian WordNet is licensed under [META-SHARE Commons BY NC ND License v1.0](http://www.meta-net.eu/meta-share/meta-share-licenses/META-SHARE%20COMMONS_BYNCND%20v1.0.pdf).
