# MCP FFmpeg LiveStream AWS Toolkit

A comprehensive toolkit for FFmpeg video processing, live streaming operations, and AWS media services integration.

## Overview

This project provides a set of tools to simplify common video processing tasks, live streaming operations, and AWS media service interactions through a unified interface. It integrates with FFmpeg for video manipulation and offers convenient access to documentation for FFmpeg, various live streaming protocols, and AWS media services.

## Features

- **Documentation Access**: Retrieve and search through official documentation for FFmpeg, live streaming protocols, and AWS media services
- **FFmpeg Command Execution**: Run FFmpeg commands directly from the toolkit
- **Command Generation**: Automatically generate FFmpeg commands for common video operations:
  - Trimming videos
  - Format conversion
  - Video compression
  - Audio extraction
  - Video scaling
  - Overlay addition
  - Video concatenation
- **Web Content Extraction**: Extract and search through web-based documentation

## Installation

### Prerequisites

- Python 3.7+
- FFmpeg installed and available in your system PATH

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mcp-ffmpeg-livestream-aws.git
   cd mcp-ffmpeg-livestream-aws
   ```

2. Install required dependencies:
   ```
   pip install httpx beautifulsoup4 mcp
   ```

## Usage

This toolkit is built using the FastMCP framework and provides several tools that can be used programmatically or via command-line.

### Documentation Tools

#### Get Documentation URLs

Retrieve URLs for official documentation:

```python
from mcp.client import Client

client = Client('mcp-ffmpeg-livestream-aws')
# Get FFmpeg documentation URLs
ffmpeg_docs = client.get_documentation_urls(service_category="ffmpeg")
# Get AWS media services documentation URLs
aws_docs = client.get_documentation_urls(service_category="aws")
# Get live streaming protocol documentation URLs
streaming_docs = client.get_documentation_urls(service_category="live_streaming")
```

#### Get Service Documentation

Extract content from specific service documentation:

```python
# Get FFmpeg filter documentation
filter_docs = client.get_service_documentation(service_category="ffmpeg", service_name="filters")
# Get HLS streaming documentation
hls_docs = client.get_service_documentation(service_category="live_streaming", service_name="hls")
```

#### Search Documentation

Search for specific terms across documentation:

```python
# Search for "keyframe" across all documentation
results = client.search_documentation(term="keyframe")
# Search for "bitrate" only in FFmpeg documentation
ffmpeg_results = client.search_documentation(term="bitrate", service_category="ffmpeg")
```

### FFmpeg Tools

#### Run FFmpeg Commands

Execute FFmpeg commands directly:

```python
# Run a simple FFmpeg command
result = client.run_ffmpeg_command("-i input.mp4 -c:v libx264 -crf 23 output.mp4")
print(result["status"])  # "success" or "error"
print(result["stdout"])  # Standard output
print(result["stderr"])  # Standard error/logs
```

#### Generate FFmpeg Commands

Generate commands for common video operations:

```python
# Generate command to trim a video
trim_cmd = client.generate_ffmpeg_command(
    operation="trim",
    input_file="input.mp4",
    start_time="00:01:00",
    duration="30",
    output_file="trimmed_output.mp4"
)
print(trim_cmd["full_command"])  # The complete FFmpeg command

# Generate command to extract audio
audio_cmd = client.generate_ffmpeg_command(
    operation="extract_audio",
    input_file="input.mp4",
    output_format="mp3"
)
print(audio_cmd["full_command"])

# Generate and execute a command
compress_cmd = client.generate_ffmpeg_command(
    operation="compress",
    input_file="input.mp4",
    crf="18",
    preset="slow",
    execute=True  # This will execute the command immediately
)
print(compress_cmd["execution_result"]["status"])
```

## Supported Operations

The toolkit can generate commands for the following FFmpeg operations:

- **trim**: Cut a segment from a video
- **convert**: Convert video to a different format
- **compress**: Compress video with customizable quality
- **extract_audio**: Extract audio track from video
- **scale**: Resize video dimensions
- **overlay**: Add an overlay to a video
- **concat**: Concatenate multiple video files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.