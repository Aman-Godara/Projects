import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S P S | S Conj S | S Conj VP
NP -> N | Det N | NP PP | AdjP NP | Det AdjP
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
PP -> P NP
AdjP -> Adj N | Adj AdjP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    temp_out = nltk.tokenize.word_tokenize(sentence)
    out = []
    for i in range(len(temp_out)):
        word = temp_out[i]
        new_word = ""
        for character in word:
            if 97 <= ord(character) <= 122:
                new_word += character
            elif 65 <= ord(character) <= 90:
                new_word += chr(ord(character) + 32)
            else:
                new_word = ""
                break
        if new_word:
            out.append(new_word)

    return out


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    out = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            np_found = 0
            for sub_subtree in subtree.subtrees():
                if sub_subtree.label() == "NP":
                    np_found += 1
            if np_found == 1:
                out.append(subtree)
    return out


if __name__ == "__main__":
    main()
