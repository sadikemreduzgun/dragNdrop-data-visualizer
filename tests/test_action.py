from visualizer import DataFrameVisualizer

def test_action():

    vis = DataFrameVisualizer(is_test=True)
    assert vis.run() == 0

