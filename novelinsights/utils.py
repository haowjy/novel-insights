from typing import Callable

try:
    import tiktoken
    
except ImportError:
    pass

def simple_token_estimator(text: str) -> int:
    """Simple token estimator that estimates the number of tokens based on:
    
    1 token ~= 4 chars in English
    1 token ~= 3/4 words
    
    and taking the average of the two.

    Args:
        text (str): The text to estimate the number of tokens in.

    Returns:
        int: The estimated number of tokens in the text.
    """
    word_count = len(text.split(" "))
    char_count = len(text)
    tokens_count_word_est = word_count / 0.75
    tokens_count_char_est = char_count / 4.0
    return (tokens_count_word_est + tokens_count_char_est) / 2

def GET_ESTIMATOR(source: str='simple', encoding_name:str='cl100k_base') -> Callable[[str], int]:
        """Use the tiktoken library to estimate the number of tokens in a text.
        See [tiktoken](https://github.com/openai/tiktoken) for more information. 

        Args:
            source (str, optional): Source of the estimator. I.e. "openai" or "tiktoken" for the tiktoken library. 'simple' for a simple estimator. Defaults to 'simple'.
            encoding_name (str, optional): The tiktoken encoding name used to count and estimate the number of tokens. Defaults to 'cl100k_base'.

        Returns:
            Callable[[str], int]: A function that takes a string and returns the number of tokens in the string.
        """
        if source.lower() == 'simple':
            return simple_token_estimator
        try:
            if source.lower() == 'openai' or source.lower() == 'tiktoken':
                encoding = tiktoken.get_encoding(encoding_name=encoding_name)
                return lambda x: len(encoding.encode(x))
        except ImportError:
            pass