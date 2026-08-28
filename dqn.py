import torch
from torch import nn
import torch.nn.functional as F


class DQN(nn.Module):
    def __init__(self, input_n, output_n):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_n, 64)
        self.fc2 = nn.Linear(64, output_n)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)