from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import  argparse

parser = argparse.ArgumentParser(description="ZepazoCrop: Cuts a portion of the video")
parser.add_argument( "-vo", "--videoOriginal", type=str, help="Video file path to crop")
parser.add_argument( "-vc", "--videoCropped", type=str, help="Video file path to analize")
parser.add_argument( "-ss", "--secondStart", type=int, help="Second when starts new cropped video")
parser.add_argument( "-se", "--secondEnd", type=int, help="Second when ends new cropped video")




