"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""

import datetime
import typing
from string import ascii_lowercase, whitespace


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        pass


class Article:
    """The `Article` class you need to write for the qualifier."""

    _instances = []

    def __init__(
        self, title: str, author: str, publication_date: datetime.datetime, content: str
    ):
        self.__class__._instances.append(self)

        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.__content = content

        self.last_edited = None

    def __repr__(self):
        title = self.title
        author = self.author
        publication_date = datetime.datetime.isoformat(self.publication_date)

        return f"<Article {title=} {author=} {publication_date=}>"

    def __len__(self):
        return len(self.content)

    def short_introduction(self, n_characters: int):
        intro = self.content[:n_characters]

        words = self.content.split()
        intro_words = intro.split()

        last_intro_word = intro_words[-1]
        if last_intro_word not in words:
            intro = intro.replace(last_intro_word, "")

        intro = intro.strip()

        return intro

    def most_common_words(self, n_words: int):
        normalized_content = "".join(
            char
            if (char in ascii_lowercase) or (char in whitespace)
            else " "  # Non-alphabet characters count as a whitespace
            for char in self.content.lower()
        )

        words = normalized_content.split()
        word_ct_map: dict[str, int] = {}
        for word in words:
            ct = word_ct_map.get(word, 0)
            word_ct_map[word] = ct + 1

        sorted_ct = sorted(word_ct_map.items(), key=lambda item: item[1], reverse=True)
        sliced_ct = sorted_ct[:n_words]

        return dict(sliced_ct)

    @property
    def id(self):
        return self.__class__._instances.index(self)

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content: str):
        self.__content = new_content
        self.last_edited = datetime.datetime.now()

    def __lt__(self, other):
        return self.publication_date < other.publication_date

    def __le__(self, other):
        return self.publication_date <= other.publication_date

    def __eq__(self, other):
        return self.publication_date == other.publication_date

    def __ne__(self, other):
        return self.publication_date != other.publication_date

    def __gt__(self, other):
        return self.publication_date > other.publication_date

    def __ge__(self, other):
        return self.publication_date >= other.publication_date
