import torch
import torch.nn as nn
from datasets import load_dataset
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.trainers import WordLevelTrainer
from tokenizers.pre_tokenizers import whitespace
from pathlib import Path

def get_all_sentences(ds , lang):
    for item in ds:
        yield item['translation'][lang]


def get_or_build_tokenizer(config , ds , lang):
    #
    tokenizer_path = Path(config['tokenizer_file'].format(lang))
    if not Path.exists(tokenizer_path):
        tokenizer = Tokenizer(WordLevel(unk_tokens = '[UNK]'))
        tokenizer.pre_tokenizer = Whitespace()
        trainer = WordLevelTrainer(special_tokens = ["[UNK]" , "[PAD]" , "[SOS]" , "[EOS]"] , min_frequency = 2)
        tokenizer.train_from_iterator(get_all_sentences(ds , lang) , trainer = trainer)
        tokenizer.save(str(tokenizer_path))
    else:
        tokenizer = Tokenizer.from_file(str(tokenizer_path))
    return tokenizer


def get_ds(config):
    ds_raw = load_dataset('opus_books' , f'{config["lang_src"]}')