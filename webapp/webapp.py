import random

from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
import bokeh.application
import bokeh.server.server
import confluent_kafka
import numpy as np
import sklearn.mixture

n_components = 3

c = confluent_kafka.Consumer({"bootstrap.servers": "localhost:9092",
                              "group.id": "mygroup"})
c.subscribe(["datastream"])

all_data = np.array([]).reshape(-1, 2)
new_data = np.array([]).reshape(-1, 2)
cluster_preds = []
model = sklearn.mixture.BayesianGaussianMixture(n_components=n_components,
                                                max_iter=5000,
                                                warm_start=True,
                                                covariance_type="spherical")

def read_from_kafka():
    global all_data
    global cluster_preds
    global new_data
    data = [m.value() for m in c.consume(100, 1)
            if (m is not None) and not m.error()]
    data_arr = np.array([np.frombuffer(item) for item in data]).reshape(-1, 2)
    new_data = np.vstack((new_data, data_arr))

    if len(new_data) > n_components:
        model.fit(new_data)
        all_data = np.vstack((all_data, new_data))
        new_data = np.array([]).reshape(-1, 2)
        cluster_preds = list(model.predict(all_data).flatten())

    if len(all_data) == 0:
        return [], [], []

    return list(all_data[:, 0]), list(all_data[:, 1]), [["red", "blue", "green"][cluster] for cluster in cluster_preds]


def make_document(doc):
    source = ColumnDataSource({"x": [], "y": [], "color": []})

    def update():
        new_x, new_y, colors = read_from_kafka()
        new = {"x": new_x,
               "y": new_y,
               "color": colors}
        source.stream(new)

    doc.add_periodic_callback(update, 1_000)

    fig = figure(title="Streaming Cluster Plot", sizing_mode="scale_height",
                 x_range=[-6, 6], y_range=[-6, 6])
    fig.circle(source=source, x="x", y="y", color="color", size=10)

    doc.title = "Streaming Cluster Plot"
    doc.add_root(fig)

apps = {"/": bokeh.application.Application(FunctionHandler(make_document))}

if __name__ == "__main__":
    server = bokeh.server.server.Server(apps, port=5006)
    server.run_until_shutdown()
