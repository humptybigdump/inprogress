import matplotlib.pyplot as plt
import numpy as np
import torch as th
from torch import nn


# th.set_printoptions(linewidth=240, sci_mode=False)
def print2d(tensor: th.tensor, width: int, precision: int):
    assert width > precision - 2
    assert tensor.ndim == 2
    # precision symbols after dot, 1 symbol for dot and possibly one for sign
    assert tensor.abs().max() < 10 ** (width - precision - 2)

    def value_format(v):
        if v == 0.0:
            return f"\033[1m{v:{width}.{precision}f}\033[0m"
        else:
            return f"{v:{width}.{precision}f}"

    for row in tensor:
        print(*(value_format(v) for v in row.tolist()))


x_min, x_max = -3, 2
data_noise = 0.3
num_data = 20
num_plot = 200
bsz = 20


def fun(x):
    return x**3 + 3 * x**2 - x - 4


th.manual_seed(seed=42)
gen = np.random.default_rng(seed=42)
x_data = np.concatenate(
    (
        gen.normal(loc=-2.0, scale=0.5, size=(num_data // 2,)),
        gen.normal(loc=1.0, scale=0.3, size=(num_data // 2,)),
    )
)
x_plot = np.linspace(num=num_plot, start=x_min, stop=x_max)
y_data = fun(x_data) + data_noise * gen.standard_normal(x_data.shape)

x = th.tensor(x_data, dtype=th.float32).unsqueeze(-1)
x_plot = th.tensor(x_plot, dtype=th.float32).unsqueeze(-1)
y = th.tensor(y_data, dtype=th.float32)

hidden = 32
dropout_p = 0.1


class EvalDropout(nn.Dropout):
    def __init__(self, p: float = 0.5, inplace: bool = False):
        super().__init__(p, inplace)
        self.do_eval_dropout = False

    def forward(self, input):
        if self.training:
            dropped_out = super().forward(input)
            # print(); print2d(dropped_out, 5, 2)
            return dropped_out
        elif self.do_eval_dropout:
            # also do consistent dropout during eval
            dim = input.shape[-1]
            mask = th.bernoulli((1 - self.p) * th.ones(size=(dim,), dtype=input.dtype))
            dropped_out = input * mask
            # print(); print2d(dropped_out, 5, 2)
            return dropped_out
        else:
            averaged = super().forward(input)
            # print(); print2d(averaged, 5, 2)
            return averaged


model_det = nn.Sequential(
    nn.Linear(1, hidden),
    nn.SiLU(),
    nn.Linear(hidden, hidden),
    nn.SiLU(),
    nn.Linear(hidden, hidden),
    nn.SiLU(),
    nn.Linear(hidden, 1),
)

model_dropout = nn.Sequential(
    nn.Linear(1, hidden),
    EvalDropout(p=dropout_p),
    nn.SiLU(),
    nn.Linear(hidden, hidden),
    EvalDropout(p=dropout_p),
    nn.SiLU(),
    nn.Linear(hidden, hidden),
    EvalDropout(p=dropout_p),
    nn.SiLU(),
    nn.Linear(hidden, 1),
)
optim_det = th.optim.Adam(params=model_det.parameters(), lr=3e-3, weight_decay=0e-1)
optim_dropout = th.optim.Adam(
    params=model_dropout.parameters(), lr=3e-3, weight_decay=0e-1
)


model_det.train()
model_dropout.train()


for iters in range(3_000):
    bsz_idx = gen.integers(0, num_data, bsz)

    y_pred_det = model_det(x[bsz_idx]).squeeze(-1)
    y_pred_dropout = model_dropout(x[bsz_idx]).squeeze(-1)

    mse_det = (y_pred_det - y[bsz_idx]).square().mean()
    optim_det.zero_grad()
    mse_det.backward()
    optim_det.step()

    mse_dropout = (y_pred_dropout - y[bsz_idx]).square().mean()
    optim_dropout.zero_grad()
    mse_dropout.backward()
    optim_dropout.step()

    if iters % 100 == 0:
        print(f"det: {mse_det.item():.3f}, dropout: {mse_dropout:.3f}")

model_det.eval()
model_dropout.eval()

# single model
with th.no_grad():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_data, y_data, label="Data")
    ax.plot(x_plot.numpy(), fun(x_plot.numpy()), label="Ground Truth")
    y_plot_det = model_det(x_plot)
    ax.plot(x_plot.numpy(), y_plot_det.numpy(), label="Single Model")

    # dropout model with mean weight
    y_plot = model_dropout(x_plot)
    ax.plot(x_plot.numpy(), y_plot.numpy(), label="Dropout Mean")
    ax.legend(loc="upper left")
    fig.show()

pass

# dropout model samples
for m in model_dropout.modules():
    if isinstance(m, EvalDropout):
        m.do_eval_dropout = True

with th.no_grad():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_data, y_data, label="Data")
    for dropouts in range(5):
        y_plot = model_dropout(x_plot)
        ax.plot(x_plot.numpy(), y_plot.numpy(), label=f"Dropout Mask Sample {dropouts}")
    fig.show()

pass


# Sample posterior predictive distribution by sampling many dropout masks and evaluating function.
model_dropout.train()
for m in model_dropout.modules():
    if isinstance(m, EvalDropout):
        m.do_eval_dropout = False

with th.no_grad():
    num_samples = 200
    num_hist_bins = 50
    num_quantiles = 11  # 0%, 10%, ..., 90%, 100%
    quantile_levels = th.linspace(0, 1, num_quantiles)

    y_plot = model_dropout(x_plot.expand((num_samples,) + x_plot.shape))
    # y_plot has shape [num_samples, x_plotting_points, 1]

    # shape of [num_quantiles, x_plotting_points, 1]
    quantiles = th.quantile(y_plot, quantile_levels, dim=0, keepdim=False)

    # fig = plt.figure()
    # ax1, ax2 = fig.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    gs = fig.add_gridspec(2, 2, height_ratios=[5, 1], width_ratios=[1, 1])

    ax1 = fig.add_subplot(gs[0, 0])  # histogram
    ax2 = fig.add_subplot(gs[0, 1])  # posterior curves
    ax_slider = fig.add_subplot(gs[1, :])  # slider spans both columns

    # plot histogram of model evaluations at one x
    histogram_sample_index = 0
    histogram = ax1.hist(
        y_plot[:, histogram_sample_index], bins=num_hist_bins, color="C0", range=(-4, 4)
    )

    # plot posterior of function in shaded regions
    from matplotlib import cm

    colormap = cm.Blues
    half = num_quantiles // 2
    quantile_shaded_regions = [
        ax2.fill_between(
            x_plot[..., -1],
            quantiles[i, ..., -1],
            quantiles[-(i + 1), ..., -1],
            color=colormap(i / half),
        )
        for i in range(0, half)
    ]

    ax1.set_title(f"Histogram of model at {x_plot[histogram_sample_index].item():.3f}")
    ax1.set_xlabel("$y$")
    ax1.set_ylabel("$p(y | x)$")

    ax2.set_title("Distribution of function values")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$f(x)$")

    ax1.set_xlim(-4, 4)
    ax2.set_xlim(-3, 3)

    # add vertical line in right subplot ax2 at selected index
    vline = ax2.axvline(x_plot[histogram_sample_index].item(), color="r", lw=2)

    from matplotlib.widgets import Slider

    slider = Slider(
        ax=ax_slider,
        label="sample index",
        valmin=0,
        valmax=x_plot.shape[0] - 1,
        valinit=histogram_sample_index,
        valfmt="%0.0f",
        valstep=1,
    )

    def update(val):
        histogram_sample_index = int(val)

        # clear and redraw histogram
        ax1.cla()
        ax1.hist(
            y_plot[:, histogram_sample_index, 0],
            bins=num_hist_bins,
            color="C0",
            range=(-4, 4),
        )
        ax1.set_title(
            f"Histogram of f(x) at x={x_plot[histogram_sample_index].item():.2f}"
        )

        # move the vertical line in the right subplot (just updating vline with set_xdata doesnt work...)
        ax2.cla()
        quantile_shaded_regions = [
            ax2.fill_between(
                x_plot[..., -1],
                quantiles[i, ..., -1],
                quantiles[-(i + 1), ..., -1],
                color=colormap(i / half),
            )
            for i in range(0, half)
        ]
        ax2.axvline(x_plot[histogram_sample_index].item(), color="r", lw=2)

        fig.canvas.draw_idle()

    slider.on_changed(update)

    fig.show()

pass
