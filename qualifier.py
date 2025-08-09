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
import typing as T
from string import ascii_lowercase, whitespace


class EndMRO:
    """
    Empty "mixin" that removes arguments from the inheritance chain

    Must be used at the end of inheritance chain that uses shared `kwargs` technique

    Needed because at the end of the inheritance chain, it is assumed that all arguments are consumed

    Must not have anything following it in the chain; i.e. the next call should be `object.__init__()`
    """

    def __init__(self, *_, **__):
        super().__init__()  # Remove all unused args


class ArticleKwargs(T.TypedDict):
    title: str
    content: str
    author: str
    publication_date: datetime.datetime


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: T.Type[T.Any]):
        self.field_type = field_type

        self._instances = {}
        self._name_in_classes = {}

    def __get__(self, instance, owner):
        value = self._instances.get(instance, None)

        return value

    def __set__(self, instance, value):
        if isinstance(value, self.field_type):
            self._instances[instance] = value

            return

        name = self._name_in_classes.get(instance.__class__, None)
        if name is None:
            raise TypeError(
                f"expected an instance of type '{self.field_type.__name__}', got '{type(value).__name__}' instead"
            )

        raise TypeError(
            f"expected an instance of type '{self.field_type.__name__}' for attribute '{name}', got '{type(value).__name__}' instead"
        )

    def __set_name__(self, owner, name):
        self._name_in_classes[owner] = name


class ArticleID:
    _instances = []

    def __init__(self, **kwargs: T.Unpack[ArticleKwargs]):
        self.__class__._instances.append(self)

        super().__init__(**T.cast(T.Any, kwargs))

    @property
    def id(self):
        return self.__class__._instances.index(self)


class ArticleContent:
    def __init__(self, **kwargs: T.Unpack[ArticleKwargs]):
        self._content = kwargs["content"]
        self.last_edited = None

        super().__init__(**T.cast(T.Any, kwargs))

    def __len__(self):
        return len(self._content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content: str):
        self._content = new_content
        self.last_edited = datetime.datetime.now()


class ArticlePublicationDate:
    def __init__(self, **kwargs: T.Unpack[ArticleKwargs]):
        self.publication_date = kwargs["publication_date"]

        super().__init__(**T.cast(T.Any, kwargs))

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


class ArticleRepresentation(ArticlePublicationDate):
    def __init__(self, **kwargs: T.Unpack[ArticleKwargs]):
        self.title = kwargs["title"]
        self.author = kwargs["author"]

        super().__init__(**T.cast(T.Any, kwargs))

    def __repr__(self):
        title = self.title
        author = self.author
        publication_date = self.publication_date_iso

        return f"<Article {title=} {author=} {publication_date=}>"

    def __hash__(self):
        """
        https://docs.python.org/3/reference/datamodel.html#object.__hash__
        - Implies that `__hash__` should only be defined if `__eq__` is defined

        This is used for associating classes with attribute names in descriptors (e.g. `ArticleField`)
        """

        title = self.title
        author = self.author
        publication_date = self.publication_date_iso

        return hash((title, author, publication_date))


class ArticleIntroduction(ArticleContent):
    def short_introduction(self, n_characters: int):
        intro = self.content[:n_characters]

        words = self.content.split()
        intro_words = intro.split()

        last_intro_word = intro_words[-1]
        if last_intro_word not in words:
            intro = intro.replace(last_intro_word, "")

        intro = intro.strip()

        return intro


class ArticleCommonWords(ArticleContent):
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


class Article(
    ArticleCommonWords,
    ArticleRepresentation,
    ArticleIntroduction,
    ArticleID,
    EndMRO,
):
    """
    The `Article` class you need to write for the qualifier.

    Uses a "middleware-like" inheritance approach. Inheritance list is evaluated in order as written
    """

    attribute = ArticleField(field_type=int)
