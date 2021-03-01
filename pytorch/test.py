from zoo.orca import init_orca_context, stop_orca_context
from zoo.orca import OrcaContext

# recommended to set it to True when running Analytics Zoo in Jupyter notebook.
OrcaContext.log_output = True # (this will display terminal's stdout and stderr in the Jupyter notebook).
init_orca_context(cores=1, memory="2g")   # run in local mode


import torch.nn as nn
import torch.nn.functional as F


max_features = 10000  # number of words to consider as features
maxlen = 500  # cut texts after this number of words (among top max_features most common words)
batch_size = 128


class SimpleRNN(nn.Module):
    def __init__(self, input_dim):
        super(SimpleRNN, self).__init__()

        self.embedding = nn.Embedding(input_dim, 32)
        self.rnn = nn.RNN(32, 32)
        self.fc = nn.Linear(32, 1)
        self.out_act = nn.Sigmoid()

    def forward(self, text):
        #embedded = self.embedding(text.transpose(0, 1))
        embedded = self.embedding(text)
        output, hidden = self.rnn(embedded)
        # output = self.fc(output[-1, :, :])
        output = self.fc(output[:, -1, :])
        return self.out_act(output)



import torch
from torchtext import data
from torchtext.datasets import IMDB

SEED = 1234

torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
TEXT = data.Field(tokenize='spacy',
                  tokenizer_language='en_core_web_sm',
                  fix_length=maxlen)
LABEL = data.LabelField(dtype=torch.float)

print("Loading data")
train_data, test_data = IMDB.splits(TEXT, LABEL)
train_data, valid_data = train_data.split(0.8)

#TEXT.build_vocab(train_data, max_size=max_features)
TEXT.build_vocab(train_data, 
                 max_size = max_features, 
                 vectors = "glove.6B.100d", 
                 unk_init = torch.Tensor.normal_)
LABEL.build_vocab(train_data)

'''
train_iterator, valid_iterator = data.BucketIterator.splits(
    (train_data, valid_data),
    batch_size=128)
'''

train_iterator, valid_iterator = data.BucketIterator.splits(
    (train_data, valid_data),
    batch_size=1)
train_list = list(train_iterator)     # A list of torchtext.data.batch.Batch
valid_list = list(valid_iterator) 

train_text = [e.text for e in train_list]
train_label = [e.label for e in train_list]
valid_text = [e.text for e in valid_list]
valid_label = [e.label for e in valid_list]


from torch.utils.data import Dataset

class IMDBDataset(Dataset):

    def __init__(self, text_list, label_list, transform=None):
        """
        Args:
            text_dataset (torchtext.data.dataset.Dataset): torchtext dataset
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """      
        self.text = text_list
        self.label = label_list
        self.transform = transform

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        text = self.text[index].squeeze(1)
        label = self.label[index]

        return text, label


# data_loader
train_loader = torch.utils.data.DataLoader(
    IMDBDataset(train_text, train_label),
    batch_size=128, shuffle=True)
valid_loader = torch.utils.data.DataLoader(
    IMDBDataset(valid_text, valid_label),
    batch_size=128, shuffle=False)


# train
from zoo.orca.learn.pytorch import Estimator
from zoo.orca.learn.trigger import EveryEpoch
from zoo.orca.learn.metrics import Accuracy


INPUT_DIM = len(TEXT.vocab)
EMBEDDING_DIM = 32
HIDDEN_DIM = 32

model = SimpleRNN(INPUT_DIM)
model.train()
print(model)

rmsprop = torch.optim.RMSprop(model.parameters(), lr=0.0001)
adam = torch.optim.Adam(model.parameters(), 0.001) 
sgd = torch.optim.SGD(model.parameters(), lr=1e-3)
criterion = torch.nn.BCELoss()
#criterion = nn.BCEWithLogitsLoss()
metrics=[Accuracy()]

est = Estimator.from_torch(model=model, optimizer=rmsprop, loss=criterion, metrics=metrics)
est.fit(data=train_loader, epochs=5, validation_data=valid_loader, batch_size=batch_size, checkpoint_trigger=EveryEpoch())