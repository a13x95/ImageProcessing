import os
from collections import Counter
from functools import reduce
from operator import mul
from sklearn.cluster import KMeans

from Clasificare.models.neural_network.vgg_16 import build_model, fit_model
from Clasificare.statistics.validation import kfold_validation
from Clasificare.utils.dataset_utils import read_data
from shutil import copyfile
import numpy as np


def cluster(dataset_path="./dataset/train",
            new_dataset_path="./dataset/clusters",
            num_clusters=5):
    dataset = read_data(
        dataset_path,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True,
        shuffle=True
    )

    x = dataset.x
    x = x.reshape((x.shape[0], reduce(mul, x.shape[1:])))
    y_labels = np.argmax(dataset.y, axis=1)
    model = KMeans(n_jobs=-1,
                   init='k-means++',
                   precompute_distances=True,
                   n_clusters=num_clusters,
                   n_init=3,
                   verbose=1,
                   algorithm='full')
    kmeans = model.fit(x)
    cluster_data = {}
    for cluster in range(num_clusters):
        cluster_data[cluster] = {}

    for file, cluster, label in zip(dataset.files, kmeans.labels_, y_labels):
        dirpath = os.path.join(new_dataset_path, str(cluster))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        num_files = len(os.listdir(dirpath))
        filename = "%s_%s.%s" % (dataset.inv_named_labels[label], str(num_files), "jpg")
        filepath = os.path.join(dirpath, filename)
        copyfile(file, filepath)

        cluster_data[cluster][label] = cluster_data[cluster].get(label, 0) + 1
        # Remember total in -1
        cluster_data[cluster][-1] = cluster_data[cluster].get(-1, 0) + 1

    label_counter = Counter(y_labels)
    for cluster in range(num_clusters):
        total = cluster_data[cluster][-1]

        print("Cluster #%s:" % cluster)
        for label in cluster_data[cluster]:
            if label == -1:
                continue

            num_instances = cluster_data[cluster][label]
            percent = round(num_instances / total * 100, 3)
            label_percent = round(num_instances / label_counter[label] * 100, 3)

            print(" * %s: %s%% | %s%%" %
                  (dataset.inv_named_labels[label],
                   percent,
                   label_percent
                   ))


def kfold(dataset_path="./dataset/vgg16"):
    dataset = read_data(
        dataset_path,
        lambda path: os.path.basename(os.path.dirname(path)),
        recursive=True,
        shuffle=True
    )

    kfold_validation(dataset,
                     build_model,
                     fit_model,
                     confusion_matrix_file='./statistics/vgg16_4fold_confusion_matrix.png')


if __name__ == '__main__':
    kfold()
