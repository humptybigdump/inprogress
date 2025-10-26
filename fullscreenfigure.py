import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QT5Agg')
from PyQt5.QtWidgets import QDesktopWidget

# =============================================================================
# Function, to open an interactive window, covering the entire screen
# =============================================================================
def fullscreenfigure(fignum):
    # open or create the figure with number fignum
    fig = plt.figure(fignum,figsize=(16, 9),dpi=72,clear=True,
                     layout='constrained')
    # clear figure
    fig.clf()
    # try to bring it to the front
    fig.canvas.manager.window.raise_()
    # enable interactive mode
    plt.ion()
    # Choose a font family (e.g., serif, sans-serif, etc.)
    plt.rcParams['font.family'] = 'sans-serif'
    # Set the specific font (e.g., Times New Roman)
    plt.rcParams['font.sans-serif'] = ['Arial']  
    # Set resolution
    plt.rcParams["figure.dpi"] = 400
    # Set font size
    plt.rcParams.update({'font.size':14})                 # fontsize 
    # make the window fill the entire screen
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    window = fig.canvas.manager.window.geometry()
    frame  = fig.canvas.manager.window.frameGeometry()
    dheight=frame.height()-window.height()
    fig.canvas.manager.window.setGeometry(1, dheight-1, screen_width-2, screen_height-dheight)
    return fig



