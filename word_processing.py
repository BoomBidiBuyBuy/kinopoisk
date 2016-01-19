# coding=utf-8
def word_remove_symbols(word):
    letters = list(u".,!?-()$#;:+=%^&*<>\"'[]{}\\/~—«»")

    cnt = 0

    for letter in letters:
        if word.find(letter) != -1:
            word = word.replace(letter, '')
            cnt += 1

    return word, cnt

def norm(word, morph):
    return set(map(lambda w: w.normal_form, morph.parse(word)))