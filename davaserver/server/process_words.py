def extract_words_from_text(text: str) -> list[str]:
    return text.splitlines()


def longest_word(words: list) -> str:
    longest= ""
    for word in words:
        if len(word) > len(longest):
            longest = word

    return longest


def shortest_word(words: list) -> str:
    shortest = words[0]
    for word in words:
        if len(word) < len(shortest):
            shortest = word

    return shortest


def order_lexicographically(words: list[str]) -> str:
    sorted_words = sorted(words)
    return "\n".join(sorted_words)


def count_vowels_and_consonants(words: list[str]) -> str:
    vowels = "aeiouAEIOU"
    lines = []

    for word in words:
        vowel_count = 0
        consonant_count = 0

        for letter in word:
            if letter in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

        line = f"{word}: vowels={vowel_count}, consonants={consonant_count}"
        lines.append(line)

    return "\n".join(lines)


def longest_consecutive_consonants(words: list[str]) -> str:
    vowels = "aeiouAEIOU"
    longest_consonant_word = ""
    longest_consonant_count = 0

    for word in words:
        current_count = 0
        longest_in_word = 0

        for letter in word:
            if letter not in vowels:
                current_count += 1
                if current_count > longest_in_word:
                    longest_in_word = current_count
            else:
                current_count = 0

        if longest_in_word > longest_consonant_count:
            longest_consonant_count = longest_in_word
            longest_consonant_word = word

    return f"{longest_consonant_word}: {longest_consonant_count} consecutive consonants"


def process_words(words: list[str]) -> dict[str, str]:
    return {
        "longest_word.txt": longest_word(words),
        "shortest_word.txt": shortest_word(words),
        "order_lexicographically.txt": order_lexicographically(words),
        "count_vowels_and_consonants.txt": count_vowels_and_consonants(words),
        "longest_consecutive_consonants.txt": longest_consecutive_consonants(words),
    }
