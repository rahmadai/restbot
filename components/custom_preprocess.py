from __future__ import annotations
import csv
from typing import Any, Dict, List, Optional, Text

from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class AnotherWhitespaceTokenizer(Tokenizer):
    """Creates features for entity extraction."""

    @staticmethod
    def not_supported_languages() -> Optional[List[Text]]:
        """The languages that are not supported."""
        return ["zh", "ja", "th"]

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            # This *must* be added due to the parent class.
            "intent_tokenization_flag": False,
            # This *must* be added due to the parent class.
            "intent_split_symbol": "_",
            # This is a, somewhat silly, config that we pass
            "only_alphanum": False,
            # New configuration for lowercase
            "lowercase": True,
            # Path to CSV file containing word changes
            "word_changes_path": "db/word_changes.csv",
        }

    def __init__(self, config: Dict[Text, Any]) -> None:
        """Initialize the tokenizer."""
        super().__init__(config)
        self.only_alphanum = config["only_alphanum"]
        self.lowercase = config.get("lowercase", True)
        self.word_changes = self._load_word_changes(config.get("word_changes_path"))

    def _load_word_changes(self, file_path: Text) -> Dict[Text, Text]:
        word_changes = {}
        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    word_changes[row["word"]] = row["changes_word"]
        except FileNotFoundError:
            print(f"CSV file '{file_path}' not found.")
        return word_changes

    def parse_string(self, s):
        if self.only_alphanum:
            return "".join([c for c in s if ((c == " ") or str.isalnum(c))])
    
        s = s.lower()

        for word, changed_word in self.word_changes.items():
            s = s.replace(word, changed_word)

        return s

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> AnotherWhitespaceTokenizer:
        return cls(config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = self.parse_string(message.get(attribute))
        # print(text)
        # print("hehe")
        words = [w for w in text.split(" ") if w]

        # if we removed everything like smiles `:)`, use the whole text as 1 token
        if not words:
            words = [text]

        # the ._convert_words_to_tokens() method is from the parent class.
        tokens = self._convert_words_to_tokens(words, text)
        print(text)

        return self._apply_token_pattern(tokens)