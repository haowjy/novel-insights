from ebooklib import epub

from bs4 import BeautifulSoup
from bs4.element import Tag

import html2text
H2T = html2text.HTML2Text()
H2T.body_width = 0

import tiktoken
TIK_ENCODING = tiktoken.get_encoding("cl100k_base")
def TOK_COUNT(text:str) -> int:
    return len(TIK_ENCODING.encode(text))


from itertools import zip_longest

def has_text(tag):
    return tag.string is not None and tag.string.strip()

def is_link(element: Tag) -> bool:
    return element.name == 'a'

def only_link_content(element: Tag) -> bool:
    if element.name == 'a':
        return True
    if not hasattr(element, 'contents'):
        return False
    return all(is_link(child) for child in element.contents)

def get_content_between_elements(elem1: Tag, elem2: Tag | None) -> str:
    content_list = []
    current_element = elem1

    while current_element and current_element != elem2:

        if not only_link_content(current_element): # if there is only content that is a link, skip it
            if current_element.text.strip() != "":
                content_list.append(H2T.handle(str(current_element)))

        current_element = current_element.find_next()

    return "\n".join(content_list)

class TocNode(dict):
    def __init__(self, title:str='', href:str='', anchor:str='', level:int=0, children:list=None):
        self.title = title
        self.href = href
        self.anchor = anchor
        self.level = level
        self.children: list[TocNode] = children
        self.element: BeautifulSoup = None
        self.content: str = None
        self.content_token_count: int = None
    
    def set_children(self, children: list):
        self.children = children
    
    def get_children(self) -> list:
        return self.children
    
    def get_num_children(self) -> int:
        if not self.children:
            return 0
        return len(self.children)
    
    def is_leaf(self) -> bool:
        return not bool(self.children)
    
    def is_root(self) -> bool:
        return self.level <= 0
    
    def get_item_with_href(self, book:epub.EpubBook) -> BeautifulSoup:
        book.get_item_with_href(self.href)
    
    def soup_element(self, soup: BeautifulSoup) -> Tag:
        if self.anchor:
            self.element = soup.find(id=self.anchor)
            return self.element
        else:
            self.element = soup.find(has_text) # find the first element with text
            return self.element
    
    def set_content(self, content: str):
        self.content = content
        self.content_token_count = TOK_COUNT(content)
    
    def __repr__(self):
        return f"title={self.title}, href={self.href}#{self.anchor if self.anchor else ''}, level={self.level}, #children={self.get_num_children()}"
    
    def __str__(self):
        return f"title={self.title}, href={self.href}#{self.anchor if self.anchor else ''}, level={self.level}, #children={self.get_num_children()}"
    
    def __iter__(self):
        return iter(self.children)
    
    def __next__(self):
        return next(self.children)
    
    def __getitem__(self, key):
        return self.children[key]
    
def split_href(href:str) -> tuple[str, str]:
    """
    Split the href into the link and the anchor (if it exists)
    """
    
    if '#' in href:
        return href.split('#')
    else:
        return href, None
    
def get_soup(book: epub.EpubBook, href:str) -> BeautifulSoup:
    content = book.get_item_with_href(href).get_body_content()
    try:
        return BeautifulSoup(content, 'lxml')
    except ImportError: # lxml not installed
        try:
            return BeautifulSoup(content, 'html5lib')
        except ImportError: # html5lib not installed
            return BeautifulSoup(content, 'html.parser')
    except:
        return BeautifulSoup(content, 'html5lib')
    
class TocTree:
    
    def __init__(self, book: epub.EpubBook):
        self.book = book
        
        self.root: TocNode = TocNode('root')
        self._parse_toc_tree(self.root, book.toc)
        self.inorder: list[TocNode] = self._get_inorder(self.root, [])[1:] # without the root node
        
        self._item_cache: dict[str, BeautifulSoup] = {}
        
        for node in self.inorder:
            if node.href and node.href not in self._item_cache:
                self._item_cache[node.href] = get_soup(book, node.href)
                
        for node1, node2 in zip_longest(self.inorder, self.inorder[1:]):
            elem1 = self.get_soup_element(node1)
            elem2 = self.get_soup_element(node2)
            
            node1.set_content(get_content_between_elements(elem1, elem2))
                
    
    def _parse_toc_tree(self, toc_node:TocNode, toc_list:list) -> list:
        next_toc_list = []

        for entry in toc_list:
            if isinstance(entry, tuple):
                section, nested_toc = entry
                section : epub.Section
                nested_toc : list
                href, anchor = split_href(section.href)

                tmp_node = TocNode(title=section.title, href=href, anchor=anchor, level=toc_node.level+1)
                next_toc_list.append(tmp_node)
                self._parse_toc_tree(tmp_node, nested_toc)
                
            elif isinstance(entry, epub.Link):
                href, anchor = split_href(entry.href)
                next_toc_list.append(TocNode(title=entry.title, href=href, anchor=anchor, level=toc_node.level+1))
                
        toc_node.set_children(next_toc_list)
        return toc_node
    
    def _get_inorder(self, toc_node:TocNode, inorder:list) -> list:
        inorder.append(toc_node)
        
        if not toc_node.is_leaf():
            for child in toc_node.get_children():
                self._get_inorder(child, inorder)
                
        return inorder
    
    def get_tree(self) -> TocNode:
        return self.root
    
    def get_inorder(self) -> list:
        return self.inorder
    
    def get_item_with_href(self, href:str) -> BeautifulSoup:
        if self._item_cache[href]:
            return self._item_cache[href]
        else:
            return get_soup(self.book, href)
    
    def get_soup_element(self, node:TocNode | None) -> Tag:
        if node is None:
            return None
        return node.soup_element(self.get_item_with_href(node.href))
    
    def __iter__(self):
        return iter(self.inorder)
    
    def __next__(self):
        return next(self.inorder)
    
    def __getitem__(self, key) -> TocNode:
        return self.inorder[key]
        
    def __repr__(self) -> str:
        return f"TOC Tree: {self.root}"
    
    def __str__(self) -> str:
        return f"TOC Tree: {self.root}"