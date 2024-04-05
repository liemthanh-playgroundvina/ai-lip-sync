# pip install basicsr
import sys
sys.path.append("scripts/wav2lip/GFPGAN")
from gfpgan import GFPGANer

restorer = GFPGANer(
    model_path="gfpgan/weights/GFPGANv1.4.pth",
)
