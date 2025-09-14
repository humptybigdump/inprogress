import os
import torch
import torch.nn as nn


class VGG(nn.Module):
    def __init__(self, input_shape: int, output_shape: int) -> None:
        super().__init__()
        self.conv_block_1 = nn.Sequential(
            nn.Conv2d(in_channels=input_shape, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2)
        )
        self.conv_block_2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=32*8*8,out_features=2048),
            nn.ReLU(),
            nn.Dropout(p=0.5), #add dropout layer to decrease overfitting
            nn.Linear(in_features=2048,out_features=1024),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(in_features=1024,out_features=output_shape)
        )
        
        self.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))


    def forward(self, x: torch.Tensor):
        x = self.conv_block_1(x)
        x = self.conv_block_2(x)
        x = self.classifier(x)
        return x

    def save_checkpoint(self, epoch, accuracy, ckptpath="checkpoint"):
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.state_dict(),
            'accuracy': accuracy,
        }
        ckptpath = os.path.join(ckptpath, "checkpoint_{}_{:.4f}.pth".format(epoch, accuracy))
        # Save the dictionary to file
        torch.save(checkpoint, ckptpath)

    def load_checkpoint(self, ckptpath, map_location=None):
        # Load the saved file
        checkpoint = torch.load(ckptpath, map_location=map_location)
        
        # Restore model and optimizer state
        self.load_state_dict(checkpoint['model_state_dict'])