import logging
from typing import List, Union

import discord
import tiktoken

log = logging.getLogger("red.vrt.assistant.utils")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def get_attachments(message: discord.Message) -> List[discord.Attachment]:
    """Get all attachments from context"""
    attachments = []
    if message.attachments:
        direct_attachments = [a for a in message.attachments]
        attachments.extend(direct_attachments)
    if hasattr(message, "reference"):
        try:
            referenced_attachments = [
                a for a in message.reference.resolved.attachments
            ]
            attachments.extend(referenced_attachments)
        except AttributeError:
            pass
    return attachments


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    if not string:
        return 0
    num_tokens = len(encoding.encode(string))
    return num_tokens


async def fetch_channel_history(
    channel: Union[discord.TextChannel, discord.Thread, discord.ForumChannel],
    limit: int = 50,
    oldest: bool = True,
) -> List[discord.Message]:
    history = []
    async for msg in channel.history(oldest_first=oldest, limit=limit):
        history.append(msg)
    return history


def extract_message_content(message: discord.Message):
    content = ""
    if message.content:
        content += f"{content}\n"
    if message.embeds:
        content += f"{extract_embed_content(message.embeds)}\n"
    return content.strip()


def extract_embed_content(embeds: List[discord.Embed]) -> str:
    content = ""
    for embed in embeds:
        if title := embed.title:
            content += f"{title}\n"
        if desc := embed.description:
            content += f"{desc}\n"
        if fields := embed.fields:
            for field in fields:
                content += f"{field.name}\n{field.value}\n"
        if foot := embed.footer:
            content += f"{foot.text}\n"
    return content.strip()


def token_pagify(text: str, max_tokens: int = 2000):
    """Pagify a long string by tokens rather than characters"""
    token_chunks = []
    tokens = encoding.encode(text)
    current_chunk = []

    for token in tokens:
        current_chunk.append(token)
        if len(current_chunk) == max_tokens:
            token_chunks.append(current_chunk)
            current_chunk = []

    if current_chunk:
        token_chunks.append(current_chunk)

    text_chunks = []
    for chunk in token_chunks:
        text_chunk = encoding.decode(chunk)
        text_chunks.append(text_chunk)

    return text_chunks