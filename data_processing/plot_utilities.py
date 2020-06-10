import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import six
import warnings
warnings.simplefilter('ignore', np.RankWarning)  # Ignores numpy polyfit rank warning

# XKCD triple red, green, blue, orange and purple
xkcd_red = [sns.xkcd_rgb["red"], sns.xkcd_rgb["lightish red"], sns.xkcd_rgb["ruby"]]
xkcd_green = [sns.xkcd_rgb["green"], sns.xkcd_rgb["pale green"], sns.xkcd_rgb["apple green"]]
xkcd_blue = [sns.xkcd_rgb["blue"], sns.xkcd_rgb["pale blue"], sns.xkcd_rgb["deep sky blue"]]
xkcd_orange = [sns.xkcd_rgb["orange"], sns.xkcd_rgb["amber"], sns.xkcd_rgb["blood orange"]]
xkcd_purple = [sns.xkcd_rgb["purple"], sns.xkcd_rgb["bright lavender"], sns.xkcd_rgb["blue violet"]]
# XKCD RGB and rainbow triples
xkcd_rgb = xkcd_red + xkcd_green + xkcd_blue
xkcd_rainbow = xkcd_purple + xkcd_blue + xkcd_green + xkcd_orange + xkcd_red

# Seaborn triple red, green, blue, orange and purple
triple_red = ['#FB9A99', '#EF5A5B', '#E31A1C']
triple_green = ['#B2DF8A', '#73C05B', '#33A02C']
triple_blue = ['#A6CEE3', '#63A3CC', '#1F78B4']
triple_orange = ['#FDBF6F', '#FE9F38', '#FF7F00']
triple_purple = ['#CAB2D6', '#9A78B8', '#6A3D9A']
# Seaborn RGB and rainbow triples
triples_rgb = triple_red + triple_green + triple_blue
triples = triple_red + triple_green + triple_blue + triple_purple + triple_orange

# Red, green, blue
rgb = ['#EF5A5B', '#73C05B', '#63A3CC']
# Red, green, blue, orange, purple
five_colour = ['#EF5A5B', '#73C05B', '#63A3CC', '#FE9F38', '#9A78B8']

colour_palettes = {'xkcd_red': xkcd_red, 'xkcd_green': xkcd_green, 'xkcd_blue': xkcd_blue,
                   'xkcd_orange': xkcd_orange, 'xkcd_purple': xkcd_purple,
                   'xkcd_rgb': xkcd_rgb, 'xkcd_rainbow': xkcd_rainbow,
                   'triple_red': triple_red, 'triple_green': triple_green, 'triple_blue': triple_blue,
                   'triple_orange': triple_orange, 'triple_purple': triple_purple,
                   'triples_rgb': triples_rgb, 'triples': triples, 'five_colour': five_colour, 'rgb': rgb,
                   'default': sns.color_palette('tab10')}


def create_colour_map(boundaries=None, pallet='RdBu_r'):
    """Creates a custom colour map around the specified boundary values."""
    # Check we have boundaries, else use default
    if boundaries is None:
        boundaries = [0.0, 1.0]

    # Create a list of colours in hex for each boundary value
    hex_colors = sns.color_palette(pallet, n_colors=len(boundaries) + 2).as_hex()
    hex_colors = [hex_colors[i] for i in range(0, len(hex_colors), 2)]

    # Map boundaries to colours
    colors = list(zip(boundaries, hex_colors))
    # Create the custom map
    custom_color_map = LinearSegmentedColormap.from_list(name='custom', colors=colors)
    return custom_color_map


def plot_line_chart(data, x='index', y='value', hue='group', style=None, size=None,
                    title='', y_label='', x_label='', colour='Paired'):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour, len(data[hue].unique()))

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.lineplot(data=data, x=x, y=y, hue=hue, style=style, size=size,
                     err_style='band', ci=24, sort=False, palette=palette)
    sns.despine(ax=g, left=True)

    # Set axis labels
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_scatter_chart(data, x='index', y='value', hue='group', size='metric',
                       title='', y_label='', x_label='', colour='Paired'):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour, len(data[hue].unique()))

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.scatterplot(data=data, x=x, y=y, hue=hue, size=size, sizes=(40, 400), alpha=1, palette=palette)
    sns.despine(ax=g, left=True)

    # Set axis labels
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_swarm_chart(data, x='index', y='value', hue='group', size=5,
                     title='', y_label='', x_label='', colour='Paired'):

    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour, len(data[hue].unique()))

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.swarmplot(data=data, x=x, y=y, hue=hue, size=size, dodge=True, palette=palette)
    sns.despine(ax=g, left=True)

    # Set axis labels
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_strip_chart(data, x='index', y='value', hue='group', title='', y_label='', x_label='', colour='Paired'):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour, len(data[hue].unique()))

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.stripplot(data=data, x=x, y=y, hue=hue, dodge=True, palette=palette)
    sns.despine(ax=g, left=True)

    # Set axis labels
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_violin_chart(data, x='index', y='value', hue=None, title='', y_label='', x_label='',
                      colour='Paired', inner='box', legend=False, legend_loc='best', x_tick_rotation=0):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        if hue:
            palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
        else:
            palette = dict(zip(data[x].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour)

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.violinplot(data=data, x=x, y=y, hue=hue, scale='width', inner=inner, cut=0, palette=palette)
    sns.despine(ax=g, left=True)

    # Add legend
    if legend:
        g.legend(frameon=True, shadow=True, loc=legend_loc)

    # Set axis labels
    g.set_xticklabels(g.get_xticklabels(), rotation=x_tick_rotation)
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_bar_chart(data, x='index', y='value', hue='variable', title='', y_label='', x_label='',
                   colour='Paired', dodge=False, legend_loc='best', num_legend_col=3, x_tick_rotation=0, show_bar_val=True):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour)

    # Create the barchart
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.barplot(data=data, x=x, y=y, hue=hue, palette=palette, dodge=dodge)
    sns.despine(ax=g, left=True)

    # Add legend
    g.legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)

    # Annotate the bars
    if show_bar_val:
        for p in g.patches:
            g.annotate('{0:.2f}'.format(p.get_height()), (p.get_x() + p.get_width() / 2.0, p.get_height()),
                       ha='center', va='center', fontsize=11, color='black', rotation=0, xytext=(0, 10),
                       textcoords='offset points')

    # Set axis labels
    g.set_xticklabels(g.get_xticklabels(), rotation=x_tick_rotation)
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g.get_figure()


def plot_box_chart(data, x='index', y='value', hue=None, title='', y_label='', x_label='',
                   colour='Paired', legend=False, legend_loc='best', x_tick_rotation=0):
    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        if hue:
            palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
        else:
            palette = dict(zip(data[x].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour)

    # Create the violin plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.boxplot(data=data, x=x, y=y, hue=hue, dodge=True, linewidth=None, palette=palette)
    sns.despine(ax=g, left=True)

    # Add legend
    if legend:
        g.legend(frameon=True, shadow=True, loc=legend_loc)

    # Set axis labels
    g.set_xticklabels(g.get_xticklabels(), rotation=x_tick_rotation)
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g, g.get_figure()


def plot_dist_chart(data, metric='value', hue=None, row=None, col='', title='', y_label='', x_label='',
                    plt_hist=True, axis_titles=False, share_x=False, share_y=False, num_col=2,
                    colour='Paired', all_legend=False, num_legend_col=1, legend_loc='best'):

    # If using xkcd colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        if hue:
            palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
        else:
            palette = dict(zip(data[metric].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour)

    # Create FacetGrid catplot for each item in 'metric'
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')

    g = sns.FacetGrid(data, row=row, col=col, hue=hue, col_wrap=num_col, palette=palette,
                      sharex=share_x, sharey=share_y, height=6, aspect=2)
    g = (g.map(sns.distplot, metric, hist=plt_hist))
    g = g.despine(left=True)

    # Add legend
    if all_legend:
        for i, ax in enumerate(g.axes.flatten()):
            ax.legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
    elif num_col:
        g.axes[num_col - 1].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
    else:
        g.axes[0, g.axes.shape[0] - 1].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)

    # Set axis labels
    g.set_xlabels(x_label)
    g.set_ylabels(y_label)

    # Set individual plot titles and main title
    if axis_titles and num_col:  # Sets plot titles to be y axis labels, else titles on top
        for i, ax in enumerate(g.axes):
            ax.set_ylabel(g.col_names[i], fontsize=14, fontweight='bold')
        g.set_titles('')
    elif axis_titles:
        for i, ax in enumerate(g.axes[:, 0]):
            ax.set_ylabel(g.row_names[i], fontsize=14, fontweight='bold')
        g.set_titles('')
        for i, ax in enumerate(g.axes[0, :]):
            ax.set_title(g.col_names[i], fontsize=14, fontweight='bold')
    else:
        g.set_titles("{col_name}", fontsize=14, fontweight='bold')

    g.fig.suptitle(title, fontsize=18, fontweight='bold', y=0.99)

    plt.tight_layout()
    return g, g.fig


def plot_heatmap(data, title='', y_label='', x_label='', colour='RdBu_r', custom_boundaries=None, center_val=None,
                 show_cbar=True, annotate=True, num_format='.3f', linewidth=0.5, linecolour=None, x_tick_rotation=0):
    # Check if creating a custom colour map, else use seaborn
    if custom_boundaries:
        # Create custom colour palette for each item in group
        palette = create_colour_map(boundaries=custom_boundaries, pallet=colour)
    else:
        palette = sns.color_palette(colour)

    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.heatmap(data, annot=annotate, fmt=num_format, linewidths=linewidth, linecolor=linecolour,
                    cmap=palette, center=center_val, cbar=show_cbar)
    # Set axis labels
    g.set_xticklabels(g.get_xticklabels(), rotation=x_tick_rotation)
    g.set_xlabel(x_label)
    g.set_ylabel(y_label)

    # Set main title
    g.set_title(title, fontsize=14, fontweight='bold')

    plt.tight_layout()
    return g.get_figure()


def plot_lmplot_chart(data, x='index', y='value', hue='group', col=None, title='', y_label='', x_label='', xtick_labels=None,
                      share_x=False, share_y=False, num_col=None, colour='Paired', legend_loc='best', num_legend_col=3,
                      scatter=True, sizes=(10, 10), order=2, ci=16, x_estimator=np.mean, x_ci=None, **kwargs):
    # If using my colours set the pallet, else use seaborn
    if colour in colour_palettes.keys():
        # Create colour palette for each item in group
        palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour, len(data[hue].unique()))

    # Create the lmplot plot
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.lmplot(data=data, x=x, y=y, hue=hue, col=col, col_wrap=num_col, sharex=share_x, sharey=share_y,
                   scatter=scatter, scatter_kws={"sizes": sizes}, order=order, ci=ci, x_estimator=x_estimator, x_ci=x_ci,
                   truncate=True, palette=palette, height=6, aspect=2, legend=False)
    g.despine(left=True)

    # Add legend to the plot, either single one or to each plot
    if len(g.axes) > 1:
        if 'all_legend' in kwargs and kwargs['all_legend']:
            for i in range(len(g.axes)):
                g.axes[i].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
        else:
            # Add to top right plot
            g.axes[num_col - 1].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
    else:
        plt.legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)

    # If x tick labels are specified set number and string values (needed because regression needs numerical x values)
    if xtick_labels is not None:
        g.set(xticks=np.arange(0, len(xtick_labels)))
        g.set_xticklabels(xtick_labels)

    # Set axis labels
    g.set_xlabels(x_label)
    g.set_ylabels(y_label)

    # Set individual plot titles and main title
    g.set_titles("{col_name}", fontsize=14, fontweight='bold')
    g.fig.subplots_adjust(top=0.95)
    g.fig.suptitle(title, fontsize=18, fontweight='bold')

    plt.tight_layout()
    return g, g.fig


def plot_facetgrid(data, x='index', y='value', hue='group', row=None, col='metric', kind='bar',
                   title='', y_label='', x_label='',
                   axis_titles=False, share_x=False, share_y=False, num_col=2,
                   colour='Paired', legend_loc='best', num_legend_col=3, all_legend=False, show_bar_value=False,
                   bar_value_rotation=0, x_tick_rotation=0, y_tick_rotation=0, **kwargs):

    # Facet grid plot functions
    def _scatter(*args, **kwargs):
        ax = plt.gca()
        current_data = kwargs.pop("data")
        sns.scatterplot(data=current_data, x=args[0], y=args[1], hue=args[2], palette=palette, ax=ax, **kwargs)

    def _violin(*args, **kwargs):
        ax = plt.gca()
        current_data = kwargs.pop("data")
        sns.violinplot(data=current_data, x=args[0], y=args[1], hue=args[2], palette=palette, ax=ax, **kwargs)

    def _bar(*args, **kwargs):
        ax = plt.gca()
        current_data = kwargs.pop("data")
        sns.barplot(data=current_data, x=args[0], y=args[1], hue=args[2], palette=palette, ax=ax, **kwargs)

    def _heatmap(*args, **kwargs):
        ax = plt.gca()
        current_data = kwargs.pop("data")
        current_data = current_data.pivot(index=args[0], columns=args[1], values=args[2])
        sns.heatmap(data=current_data,  cmap=palette, ax=ax, **kwargs)

    # Get the desired plot function for facetgrid
    plot_types = {'scatter': _scatter,
                  'violin': _violin,
                  'bar': _bar,
                  'heatmap': _heatmap}

    plot_function = plot_types[kind]

    # Check if creating a custom colour map, elsif using xkcd colours set the pallet, else use seaborn
    if 'custom_boundaries' in kwargs.keys() and kwargs['custom_boundaries']:
        palette = create_colour_map(boundaries=kwargs['custom_boundaries'], pallet=colour)
        del kwargs['custom_boundaries']
    # If using xkcd colours set the pallet, else use seaborn
    elif colour in colour_palettes.keys():
        if hue:
            palette = dict(zip(data[hue].unique(), colour_palettes[colour]))
        else:
            palette = dict(zip(data[x].unique(), colour_palettes[colour]))
    else:
        palette = sns.color_palette(colour)

    # Create FacetGrid for each item in 'metric'
    sns.set(rc={'figure.figsize': (11.7, 8.27)}, style='whitegrid')
    g = sns.FacetGrid(data=data, row=row, col=col, col_wrap=num_col, sharex=share_x, sharey=share_y, height=6, aspect=2)
    g.map_dataframe(plot_function, x, y, hue, **kwargs)
    g.despine(left=True)

    # Add legend to the plot, either a single one or to each plot (if not creating heatmaps)
    if kind != 'heatmap':
        if len(g.axes) > 1:
            if all_legend:
                for i, ax in enumerate(g.axes.flatten()):
                    ax.legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
            else:
                # Add to top right plot
                if num_col:
                    g.axes[num_col - 1].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
                else:
                    g.axes[0, g.axes.shape[0] - 1].legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)
        else:
            plt.legend(frameon=True, shadow=True, loc=legend_loc, ncol=num_legend_col)

    # Annotate the bars if using bar chart
    if kind == 'bar' and show_bar_value:
        for i, ax in enumerate(g.axes.flatten()):
            for p in ax.patches:
                y_txt_offset = 20 if bar_value_rotation == 90 else 10
                ax.annotate('{0:.2f}'.format(p.get_height()), (p.get_x() + p.get_width() / 2.0, p.get_height()),
                            ha='center', va='center', fontsize=11, color='black', rotation=bar_value_rotation,
                            xytext=(0, y_txt_offset), textcoords='offset points')
    # Set axis labels
    for ax in g.axes.flatten():
        # If sharing axis labels just get the first, else get each axis labels (because matplotlib/seaborn is why...)
        if share_y:
            ytick_labels = g.axes.flatten()[0].get_yticklabels()
        else:
            ytick_labels = ax.get_yticklabels()
        if share_x:
            xtick_labels = g.axes.flatten()[0].get_xticklabels()
        else:
            xtick_labels = ax.get_xticklabels()

        horiz_alignment = 'right' if x_tick_rotation != 0 else 'center'
        ax.set_xticklabels(xtick_labels, rotation=x_tick_rotation, ha=horiz_alignment)
        ax.set_yticklabels(ytick_labels, rotation=y_tick_rotation)

    # Set axis labels
    g.set_xlabels(x_label)
    g.set_ylabels(y_label)

    # Set individual plot titles and main title
    if axis_titles and num_col:  # Sets plot titles to be y axis labels, else titles on top
        for i, ax in enumerate(g.axes):
            ax.set_ylabel(g.col_names[i], fontsize=14, fontweight='bold')
        g.set_titles('')
    elif axis_titles:
        for i, ax in enumerate(g.axes[:, 0]):
            ax.set_ylabel(g.row_names[i], fontsize=14, fontweight='bold')
        g.set_titles('')
        for i, ax in enumerate(g.axes[0, :]):
            ax.set_title(g.col_names[i], fontsize=14, fontweight='bold')
    else:
        g.set_titles("{col_name}", fontsize=14, fontweight='bold')

    g.fig.suptitle(title, fontsize=18, fontweight='bold', y=0.99)

    plt.tight_layout()
    return g, g.fig


def plot_table(data, title=''):
    """Generates a table from a Dataframe."""
    # Matplotlib refuses to show the row labels so just set them as a column
    data = data.copy()
    data.insert(0, column='Labels', value=data.index)

    # Params
    col_width = 2.1
    row_height = 0.5
    font_size = 14
    header_color = '#40466e'
    row_colors = ['#f1f1f2', 'w']
    edge_color = 'w'
    bbox = [0, 0, 1, 1]
    header_columns = 1

    # Set the size of the table
    size = (np.array(data.shape[::]) + np.array([0, 1])) * np.array([col_width, row_height])
    fig, ax = plt.subplots(figsize=size)
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=data.values, cellLoc='center', colLabels=data.columns, bbox=bbox)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)

    # Colour the cells
    for k, cell in six.iteritems(table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    plt.title(title, fontdict={'fontsize': font_size * 2})

    plt.tight_layout()
    return fig
