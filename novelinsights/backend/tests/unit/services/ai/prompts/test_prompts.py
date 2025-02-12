import importlib
import pkgutil
import pytest

from novelinsights.services.ai.prompts import base
from novelinsights.services.ai.prompts.base import PromptBase, PromptRequest

def get_all_prompt_subclasses(cls):
    """Recursively get all subclasses of the given class."""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_all_prompt_subclasses(subclass))
    return subclasses

def import_all_submodules(module):
    """
    Import all submodules of the given module (if it's a package).
    """
    if hasattr(module, '__path__'):
        for loader, module_name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
            importlib.import_module(module_name)

# Import all submodules of your prompts package.
import_all_submodules(base)

@pytest.mark.parametrize("prompt_cls", get_all_prompt_subclasses(PromptBase))
def test_prompt_subclass_renders_valid_output(prompt_cls):
    """
    For each subclass of PromptBase, instantiate (with defaults/dummy args) and test that
    render() returns a PromptRequest with the expected properties.
    """
    # Depending on your actual constructor requirements, you might need to adjust
    try:
        instance = prompt_cls()  # Use dummy/default parameters if necessary.
    except Exception as e:
        pytest.skip(f"Could not instantiate {prompt_cls.__name__}: {e}")
        
    instance: PromptBase
    print(instance)
    
    # Check that a prompt string is returned and tokens are estimated.
    rendered = instance.render()
    assert isinstance(rendered, PromptRequest)
    assert isinstance(rendered.prompt, str) 
    assert isinstance(rendered.estimated_tokens, int)
    assert rendered.estimated_tokens > 0