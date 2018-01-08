import matplotlib.pyplot as plt
import numpy as np


def build_confusion_matrix(named_labels,
                           conf_mat,
                           filename='confusion_matrix.png'):
    fig_size = plt.rcParams["figure.figsize"]
    plt.rcParams["figure.figsize"] = [14, 6]

    fig = plt.figure(1)
    fig.canvas.set_window_title('Confusion matrix')

    plt.rcParams["figure.figsize"] = fig_size

    conf_mat_norm = conf_mat / conf_mat.sum(axis=1)[:, None]

    conf_mat2 = np.around(conf_mat_norm, decimals=1)
    plt.imshow(conf_mat2, interpolation='nearest', aspect='equal')
    for x in range(len(named_labels)):
        for y in range(len(named_labels)):
            plt.annotate(str(conf_mat2[x][y]), xy=(y, x), ha='center', va='center', fontsize=5)

    plt.xticks(range(len(named_labels)),
               rotation=90,
               fontsize=6)

    plt.yticks(range(len(named_labels)),
               map(lambda e: "{0} #{1}".format(e[1], e[0]),
                   enumerate(named_labels)),
               fontsize=6)

    plt.title('Confusion matrix')
    plt.colorbar()
    plt.savefig(filename)

    return fig
