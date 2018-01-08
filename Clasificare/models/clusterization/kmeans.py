from sklearn.cluster import KMeans


def build_model(dataset):
    return KMeans(
        n_jobs=-1,
        precompute_distances=True,
        n_clusters=len(dataset.y),
        n_init=3,
        verbose=1,
        algorithm='full'
    )


def fit_model(model,
              x_train, y_train, y_train_labeled,
              x_test, y_test, y_test_labeled):
    return model.fit(x_train)
