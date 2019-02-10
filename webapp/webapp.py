import random

from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
import bokeh.application
import bokeh.server.server
import confluent_kafka
import numpy as np
import sklearn.mixture

c = confluent_kafka.Consumer({"bootstrap.servers": "localhost:9092",
                              "group.id": "mygroup"})
c.subscribe(["datastream"])

# data_arr = np.array([]).reshape(-1, 2)
# model = sklearn.mixture.BayesianGaussianMixture(n_components=10,
#                                                 max_iter=5000,
#                                                 warm_start=True,
#                                                 covariance_type="spherical")

def read_from_kafka():
    data = [m.value() for m in c.consume(100, 1)
            if (m is not None) and not m.error()]
    data_arr = np.array([np.frombuffer(item) for item in data])

    if len(data_arr) == 0:
        return [], [], []


    return list(data_arr[:, 0]), list(data_arr[:, 1]), [random.choice(["red", "blue", "green"]) for _ in range(len(data_arr))]


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




# def kafka_to_buffer():
#     data = [m.value() for m in c.consume(100, 1)
#             if (m is not None) and not m.error()]
#     return np.array([np.frombuffer(item) for item in data])

# def read_from_buffer():
#     global data_arr
#     data_arr.extend(kafka_to_buffer())
#     if len(data_arr) >= 10:
#         data_copy =  data_arr.copy()
#         data_arr = []
#         return data_copy
#     else:
#         return []

# @app.route("/")
# def send_model_params():
#     X = read_from_buffer()
#     if not len(X) == 0:
#         model.fit(X)
#     else:
#         return flask.jsonify({"Data": [],
#                               "Clusters": []})

#     estimated_clusters = [float(val) for val in model.predict(X)]

#     data_list = []
#     for arr in X:
#         data_list.append(list(arr))
#     return flask.jsonify({"Data": data_list,
#                           "Clusters": estimated_clusters})
