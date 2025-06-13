import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Creating two layers for our network
        # Linear 1 : input --> hidden. Linear 2 : hidden --> output
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    # Function to go forward through the neural network layers we have defined
    def forward(self, currentVal):
        # Input --> Hidden
        currentVal = F.relu(self.linear1(currentVal))
        # Hidden --> Output
        return F.relu(self.linear2(currentVal))

    # Function to save the current model
    def save(self, fileName):
        # Making another folder to store our models
        model_folder_path = "./model"
        # If the model folder doesn't exist, make the model folder
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        # Appending the model folder path to the given filename
        file_name = os.path.join(model_folder_path, file_name)
        # Saving the model at that file_name path
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, lr, gamma, model):
        # Initialising some of the parameters of the Trainer
        self.lr = lr
        self.gamma = gamma
        self.model = model
        # Optimising our model, using the parameters and the learning rate
        self.optimiser = optim.Adam(model.parameters(), lr=self.lr)
        # Creating the Loss Function / Criterion Function
        # Our Loss Function is the Mean Squared Error function
        self.criterion = nn.MSELoss()

    # Converting a (x,y) tuple into a idx
    def getIndexFromCoordinate(self, coordinate):
        x, y = coordinate[0] - 1, coordinate[1] - 1
        return x + y * 8

    # Training the model
    def train_step(self, state, final_move, reward, next_state, checkmate):
        # Converting some of the inputs to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)

        # Checking if we are working with 1 value or lists of values
        if len(state.shape) == 3:
            # Needs these attributes in the form (1,x) so this is what the code below is doing
            # If we have a list of attributes, they are already in this form so we don't need to worry then
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            reward = torch.unsqueeze(reward, 0)
            final_move = (final_move,)

        # Predict the Q values with the current state
        pred = self.model(state)
        # Creating a clone of the prediction
        target = pred.clone()
        # Going over all the values given
        for idx in range(len(state)):
            # Setting Q_new to be the reward at the current index
            Q_new = reward
            # Applying the formula to get the next set of parameters
            # Only multiple by 1 value, the max of the predicted Q value for the next state
            Q_new = Q_new + self.gamma * torch.max(self.model(next_state[idx]))

            # Getting the coordinate for the move at the current idx
            moveIdx = self.getIndexFromCoordinate(final_move[idx][1])

            # Setting the new target value to be Q_new at the maximum value of action
            target[0][0][0][moveIdx] = Q_new

        # Applying the Loss Function
        self.optimiser.zero_grad()  # Emptying the gradient (step needed to learn within PyTorch)
        loss = self.criterion(target, pred)
        loss.backward()  # Applying backpropagation

        self.optimiser.step()


def train_step(self, state, action, reward, next_state, done):
    # Converting some of the inputs to tensors
    state = torch.tensor(state, dtype=torch.float)
    next_state = torch.tensor(next_state, dtype=torch.float)
    action = torch.tensor(action, dtype=torch.float)
    reward = torch.tensor(reward, dtype=torch.float)

    # Checking if we are working with 1 value or lists of values
    if len(state.shape) == 1:
        # Needs these attributes in the form (1,x) so this is what the code below is doing
        # If we have a list of attributes, they are already in this form so we don't need to worry then
        state = torch.unsqueeze(state, 0)
        next_state = torch.unsqueeze(next_state, 0)
        action = torch.unsqueeze(action, 0)
        reward = torch.unsqueeze(reward, 0)
        done = (done,)

    # Predict the Q values with the current state
    pred = self.model(state)
    # Creating a clone of the prediction
    target = pred.clone()
    # Going over all the values in the tensor
    for idx in range(len(done)):
        # Setting Q_new to be the reward at the current index
        Q_new = reward[idx]
        # Only apply the next parameters formula if the game isn't over at this step
        if not done[idx]:
            # Applying the formula to get the next set of parameters
            # Only multiple by 1 value, the max of the predicted Q value for the next state
            Q_new = Q_new + self.gamma * torch.max(self.model(next_state[idx]))

        # Setting the new target value to be Q_new at the maximum value of action
        target[idx][torch.argmax(action).item()] = Q_new

    # Applying the Loss Function
    self.optimiser.zero_grad()  # Emptying the gradient (step needed to learn within PyTorch)
    loss = self.criterion(target, pred)
    loss.backward()  # Applying backpropagation

    self.optimiser.step()
