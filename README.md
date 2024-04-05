

https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/13985

Replace /venv/lib/python3.10/site-packages/basicsr/data/degradations.py from at line 8:
from torchvision.transforms.functional_tensor import rgb_to_grayscale
to:
from torchvision.transforms.functional import rgb_to_grayscale

mapping: /venv/lib/python3.10/site-packages/basicsr/data/degradations.py:./models/degradation.py