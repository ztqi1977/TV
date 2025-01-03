import subprocess
import sys
import re
import urllib.parse

def ends_with_h264(url):
    """Check if the URL ends with '-h264'."""
    return url.lower().endswith('-h264')

def get_video_codec(stream_url, timeout=10):
    """Use ffprobe to get the video codec of a stream with error handling."""
    try:
        # Ensure URL is valid and starts with http(s) or [ipv6]
        if not (stream_url.startswith('http://') or stream_url.startswith('https://') or stream_url.startswith('[')):
            print(f"Invalid URL format: {stream_url}")
            return None
        
        # Use ffprobe to check video codec
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', stream_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            timeout=timeout  # Set a timeout for the command
        )
        # Split the output by lines and take the first line only
        codec_lines = result.stdout.decode().strip().splitlines()
        codec = codec_lines[0] if codec_lines else None
        return codec if codec else None
    except subprocess.CalledProcessError as e:
        print(f"Error checking video codec for {stream_url}: {e}")
        return None
    except subprocess.TimeoutExpired:
        print(f"Timeout expired while checking video codec for {stream_url}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred for {stream_url}: {e}")
        return None

def filter_m3u(input_file, output_file):
    """
    Filter M3U file to only include URLs that end with '-h264' and confirm they are H.264 encoded.
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("#EXTM3U\n")  # Write first info line
        current_info_line = None
        
        for line in infile:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # Save the info line to possibly write later
                current_info_line = line
            elif current_info_line and (line.startswith('http://') or line.startswith('https://') or line.startswith('[')):
                url = line.strip()  # 获取URL行
                if ends_with_h264(url):
                    video_codec = get_video_codec(url)
                    if video_codec and video_codec.lower() == 'h264':
                        print(f"Confirmed H.264 encoded URL: {url}")
                        outfile.write(current_info_line + '\n')  # 写入信息行
                        outfile.write(url + '\n')  # 写入URL行
                    else:
                        print(f"URL does not use H.264 encoding: {url}")
                current_info_line = None
            else:
                current_info_line = None

# 使用函数
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python filtermp2.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    filter_m3u(in_file, out_file)