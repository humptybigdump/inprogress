import math
import torch
import torchvision
import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sn

from torchvision import transforms
from sklearn.metrics import confusion_matrix, accuracy_score


def load_cifar10(root_dir, batch_size, num_workers, augment_data=False):

    if augment_data:
        transform = transforms.Compose([
            # Flip the images randomly on the horizontal
            transforms.RandomHorizontalFlip(p=0.5),
            # Randomly rotate some images by 20 degrees
            transforms.RandomRotation(20),
            # Randomly adjust color jitter of the images
            transforms.ColorJitter(brightness = 0.1,contrast = 0.1,saturation = 0.1),
            # Randomly adjust sharpness
            transforms.RandomAdjustSharpness(sharpness_factor = 2,p = 0.2),
            # Turn the image into a torch.Tensor
            transforms.ToTensor() ,
            #randomly erase a pixel
            transforms.Normalize(mean, std),
            transforms.RandomErasing(p=0.75,scale=(0.02, 0.1),value=1.0, inplace=False)
        ])
    else:
        transform = transforms.Compose([
             transforms.ToTensor()
        ])

    trainset = torchvision.datasets.CIFAR10(root=root_dir, train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    
    validset = torchvision.datasets.CIFAR10(root=root_dir, train=False, download=True, transform=transform)
    validloader = torch.utils.data.DataLoader(validset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return trainloader, validloader
    


def visualize_cifar10(train_loader, class_names, N=25): 
    # Determine grid dimensions
    rows = int(math.sqrt(N))
    cols = (N + rows - 1) // rows  # Ensures enough subplots for all images

    # Get N random batches of images and their corresponding labels
    dataiter = iter(train_loader)
    images, labels = next(dataiter)

    # Create a grid of subplots
    fig, axes = plt.subplots(rows, cols, figsize=(rows*2, cols*2))
    axes = axes.flatten()  # Flatten the 2D array of axes to simplify looping

    for i in range(N):
        img = images[i].numpy()  # convert from tensor to numpy array
        img = (img - img.min()) / (img.max() - img.min())
        img = np.transpose(img, (1, 2, 0))  # rearrange dimensions from CxHxW to HxWxC

        # Display image
        axes[i].imshow(img)
        axes[i].set_title(class_names[labels[i]])
        axes[i].axis('off')  # hide axes ticks

    # Hide any unused axes if N is not a perfect square
    for j in range(N, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    
def plot_confusion_matrix(model, loader, class_names, device):
        
    y_pred = []
    y_true = []
    
    model.eval()

    with torch.inference_mode():
        for X, y in loader:
            X , y = X.to(device) , y.to(device)
            pred_logits = model(X)
            pred = pred_logits.argmax(dim=1).cpu().numpy()
            y_pred.extend(pred)
            true = y.cpu().numpy()
            y_true.extend(true)
    
    cf_matrix = confusion_matrix(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
        
    df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix) *10, index=class_names, columns=class_names)
    plt.figure(figsize = (12,7))
    plt.title("{} - {:.2f}".format(model.__class__.__name__, 100 * accuracy))
    sn.heatmap(df_cm, annot=True)
