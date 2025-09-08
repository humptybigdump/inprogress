# import the necessary packages
from os import listdir
from os.path import isfile, join, splitext
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import torch.nn.functional as F
import torch.nn as nn
import random
import matplotlib.pyplot as plt


def multi_class_dice_coeff(true, logits, eps=1e-7):
    """Computes the Sørensen-Dice coefficient for multi-class.
    Args:
        true: a tensor of shape [B, 1, H, W].
        logits: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or logits of the model.
        eps: added to the denominator for numerical stability.
    Returns:
        dice_coeff: the Sørensen-Dice coefficient.
    """
    num_classes = logits.shape[1]
    true_1_hot = torch.eye(num_classes, device=true.device)[true.squeeze(1)]
    true_1_hot = true_1_hot.permute(0, 3, 1, 2).float()
    probas = F.softmax(logits, dim=1)
    true_1_hot = true_1_hot.type(logits.type())
    dims = (0,) + tuple(range(2, true.ndimension()))
    intersection = torch.sum(probas * true_1_hot, dims)
    cardinality = torch.sum(probas + true_1_hot, dims)
    dice_coeff = (2.0 * intersection / (cardinality + eps)).mean()
    return dice_coeff



def dice_loss(true, logits, eps=1e-7):
    """Computes the Sørensen-Dice loss, which is 1 minus the Dice coefficient.
    Args:
        true: a tensor of shape [B, 1, H, W].
        logits: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or logits of the model.
        eps: added to the denominator for numerical stability.
    Returns:
        dice_loss: the Sørensen-Dice loss.
    """
    return 1 - multi_class_dice_coeff(true, logits, eps)



def evaluate(model: nn.Module, dataloader: DataLoader, device: torch.device, criterion):
    
    model.eval()

    total_loss = 0.0
    total_dice = 0.0
    with torch.no_grad():
        for batch in dataloader:
            # extract the image and mask batch, and move the batch to the device
            images, true_masks = batch['image'], batch['mask']
            true_masks = true_masks.squeeze(1) # remove the channel dimension if it exists
            # move images and masks to correct device and type
            images = images.to(
                device=device,
                dtype=torch.float32,
                memory_format=torch.channels_last,
            )
            true_masks = true_masks.to(device=device, dtype=torch.long)
            # predict the mask using the model
            masks_pred = model(images)
            # ensure the predicted masks are in the correct shape
            
            # compute the cross-entropy loss and the Dice loss for the predicted masks vs. the true masks
            loss = criterion(masks_pred, true_masks)
            loss += dice_loss(true_masks, masks_pred)
            
            total_loss += loss.item()
            # compute Dice score for training set for this batch and add it to the epoch Dice score
            dice_score_batch = multi_class_dice_coeff(
                true_masks, masks_pred
            )
            total_dice += (
                dice_score_batch.item()
            )  # Sum up the Dice score for each batch
            # compute average loss and Dice score for this epoch
        
    avg_loss = total_loss / len(dataloader)
    avg_dice = total_dice / len(dataloader)
    return avg_dice, avg_loss



def visualize_predictions(model: nn.Module, dataloader: DataLoader, device: torch.device):
    model.eval()
    with torch.no_grad():
        sample_batch = random.choice(list(dataloader))
        images, true_masks = sample_batch['image'], sample_batch['mask']
        idx = random.randint(0, images.shape[0] - 1)
        sample_image = images[idx].unsqueeze(0).to(device=device, dtype=torch.float32, memory_format=torch.channels_last)
        sample_true_mask = true_masks[idx].squeeze().to(device=device)
        prediction = model(sample_image)
        prediction = prediction.argmax(dim=1).squeeze().cpu().numpy()
        sample_true_mask = sample_true_mask.cpu().numpy().astype(np.uint8)
        sample_image = (sample_image - sample_image.min()) / (sample_image.max() - sample_image.min() + 1e-6)
        sample_image = sample_image.squeeze(0).cpu().permute(1, 2, 0).numpy()
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        def overlay_multiclass_mask(image, mask, class_colors, alpha=0.5):
            """
            Overlay multi-class mask on image.
            - image: H x W x 3 float image (0-1)
            - mask: H x W int mask with values 0..N classes
            - class_colors: dict[class_value] = (r,g,b)
            - alpha: transparency for all classes
            Returns an image with overlays.
            """
            overlay = image.copy()
            for class_val, color in class_colors.items():
                class_mask = (mask == class_val)
                color_arr = np.array(color).reshape(1, 1, 3)
                class_mask_3d = np.repeat(class_mask[:, :, np.newaxis], 3, axis=2)
                overlay = np.where(
                    class_mask_3d,
                    (1 - alpha) * overlay + alpha * color_arr,
                    overlay)
            return overlay

        class_colors = {
            0: (1, 0, 0),  # background red
            1: (0, 1, 0),  # pet green
            2: (0, 0, 1),  # border blue
        }
        true_overlay = overlay_multiclass_mask(sample_image, sample_true_mask, class_colors, alpha=0.5)
        pred_overlay = overlay_multiclass_mask(sample_image, prediction, class_colors, alpha=0.5)
        axs[0].imshow(sample_image)
        axs[0].set_title("Input Image")
        axs[0].axis("off")
        axs[1].imshow(true_overlay)
        axs[1].set_title("True Mask Overlay")
        axs[1].axis("off")
        axs[2].imshow(pred_overlay)
        axs[2].set_title("Predicted Mask Overlay")
        axs[2].axis("off")
        plt.tight_layout()
        plt.show()



def plot_training(epoch_losses=[], val_scores=[], train_scores=[], val_losses=[], moving_average_window=5):
    """
    Plots training and validation loss and score curves over epochs.
    
    Parameters:
    - epoch_losses: list of training losses per epoch
    - val_scores: list of validation scores per epoch
    - train_scores: list of training scores per epoch
    - val_losses: list of validation losses per epoch
    - moving_average_window: window size for moving average smoothing
    """
    def moving_average(data, window):
        if len(data) < window:
            return data
        return np.convolve(data, np.ones(window)/window, mode='valid')
    
     # Clear the output before plotting again
    plt.clf()
    plt.cla()
    plt.close('all')  # force close previous figures
    
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    epochs = np.arange(1, len(epoch_losses) + 1)

    # ==== LOSS PLOT ====
    if epoch_losses:
        axs[0].plot(epochs, epoch_losses, label="Train Loss (raw)", color='blue', alpha=0.3)
        ma_train_loss = moving_average(epoch_losses, moving_average_window)
        axs[0].plot(epochs[-len(ma_train_loss):], ma_train_loss, label="Train Loss (MA)", color='blue')

    if val_losses:
        axs[0].plot(epochs, val_losses, label="Val Loss (raw)", color='green', alpha=0.3)
        ma_val_loss = moving_average(val_losses, moving_average_window)
        axs[0].plot(epochs[-len(ma_val_loss):], ma_val_loss, label="Val Loss (MA)", color='green')

    axs[0].set_title("Loss over Epochs")
    axs[0].set_xlabel("Epoch")
    axs[0].set_ylabel("Loss")
    axs[0].legend()
    axs[0].grid(True)

    # ==== SCORE PLOT ====
    if train_scores:
        axs[1].plot(epochs, train_scores, label="Train Score (raw)", color='blue', alpha=0.3)
        ma_train_score = moving_average(train_scores, moving_average_window)
        axs[1].plot(epochs[-len(ma_train_score):], ma_train_score, label="Train Score (MA)", color='blue')

    if val_scores:
        axs[1].plot(epochs, val_scores, label="Val Score (raw)", color='green', alpha=0.3)
        ma_val_score = moving_average(val_scores, moving_average_window)
        axs[1].plot(epochs[-len(ma_val_score):], ma_val_score, label="Val Score (MA)", color='green')

    axs[1].set_title("Dice Score over Epochs")
    axs[1].set_xlabel("Epoch")
    axs[1].set_ylabel("Score")
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()