#!/usr/bin/env python

# Author : Ledoux Louis

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from data_1_8v import *


# Figure width base on the column width of the Latex document.
fig_width = 252
fig_text_width = 516
fig_text_width_thesis = 473.46

def set_size(width, fraction=1, subplots=(1, 1)):
    """

    :param width:
    :param fraction:
    :return:
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches.
    inches_per_pt = 1 / 72.27

    # Golden ration to set aesthetic figure height.
    # https://disq.us/p/2940ij3
    golden_ratio = (5 ** (1 / 2) - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    #if width == fig_text_width:
    #    fig_height_in /= 0.5

    #fig_height_in = fig_width_in*1.4
    #fig_height_in *= 1.2

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


bit_distance = [0,4,8,12,16,20,24,28]

# Define a discrete color palette
# https://matplotlib.org/stable/users/explain/colors/colormaps.html#qualitative
palette = plt.get_cmap('Set1')

computed_data = raw_2_dict(raw_data_1_8v)

adders = {
    "behavioural": {
        "data": {
            "delay_1.8v": [2.1705719, 2.755608483, 3.118534548, 3.570078162, 4.38043839, 4.295562862, 4.864215004, 5.584309915],
            "delay_1.6v": [2.442989127, 2.943768685, 3.575677076, 4.202644508, 5.489969055, 5.432029896, 6.131974168, 7.157025764]
        },
        "plot_style": {
            "marker": "o",
            "linestyle": "-",
            "label": "Behavioural",
            "color": palette(0),
        }
    },
    "sklansky": {
        "data": {
            "delay_1.8v": [1.851831782, 2.788259438, 3.195847207, 3.613921169, 4.040814325, 4.403930573, 4.650926841, 4.703482199],
            "delay_1.6v": [2.345819642, 3.561338293, 4.218343354, 4.842155666, 5.487880279, 5.907767099, 6.227035652, 6.346833889]
        },
        "plot_style": {
            "marker": "s",
            "linestyle": "--",
            "label": "Sklansky",
            "color": palette(1),
        }
    },
    "brent_kung": {
        "data": {
            "delay_1.8v": [1.495781696, 2.481109048, 3.419925329, 3.344422343, 3.500948896, 3.687447666, 4.020314825, 5.026352601],
            "delay_1.6v": [1.704489071, 3.028765991, 4.30874534, 4.298181594, 4.517705912, 4.823445272, 5.231962826, 6.585568486]
        },
        "plot_style": {
            "marker": "^",
            "linestyle": "-.",
            "label": "Brent-Kung",
            "color": palette(2),
        }
    },
    "ripple": {
        "data": {
            "delay_1.8v": [0.06231745902,1.117840846,3.53092025,5.487520426,7.017823034,8.627782244,9.747552148,10.6970611],
            "delay_1.6v": [0.3004265974, 1.700647181, 4.722209498, 7.368598817, 9.41320625, 11.54355026, 13.24879231, 14.57669217]
        },
        "plot_style": {
            "marker": "x",
            "linestyle": ":",
            "label": "Ripple",
            "color": palette(3),
        }
    },
    "kogge": {
        "data": {
            "delay_1.8v": [2.116786639, 3.037296205, 3.012803961, 3.067843271, 3.144087579, 3.810230415, 3.964014607, 3.905994351],
            "delay_1.6v": [2.402238157, 3.783138193, 3.628780702, 3.806547487, 3.954037386, 4.734552003, 4.939722087, 4.842312202]
        },
        "plot_style": {
            "marker": "x",
            "linestyle": ":",
            "label": "Kogge-Stone",
            "color": palette(4),
        }
    }
}

for adder in adders.keys():
    if adder in computed_data:
        adders[adder]["data"]["computed_adder_delay_1.8v"] = [data["adder_delay_mean"] for data in computed_data[adder]]
        adders[adder]["data"]["computed_adder_delay_error_1.8v"] = [data["adder_delay_error"] for data in computed_data[adder]]

def plot():

    num_subplots = 2

    fig_dim = set_size(fig_width,1,(1,1))
    #fig = plt.figure(constrained_layout=True, figsize=fig_dim, dpi=500)
    fig = plt.figure(constrained_layout=False, figsize=fig_dim, dpi=500)
    gs = GridSpec(num_subplots, 1,figure=fig)

    # Create an initial axis object
    ax_main = fig.add_subplot(gs[0, 0])

    # Create the rest of the axes and share Y with the main axis
    #axes = [ax_main] + [fig.add_subplot(gs[i, 0], sharex=ax_main) for i in range(1, num_subplots)]
    axes = [ax_main] + [fig.add_subplot(gs[i, 0]) for i in range(1, num_subplots)]
    ax = axes[0]

     Iterate over adders and plot each one
    for adder_name, adder_info in adders.items():
        ax.plot(bit_distance, adder_info["data"]["delay_1.8v"],
                     marker=adder_info["plot_style"]["marker"],
                     linestyle=adder_info["plot_style"]["linestyle"],
                     color=adder_info["plot_style"]["color"],
                     label=adder_info["plot_style"]["label"])


    # because series share same x position we do dodge/drift technic
#    offset_value = 0.1  # This value can be adjusted based on the scale of your x-axis
#    num_series = len(adders.keys())  # Number of data series
#    midpoint = num_series / 2
#
#    scaling_factor = 1000

#    for i, (adder_name, adder_info) in enumerate(adders.items()):
#        # Calculate the offset for each series
#        series_offset = (i - midpoint) * offset_value
#        adjusted_bit_distance = [x + series_offset for x in bit_distance]
#
#        # Scale errors if needed
#        scaled_errors = [error * scaling_factor for error in adder_info["data"]["computed_adder_delay_error_1.8v"]]
#
#        ax.errorbar(adjusted_bit_distance,
#                    adder_info["data"]["computed_adder_delay_1.8v"],
#                    yerr=scaled_errors,
#                    fmt=adder_info["plot_style"]["marker"],
#                    linestyle=adder_info["plot_style"]["linestyle"],
#                    color=adder_info["plot_style"]["color"],
#                    label=adder_info["plot_style"]["label"])

#    for i, (adder_name, adder_info) in enumerate(adders.items()):
#        # Calculate the offset for each series to avoid overlap
#        series_offset = (i - midpoint) * offset_value
#        adjusted_bit_distance = [x + series_offset for x in bit_distance]
#
#        # Calculate percentage errors
#        mean_values = adder_info["data"]["computed_adder_delay_1.8v"]
#        absolute_errors = adder_info["data"]["computed_adder_delay_error_1.8v"]
#        percentage_errors = [(error / mean) * 100 if mean != 0 else 0 for mean, error in zip(mean_values, absolute_errors)]
#
#        # Plot with error bars
#        ax.errorbar(adjusted_bit_distance,
#                    mean_values,
#                    yerr=percentage_errors,
#                    fmt=adder_info["plot_style"]["marker"],
#                    linestyle=adder_info["plot_style"]["linestyle"],
#                    color=adder_info["plot_style"]["color"],
#                    label=adder_info["plot_style"]["label"])
#
    # scales
    #ax.set_yscale("log")

    # customize ticks
    ax.set_xticks(bit_distance)
    ax.set_xticklabels([f"{bd}" for bd in bit_distance])

    # legend and labels
    ax.set_xlabel("Index of Output Bit")
    ax.set_ylabel(r"Delay $(ns)$")
    #ax.set_title("Comparison of Adder Topologies at 1.8V")

    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(adders), title="Adder Topology", fancybox=False, framealpha=1.0, edgecolor="white")
    #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=1,title="Adder Topology", fancybox=False, framealpha=1.0, edgecolor="white")


    #plt.tight_layout()
    plt.savefig(f"instrumented_adder_delays_1_8v.pdf", bbox_inches='tight')
    #plt.savefig(f"instrumented.pdf")
    plt.close(fig)


def main():
    # Configurations for publication quality
    tex_fonts = {
        'text.usetex': True,
        'font.family': 'serif',
        'font.serif': ['Times New Roman'] + plt.rcParams['font.serif'],
        'axes.labelsize': 8,
        'font.size': 8,
        'legend.fontsize': 5,
        'legend.handlelength': 2.25,
        'legend.columnspacing': 0.5,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'lines.markeredgewidth': 0.3,
        'lines.markersize': 3,
        'lines.linewidth': 0.5,
        'hatch.linewidth': 0.2,
         #grid
        'grid.color': '#A5A5A5',     # Light gray grid
        'grid.linestyle': '--',      # Dashed grid lines
        'grid.linewidth': 0.3,       # Grid line width
        'axes.grid': True,           # Display grid by default
        'axes.grid.which': 'both'    # Apply to both major and minor grid lines
    }

    plt.style.use('grayscale')
    plt.rcParams.update(tex_fonts)


    plot()

if __name__ == '__main__':
    main()
