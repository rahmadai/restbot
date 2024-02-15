from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
import pandas as pd

df = pd.read_csv('db/word_changes.csv')

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)
class Preprocess(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        # TODO: Implement this
        ...
        
    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        ...

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # TODO: Implement this if your component augments the training data with
        #       tokens or message features which are used by other components
        #       during training.
        ...

        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        # lowercase message in messages
        for message in messages:
            # change all the symbol with space
            message.data['text'] = message.data['text'].replace('.', ' ')
            message.data['text'] = message.data['text'].replace(',', ' ')
            message.data['text'] = message.data['text'].replace('!', ' ')
            message.data['text'] = message.data['text'].replace('?', ' ')
            message.data['text'] = message.data['text'].replace('/', ' ')
            message.data['text'] = message.data['text'].replace('-', ' ')
            message.data['text'] = message.data['text'].replace('_', ' ')
            message.data['text'] = message.data['text'].replace('(', ' ')
            message.data['text'] = message.data['text'].replace(')', ' ')
            message.data['text'] = message.data['text'].replace('[', ' ')
            message.data['text'] = message.data['text'].replace(']', ' ')
            message.data['text'] = message.data['text'].replace('{', ' ')
            message.data['text'] = message.data['text'].replace('}', ' ')
            message.data['text'] = message.data['text'].replace(':', ' ')
            message.data['text'] = message.data['text'].replace(';', ' ')
            message.data['text'] = message.data['text'].lower()
            # replace word in message.data['text'] with word in csv file
            # run word by word inside text and replace with word_changes.csv
            # for word in message.data['text'].split():
            #     try:
            #         message.data['text'] = message.data['text'].replace(word, df.loc[df['word'] == word, 'changes_word'].iloc[0])
            #     except:
            #         pass
            # print(message.data['text'])

        return messages
