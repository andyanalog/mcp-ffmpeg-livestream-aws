# MCP FFmpeg LiveStream AWS Toolkit

A comprehensive toolkit for FFmpeg video processing, live streaming operations, and AWS media services integration.

## Overview

This project provides a set of tools to simplify common video processing tasks, live streaming operations, and AWS media service interactions through a unified interface. It integrates with FFmpeg for video manipulation and offers convenient access to documentation for FFmpeg, various live streaming protocols, and AWS media services.

## Example

In this example, we can see how Claude trims a video of our local machine using ffmpeg.

https://github.com/user-attachments/assets/858ff2f0-8e35-429b-ac91-a11e0fde3c5a



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

## Documentation Tools

### Extract-Web-Page-Content-Tool
Tool to extract page content in text format

### Generate-FFmpeg-Command
Generate FFmpeg command for common video operations

### Get-Documentation-URLs
Retrieve URLs for official documentation of ffmpeg, live streaming, or AWS services

### Get-Service-Documentation
Extract content from specific service documentation

### Run-FFmpeg-Command
Run FFmpeg commands directly on the local system

### Search-Documentation
Search for specific term across documentation URLs

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
