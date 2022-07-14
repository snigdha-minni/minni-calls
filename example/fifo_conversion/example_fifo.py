import asyncio
import atexit
import os
import signal
import subprocess
import time

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

app = Client(
    'py-tgcalls',
    api_id=123456789,
    api_hash='abcdef12345',
)

call_py = PyTgCalls(app)
proc = {}


@app.on_message(filters.regex('!test'))
async def test_handler(client: Client, message: Message):
    global proc
    file = 'input.webm'
    output_file = 'input_fifo.raw'
    os.mkfifo(output_file)
    proc[message.chat.id] = await asyncio.create_subprocess_shell(
        cmd=(
            'ffmpeg '
            '-y -i '
            f'{file} '
            '-f s16le '
            '-ac 1 '
            '-ar 48000 '
            '-acodec pcm_s16le '
            f'{output_file}'
        ),
        stdin=asyncio.subprocess.PIPE,
    )

    while not os.path.exists(output_file):
        time.sleep(0.125)
    await call_py.join_group_call(
        message.chat.id,
        InputStream(
            InputAudioStream(
                output_file,
            ),
        ),
        stream_type=StreamType().pulse_stream,
    )


def close_all_process():
    global proc
    for i in proc:
        try:
            proc[i].send_signal(signal.SIGINT)
            proc[i].wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc[i].kill()


# AVOID ZOMBIE FFMPEG PROCESS
atexit.register(close_all_process)
call_py.start()
idle()
