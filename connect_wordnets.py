#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""WordNet connector.

Usage:
    connect_wordnets.py translations [--console]
    connect_wordnets.py synsets [--console]
    connect_wordnets.py definitions [--console]
    connect_wordnets.py examples [--console]
    connect_wordnets.py all [--console]
    connect_wordnets.py test
    connect_wordnets.py -h | --help

Options:
    -h --help   Show this screen.
    --console    Write to console.
"""

import os, re
from docopt import docopt
import xml.etree.ElementTree as ET
from collections import defaultdict


def get_id(raw_id, pos_needed=False):
    offset = re.search(r'.*(.)([0-9]{8})', raw_id)
    if offset:
        if pos_needed:
            return offset.group(2), offset.group(1)
        return offset.group(2)
    return None


def pos2ud(pos):
    return {'n' : 'NOUN', 'v' : 'VERB', 'b' : 'ADV', 'a' : 'ADJ'}[pos]


def connecting_wordnets(lang1, lang2, lang1_name, lang2_name):
    connected_wordnets = defaultdict(dict)
    synset_offsets = set(lang1.keys()).intersection(set(lang2.keys()))
    for offset in synset_offsets:
        lang1_pos = lang1[offset] 
        lang2_pos = lang2[offset]
        poses = set(list(lang1_pos.keys()) + list(lang2_pos.keys()))
        for pos in poses:
            if pos not in connected_wordnets[offset]:
                connected_wordnets[offset][pos] =  {lang1_name : set(), lang2_name : set()}
            try:
                connected_wordnets[offset][pos][lang1_name].update(lang1[offset][pos])
            except KeyError:
                pass
            try:
                connected_wordnets[offset][pos][lang2_name].update(lang2[offset][pos])
            except KeyError:
                pass
    return connected_wordnets


def extract_fin(fi_wn):
    fin_vocab = {}
    with open(fi_wn, encoding='utf-8') as fi:
        for line in fi:
            data = line.split('\t')
            if len(data) == 6:
                fid, fword = data[0:2]
                if data[4] != 'synonym':
                    continue
                fi_offset, fi_pos = get_id(fid, pos_needed=True)
                if fi_pos == 'r':
                    fi_pos = 'b'
                if fi_offset in fin_vocab:
                    if fi_pos in fin_vocab[fi_offset]:
                        fin_vocab[fi_offset][fi_pos].add(fword)
                    else:
                        fin_vocab[fi_offset][fi_pos] = set([fword])
                else:
                    fin_vocab[fi_offset] = {fi_pos : set([fword])}
    return fin_vocab


def extract_hun(hu_wn):
    hun_vocab = {}
    tree = ET.parse(hu_wn)
    hun_defs = defaultdict(dict)
    hun_examps = defaultdict(dict)
    for synset in tree.getroot():
        huid, hupos = None, None
        huword_list = []
        for element in synset:
            if element.tag == 'ID3':
                huid = element.text
            elif element.tag == 'POS':
                hupos = element.text
            elif element.tag == 'SYNONYM':
                # each synonym tag can have more than one literal element
                for syno_child in element:
                    if syno_child.tag == 'LITERAL':
                        if syno_child.text.startswith('nl_') or syno_child.text.startswith('tnl_'):
                            continue
                        huword_list.append(syno_child.text)
            elif element.tag == 'DEF':
                hudef = element.text
                if not huword_list:
                    continue
            elif element.tag == 'USAGE':
                huexamp = element.text
                if not huword_list:
                    continue
                if huid:
                    hu_offset = get_id(huid)
                    for word in huword_list:
                        if hupos not in hun_examps[hu_offset]:
                            hun_examps[hu_offset][hupos] = dict()
                        if word not in hun_examps[hu_offset][hupos]:
                            hun_examps[hu_offset][hupos][word] = set()
                        hun_examps[hu_offset][hupos][word].add(huexamp)

        if huid and huword_list and hupos:
            hu_offset = get_id(huid)
            if hudef:
                for word in huword_list:
                    if hupos not in hun_defs[hu_offset]:
                        hun_defs[hu_offset][hupos] = dict()
                    if word not in hun_defs[hu_offset][hupos]:
                        hun_defs[hu_offset][hupos][word] = set()
                    hun_defs[hu_offset][hupos][word].add(hudef)
            if hu_offset in hun_vocab:
                if hupos in hun_vocab[hu_offset]:
                    hun_vocab[hu_offset][hupos].update(huword_list)
                else:
                    hun_vocab[hu_offset][hupos] = set(huword_list)
            else:
                hun_vocab[hu_offset] = {hupos : set(huword_list)}
    return hun_vocab, hun_defs, hun_examps


def write_file(script_dir, pairs, hudefs, huexs, type='translations', to_console=False):
    output_file = {
        'synsets'        : 'wordnet_synsets.tsv',
        'translations'   : 'wordnet_wordpairs.tsv',
        'definitions'    : 'wordnet_hu_defs.tsv',
        'examples'       : 'wordnet_hu_examps.tsv',
    }[type]

    foutput = os.path.join(script_dir, 'output', output_file)
   
    if not to_console:
        w = open(foutput, 'w', encoding='utf-8')
    if type == 'translations':
        for offset in pairs:
            for pos in pairs[offset]:
                lang1_words = pairs[offset][pos]['fi']
                lang2_words = pairs[offset][pos]['hu']
                udpos = pos2ud(pos)
                for l1_word in lang1_words:
                    for l2_word in lang2_words:
                        to_print = '{}\t{}\t{}\t{}'.format(l1_word, l2_word, udpos, offset)
                        if to_console:
                            print(to_print)
                        else:
                            w.write(to_print + '\n')
    elif type == 'synsets':
        for offset, worddt in pairs.items():
            for pos in worddt:
                for lang in ['fi', 'hu']:
                    udpos = pos2ud(pos)
                    synsets = '\t'.join(pairs[offset][pos][lang])
                    to_print = '{}\t{}\t{}\t{}'.format(udpos, offset, lang, synsets)
                    if to_console:
                        print(to_print)
                    else:
                        w.write(to_print + '\n')
    elif type == 'definitions':
        if to_console:
            print(write_sentences(hudefs), end='')
        else:
            w.write(write_sentences(hudefs))
    elif type == 'examples':
        if to_console:
            print(write_sentences(huexs), end='')
        else:
            w.write(write_sentences(huexs))

    if not to_console:
        w.close()


def write_sentences(dataset):
    complete_str = ''
    for offset, data in dataset.items():
        for pos, pair in data.items():
            for word, sent_list in pair.items():
                for sent in sent_list:
                    complete_str += '\t'.join([pos2ud(pos), offset, word, sent]) + '\n'
    return complete_str

def main():
    arguments = docopt(__doc__)
    to_console = False
    if arguments['--console']:
        to_console = True
    options = ['translations', 'synsets', 'definitions', 'examples']
    for mode_option in [*options, 'all', 'test']:#['all', 'synsets', 'words', 'test']:
        if arguments[mode_option]:
            mode = mode_option

    script_dir = os.path.dirname(__file__)
    if not os.path.exists('output'):
        os.makedirs('output')
    """
    if mode not in options and mode != 'all' and mode != 'test':
        raise ValueError('ValueError: unknown mode')

    """

    fi_wn = os.path.join(script_dir, 'wordnets', 'finnwordnet', 'rels', 'fiwn-transls.tsv')
    fin_vocab = extract_fin(fi_wn)

    hu_wn = os.path.join(script_dir, 'wordnets', 'huwn.xml')
    hungarian, hudefs, huexs = extract_hun(hu_wn)

    connected_wordnets = connecting_wordnets(fin_vocab, hungarian, 'fi', 'hu')

    if mode == 'test':
        return

    if mode == 'all':
        for opt in options:
            write_file(script_dir, connected_wordnets, hudefs, huexs, type=opt, to_console=to_console)
    else:
        write_file(script_dir, connected_wordnets, hudefs, huexs, type=mode, to_console=to_console)


if __name__ == '__main__':
    main()

