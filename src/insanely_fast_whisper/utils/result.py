from typing import TypedDict


class JsonTranscriptionResult(TypedDict):
    speakers: list
    chunks: list
    text: str


def build_result(transcript:str, outputs:dict[str]) -> JsonTranscriptionResult:
    return {
        "speakers": transcript,
        "chunks": outputs["chunks"],
        "text": outputs["text"],
    }
