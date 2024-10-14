from typing import Callable
import json

try:
    import tiktoken
except ImportError:
    pass

from llama_index.core.utils import Tokenizer

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

def get_estimator(tokenizer: str | Tokenizer = 'simple') -> Callable[[str], int]:
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

import json
def parse_json(json_str:str) -> dict:
    """Parse the JSON string into a dictionary. The JSON should be the last to be surrounded by backticks.

    Args:
        json_str (str): JSON string to be parsed.

    Returns:
        dict: Parsed JSON dictionary.
    """
    json_str = json_str.strip()
    if json_str.startswith("```json") and json_str.endswith("```"):
        json_str = json_str[7:-3].strip()
    return json.loads(json_str)

def parse_json(json_str:str) -> dict:
    """ Parse the last json in the response"""
    
    json_str = json_str.strip()
    # find the last ``` in the string
    end = json_str.rfind("```")
    print(end)
    if end == -1:
        return None
    # find the start of the based on the second last ``` in the string
    start = json_str.rfind("```", 0, end)
    
    if start == -1:
        return None

    # handle the case where there is a ```json\n and ``` in the response
    if json_str[start+3:start+7] == "json":
        start += 7
    else:
        start += 3
    # return json.loads(json_str[start:end])
    try:
        return json.loads(json_str[start:end])
    except json.JSONDecodeError:
        return None
    
# def parse_json(response:str, json_index:int=0) -> dict:
#     # json is between ``` and ``` in the response, possibly with a ```json and ``` as well
#     # the json_index json surrounded by ``` is the one we want
#     # repeatedly find ``` until we find the json_index-th one
#     # use response.find
#     """ Find the json_index-th json in the response

#     Args:
#         response (str): The string response from the API
#         json_index (int, optional): index of the json to find. Defaults to 0.

#     Returns:
#         dict: The json object. Could error if the json is not valid
    
#     Throws:
#         ValueError: If the json is not
#     """
#     start = -1
#     count = 0
#     while count < json_index+1:
#         start = response.find("```", start+1)
#         if start == -1:
#             break
#         count += 1
#     # find the end of the json
#     end = response.find("```", start+1)
 
#     if start == -1 or end == -1:
#         return None
    
#     # handle the case where there is a ```json\n and ``` in the response
#     if response[start+3:start+7] == "json":
#         start += 7

#     return json.loads(response[start:end])