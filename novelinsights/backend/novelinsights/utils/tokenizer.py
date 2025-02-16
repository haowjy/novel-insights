from typing import Callable

try:
    import tiktoken
except ImportError:
    pass

try:
    from llama_index.core.utils import Tokenizer
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
    return int((tokens_count_word_est + tokens_count_char_est) / 2)

def get_estimator(tokenizer: 'str | Tokenizer' = 'simple') -> Callable[[str], int]:
    """estimate the number of tokens in a text.

    Args:
        source (str, optional): Source of the estimator. I.e. "openai" or "tiktoken" for the tiktoken library. 'simple' for a simple estimator. Defaults to 'simple'.
        encoding_name (str, optional): The tiktoken encoding name used to count and estimate the number of tokens. Defaults to 'cl100k_base'.

    Returns:
        Callable[[str], int]: A function that takes a string and returns the number of tokens in the string.
    """
    if tokenizer == 'simple' or tokenizer is None:
        return simple_token_estimator
    
    if isinstance(tokenizer, str):
        try:
            encoding = tiktoken.get_encoding(tokenizer)
            return lambda x: len(encoding.encode(x))
        except: # ImportError or AttributeError
            return simple_token_estimator
    
    elif isinstance(tokenizer, Tokenizer): # why is a string a tokenizer???
        return lambda x: len(tokenizer.encode(x))
    
    # if all else, just use the simple estimator
    return simple_token_estimator


class TokenEstimator:
    def __init__(self, tokenizer: 'str | Tokenizer' = 'simple'):
        self.tokenizer = get_estimator(tokenizer)
    
    def estimate(self, text: str) -> int:
        return self.tokenizer(text)
    
    @staticmethod
    def simple(text: str) -> int:
        return simple_token_estimator(text)
