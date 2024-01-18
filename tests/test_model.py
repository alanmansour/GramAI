import pytest
import torch

from src.models.model import MyAwesomeModel


@pytest.mark.parametrize("x, y", [((1, 1, 28, 28), (1, 10)), ((10, 1, 28, 28), (10, 10))])
def test_model(x, y):
    model = MyAwesomeModel()
    model.eval()
    x_ = torch.randn(x)
    y_ = model(x_)
    assert y_.shape == y, f"The output shape does not equal to {y} given the input {x}"


def test_error_on_wrong_shape():
    model = MyAwesomeModel()
    with pytest.raises(ValueError, match="Expected input to a 4D tensor"):
        model(torch.randn(1, 2, 3))
