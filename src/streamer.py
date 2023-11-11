from transformers import TextStreamer

class CustomStreamer(TextStreamer):

    def __init__(self, queue,tokenizer, skip_prompt,**decode_kwargs) -> None:
        super().__init__(tokenizer, skip_prompt, **decode_kwargs)
        self._queue = queue
        self.stop_signal=None
        self.timeout = 1
        
    def on_finalized_text(self, text: str, stream_end: bool = False):
        self._queue.put(text)
        if stream_end:
            self._queue.put(self.stop_signal)