from typing import Set, Generator


class WordGenerator:
    @staticmethod
    def generate_words(alphabet: Set[str], max_length: int) -> Generator[str, None, None]:
        alpha_list = list(alphabet)
        k = len(alpha_list)

        if k == 0:
            total_words = 1
        elif k == 1:
            total_words = max_length + 1
        else:
            total_words = (k ** (max_length + 1) - 1) // (k - 1)

        if total_words > 10 ** 5:
            raise ValueError("Слишком большое количество возможных слов")

        def _backtrack(current_word: str, current_len: int) -> Generator[str, None, None]:
            yield current_word
            if current_len >= max_length:
                return
            for symbol in alpha_list:
                yield from _backtrack(current_word + symbol, current_len + 1)

        yield from _backtrack("", 0)
