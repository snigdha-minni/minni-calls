from pyrogram import Client

from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped

app = Client(
    'py-tgcalls',
    api_id=12345,
    api_hash='0123456789abcdef0123456789abcdef',
)

call_py = PyTgCalls(app)
chat_id = -1001234567890
call_py.start()
audio_file = 'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4'
call_py.join_group_call(
    chat_id,
    AudioPiped(
        audio_file,
    ),
    stream_type=StreamType().pulse_stream,
)
idle()
