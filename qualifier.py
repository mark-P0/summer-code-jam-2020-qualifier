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
        self.field_type = field_type

        self._instances = {}

    def __get__(self, instance, owner):
        value = self._instances.get(instance, None)

        return value

    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"Expected type is {self.field_type}; got {type(value)}")

        self._instances[instance] = value


class ArticleID:
    _instances = []

    def __init__(self, *args, **kwargs):
        self.__class__._instances.append(self)

        super().__init__(*args, **kwargs)

    @property
    def id(self):
        return self.__class__._instances.index(self)


class ArticleContent:
    def __init__(self, content: str, **kwargs):
        self._content = content
        self.last_edited = None

        super().__init__(**kwargs)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content: str):
        self._content = new_content
        self.last_edited = datetime.datetime.now()


class ArticlePublicationDate:
    def __init__(self, publication_date: datetime.datetime, **kwargs):
        self.publication_date = publication_date

        super().__init__(**kwargs)

    def __lt__(self, other):
        return self.publication_date < other.publication_date

    def __le__(self, other):
        return self.publication_date <= other.publication_date

    def __gt__(self, other):
        return self.publication_date > other.publication_date

    def __ge__(self, other):
        return self.publication_date >= other.publication_date

    @property
    def publication_date_iso(self):
        return datetime.datetime.isoformat(self.publication_date)


class Article(ArticleID, ArticleContent, ArticlePublicationDate):
    """The `Article` class you need to write for the qualifier."""

    attribute = ArticleField(field_type=int)

    def __init__(
        self, title: str, author: str, publication_date: datetime.datetime, content: str
    ):
        self.title = title
        self.author = author

        super().__init__(
            publication_date=publication_date,
            content=content,
        )

    def __repr__(self):
        title = self.title
        author = self.author
        publication_date = self.publication_date_iso

        return f"<Article {title=} {author=} {publication_date=}>"

    def __len__(self):
        return len(self.content)

    def __hash__(self):
        title = self.title
        author = self.author
        publication_date = self.publication_date_iso

        return hash((title, author, publication_date))

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
