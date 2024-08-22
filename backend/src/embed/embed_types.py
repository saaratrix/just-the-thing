import re
from enum import Enum

from .redgifs_embedder import redgifs_url_regex, RedgifsEmbedder

_redgifsEmbedder = RedgifsEmbedder()

class UrlType(Enum):
    Unknown = 0,
    Redgifs = 4

def get_embedder(url: str):
    embed_type = get_embed_type(url)
    if embed_type == UrlType.Unknown:
        return None
    if embed_type == UrlType.Redgifs:
        return _redgifsEmbedder


def get_embed_type(url: str) -> int:
    if redgifs_url_regex.match(url):
        return UrlType.Redgifs

    return UrlType.Unknown