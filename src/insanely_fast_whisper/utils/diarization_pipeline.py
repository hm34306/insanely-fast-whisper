from typing import Any

import torch
from pyannote.audio import Pipeline
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

from .diarize import (
    diarize_audio,
    post_process_segments_and_transcripts,
    preprocess_inputs,
)


def diarize(args: list[Any], outputs: dict[str]):  # noqa
    diarization_pipeline = Pipeline.from_pretrained(
        checkpoint_path=args.diarization_model,
        use_auth_token=args.hf_token,
    )
    diarization_pipeline.to(
        torch.device("mps" if args.device_id == "mps" else f"cuda:{args.device_id}")
    )

    with Progress(
        TextColumn("🤗 [progress.description]{task.description}"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Segmenting...", total=None)

        inputs, diarizer_inputs = preprocess_inputs(inputs=args.file_name)

        segments = diarize_audio(
            diarizer_inputs,
            diarization_pipeline,
            args.num_speakers,
            args.min_speakers,
            args.max_speakers,
        )

        return post_process_segments_and_transcripts(
            segments, outputs["chunks"], group_by_speaker=False
        )
