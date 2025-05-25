# get the sentence
# pick a few words based on its length (or 10 words btn stutters)
    # the words must have l1 == consonant and l2 == vowel
    # minimum word length is 2
# stutter the words
# return the sentence with updated words
import eng_to_ipa as ipa
import pyphen as separator
###

import re
import random

def is_bad_lx(word):
    # check if the first letter is in a list of letters that change sounds in some situations
    # e.g., "c" in "century" v "category" or "g" in "giraffe" v "goat"
    return word[0].lower() in ['c', 'g', 's', 'x', 'y']

def l2_is_vowel(word):
    # Check if the second character is a vowel
    if len(word) > 1:
        return word[1].lower() in 'aeiou'
    return False

def lx_is_cnsnt(word, index):
    # return if the Xth letter of the word is a consonant
    if len(word) > 0:
        return word[index-1].lower() not in 'aeiou'
    return None

def remove_trailing_consonants(word):
    # remove trailing consonants from the word
    # e.g., "cat" -> "ca"
    while word[-1] in 'bcdfghjklmnpqrstvwxyz':
        word = word[:-1]
    return word

def get_phoneme(word):
    # convert the word to phonemes
    res = ipa.convert(word)
    res = remove_trailing_consonants(res)
    # deal with double phonemes e.g., wɪθ -> wɪ and ʤoʊ -> ʤo
    res = res[:2] if len(res) > 2 else res
    return res

def get_first_syllable(word):
    # other available methods:
    # dic.wrap('autobandventieldopje', 11)
    # for pair in dic.iterate('Amsterdam'):
    #     print(pair)
    separator.language_fallback('nl_NL_variant1')
    dic = separator.Pyphen(lang='nl_NL')
    word_with_hyphens = dic.inserted(word)
    res = word_with_hyphens.split('-')[0]
    return res

def stutter_one_word(phoneme, word):
    """Stutters a single word by repeating the first phoneme."""
    return f"||{phoneme}||{word}||"


def get_stutter(sentence):
    """Stutters words that are 8-10 words apart in a sentence."""
    words = sentence.split()
    stuttered_words = []
    
    # Start with a random offset between 0 and 
    sentence_length = len(words)
    base_stutter_gap = max(5, sentence_length // 10)  # Adjust based on text length
    next_stutter = random.randint(0, base_stutter_gap)
    # next_stutter = 1
    
    for i, word in enumerate(words):
        # if the word length is less than 3, or l2_is_vowel(word) is False, append the word to stuttered_words
        # else, append the stuttered word to stuttered_words, and increment next_stutter by a random number between 6 and 10
        if i == next_stutter:
            # Check if the word is a noun or verb
            if  lx_is_cnsnt(word,1) or (len(word) > 1 and l2_is_vowel(word)):
            # if len(word) > 2 and lx_is_cnsnt(word,3) and not is_bad_lx(word) :
                # Get the first syllable of the word
                first_syllable = get_first_syllable(word)
                # Get the phoneme of the word
                phoneme = get_phoneme(first_syllable)
                # Stutter the word
                stuttered_word = stutter_one_word(phoneme, word)
                stuttered_words.append(stuttered_word)
                # Adjust next stutter gap dynamically
                next_stutter += random.randint(base_stutter_gap, base_stutter_gap + 5) 
                # print(f"i: {i} || word: {word} ")
                # print(f"inext: {next_stutter} || word: {word} ")
            else:
                next_stutter += 1
                stuttered_words.append(word)
                # print(f"enext: {next_stutter} || word: {word} ")
        elif word.endswith('ed') and random.randint(1, 2) == 1:# word ends with 'ed'
            stuttered_words.append(f"{word}ed")
        else:
            stuttered_words.append(word)
        # print(f"i: {i} || word: {word} \nstuttered_word: {stuttered_words}\n")
    return " ".join(stuttered_words)

def main():
    # Example usage:
    sentence = "In the beautiful suburb of Hout Bay, Sipho, a recent transplant from Johannesburg, feels isolated and struggles to connect with his new surroundings and the local community."
    stuttered_sentence = get_stutter(sentence)
    print(get_phoneme(get_first_syllable("century")))
    print(stuttered_sentence)
    cnsnt = 0
    vowel = 0
    badxtr = 0
    
    for word in sentence.split():
        cnsnt += 1 if lx_is_cnsnt(word,1) else 0
        vowel += 1 if l2_is_vowel(word) else 0
        badxtr += 1 if is_bad_lx(word) else 0
    print (f"cnsnt: {cnsnt} || vowel: {vowel} || badxtr: {badxtr} || total: {len(sentence.split())}")


if __name__ == "__main__":
    main()