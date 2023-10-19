# Prediction interface for Cog 
from cog import BasePredictor, Input, Path
import os
import sys
import subprocess

sys.path.extend(['/VideoCrafter'])

MODEL_CACHE = "model-cache"

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""

    def predict(
        self,
        prompt: str = Input(description="Input Prompt"),
        width: int = Input(
            description="Width of the output video", default=1024
        ),
        height: int = Input(
            description="Height of the output video", default=576
        ),
        steps: int = Input(
            description="Number of steps to take in the video", default=50
        ),
        fps: int = Input(
            description="Frames per second of the output video", default=28
        ),
        seed: int = Input(
            description="Random seed. Leave blank to randomize the seed", default=None
        ),
    ) -> Path:
        """Run a single prediction on the model"""
        # Seed
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")

        # make prompt file
        with open("/tmp/input.txt", "w") as file:
            file.write(prompt)

        command = [
            "python",   "/VideoCrafter/scripts/evaluation/inference.py",
            "--seed",   str(seed),
            "--mode",   "base",
            "--ckpt_path",  "/src/model-cache/model.ckpt",
            "--config",     "/VideoCrafter/configs/inference_t2v_1024_v1.0.yaml",
            "--savedir",    "/VideoCrafter/results",
            "--n_samples",  "1",
            "--bs",         "1",
            "--height",     str(height),
            "--width",      str(width),
            "--unconditional_guidance_scale",   "12.0",
            "--ddim_steps", str(steps),
            "--ddim_eta",   "1.0",
            "--prompt_file","/tmp/input.txt",
            "--fps",        str(fps)
        ]
        subprocess.run(command)
        
        return_path="/VideoCrafter/results/0001.mp4"
        return Path(return_path)
