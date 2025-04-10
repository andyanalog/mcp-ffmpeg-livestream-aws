import httpx
import subprocess
import shlex
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union
import os

# Initialize MCP with ffmpeg focus and required dependencies
mcp = FastMCP(
    'mcp-ffmpeg-livestream-aws',
    dependencies=['beautifulsoup4']
)

# Dictionary of documentation URLs organized by service
DOCUMENTATION_URLS = {
    # FFmpeg documentation
    "ffmpeg": {
        "main": "https://ffmpeg.org/documentation.html",
        "wiki": "https://trac.ffmpeg.org/wiki",
        "ffmpeg_docs": "https://ffmpeg.org/ffmpeg.html",
        "ffprobe_docs": "https://ffmpeg.org/ffprobe.html",
        "ffplay_docs": "https://ffmpeg.org/ffplay.html",
        "filters": "https://ffmpeg.org/ffmpeg-filters.html",
        "formats": "https://ffmpeg.org/ffmpeg-formats.html",
        "codecs": "https://ffmpeg.org/ffmpeg-codecs.html",
    },
    
    # Live streaming documentation
    "live_streaming": {
        "rtmp": "https://www.adobe.com/devnet/rtmp.html",
        "hls": "https://developer.apple.com/documentation/http-live-streaming",
        "dash": "https://dashif.org/docs/DASH-IF-IOP-v4.3.pdf",
        "webrtc": "https://webrtc.org/getting-started/overview",
        "srt": "https://www.srtalliance.org/developers/",
        "mpeg_ts": "https://en.wikipedia.org/wiki/MPEG_transport_stream",
    },
    
    # AWS media services documentation
    "aws": {
        "main": "https://docs.aws.amazon.com/",
        "mediaconvert": "https://docs.aws.amazon.com/mediaconvert/",
        "mediapackage": "https://docs.aws.amazon.com/mediapackage/",
        "medialive": "https://docs.aws.amazon.com/medialive/",
        "mediastore": "https://docs.aws.amazon.com/mediastore/",
        "mediaconnect": "https://docs.aws.amazon.com/mediaconnect/",
        "ivs": "https://docs.aws.amazon.com/ivs/",
        "elemental": "https://docs.aws.amazon.com/elemental-appliances-software/",
        "s3": "https://docs.aws.amazon.com/s3/",
        "cloudfront": "https://docs.aws.amazon.com/cloudfront/",
    }
}

@mcp.tool(
    name='Extract-Web-Page-Content-Tool',
    description='Tool to extract page content in text format'
)
def extract_web_content(url: str) -> str | None:
    """
    Extract text content from a web page
    """
    try:
        response = httpx.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'
            },
            timeout=10.0,
            follow_redirects=True
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text().replace('\n', ' ').replace('\r', ' ').strip()
    except Exception as e:
        return f'Error fetching content: {str(e)}'

@mcp.tool(
    name='Get-Documentation-URLs',
    description='Retrieve URLs for official documentation of ffmpeg, live streaming, or AWS services'
)
def get_documentation_urls(service_category: str) -> Dict[str, str]:
    """
    Return documentation URLs for the specified service category.
    
    Args:
        service_category: Category of service (ffmpeg, live_streaming, aws, or all)
        
    Returns:
        Dictionary of documentation URLs for the specified service
    """
    if service_category.lower() == "all":
        return DOCUMENTATION_URLS
    
    service_category = service_category.lower()
    if service_category in DOCUMENTATION_URLS:
        return {service_category: DOCUMENTATION_URLS[service_category]}
    else:
        return {"error": f"Service category '{service_category}' not found. Available categories: {list(DOCUMENTATION_URLS.keys())}"}

@mcp.tool(
    name='Get-Service-Documentation',
    description='Extract content from specific service documentation'
)
def get_service_documentation(service_category: str, service_name: str) -> str:
    """
    Get documentation content for a specific service in a category.
    
    Args:
        service_category: Category of service (ffmpeg, live_streaming, aws)
        service_name: Name of the specific service within the category
        
    Returns:
        Text content from the documentation URL
    """
    service_category = service_category.lower()
    service_name = service_name.lower()
    
    if service_category not in DOCUMENTATION_URLS:
        return f"Service category '{service_category}' not found. Available categories: {list(DOCUMENTATION_URLS.keys())}"
    
    if service_name not in DOCUMENTATION_URLS[service_category]:
        return f"Service '{service_name}' not found in category '{service_category}'. Available services: {list(DOCUMENTATION_URLS[service_category].keys())}"
    
    url = DOCUMENTATION_URLS[service_category][service_name]
    return extract_web_content(url)

@mcp.tool(
    name='Search-Documentation',
    description='Search for specific term across documentation URLs'
)
def search_documentation(term: str, service_category: Optional[str] = None) -> Dict[str, str]:
    """
    Search for a term across documentation URLs.
    
    Args:
        term: Term to search for
        service_category: Optional category to limit search (ffmpeg, live_streaming, aws, or all)
        
    Returns:
        Dictionary with URLs and brief content snippets containing the search term
    """
    results = {}
    categories = [service_category.lower()] if service_category and service_category.lower() != "all" else DOCUMENTATION_URLS.keys()
    
    for category in categories:
        if category not in DOCUMENTATION_URLS:
            continue
            
        for service_name, url in DOCUMENTATION_URLS[category].items():
            try:
                content = extract_web_content(url)
                if term.lower() in content.lower():
                    # Find a snippet around the search term
                    term_index = content.lower().find(term.lower())
                    start = max(0, term_index - 100)
                    end = min(len(content), term_index + len(term) + 100)
                    snippet = content[start:end]
                    
                    results[f"{category}:{service_name}"] = {
                        "url": url,
                        "snippet": f"...{snippet}..."
                    }
            except Exception as e:
                results[f"{category}:{service_name}"] = {"error": str(e)}
    
    return results or {"message": f"No results found for '{term}'"}

@mcp.tool(
    name='Run-FFmpeg-Command',
    description='Run FFmpeg commands directly on the local system'
)
def run_ffmpeg_command(command: str) -> Dict[str, str]:
    """
    Execute FFmpeg commands on the local system.
    
    Args:
        command: The FFmpeg command to execute (without the initial 'ffmpeg')
    
    Returns:
        Dictionary with status, output, and error information
    """
    try:
        # Prefix with ffmpeg if not already present
        ffmpeg_cmd = command if command.strip().startswith("ffmpeg") else f"ffmpeg {command}"
        
        # Use shlex to properly handle command arguments
        args = shlex.split(ffmpeg_cmd)
        
        # Run the command with subprocess and capture output
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        return {
            "status": "success" if process.returncode == 0 else "error",
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool(
    name='Generate-FFmpeg-Command',
    description='Generate FFmpeg command for common video operations'
)
def generate_ffmpeg_command(operation: str, input_file: str, **kwargs) -> Dict[str, Union[str, bool]]:
    """
    Generate FFmpeg commands for common operations.
    
    Args:
        operation: Type of operation (trim, convert, compress, extract_audio, etc.)
        input_file: Path to the input video file
        **kwargs: Additional parameters for the specific operation
    
    Returns:
        Dictionary with generated command and option to execute it
    """
    input_file = input_file.replace('\\', '/')  # Normalize path separators
    
    if operation.lower() == "trim":
        start_time = kwargs.get("start_time", "00:00:00")
        end_time = kwargs.get("end_time")
        duration = kwargs.get("duration")
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}_trimmed{os.path.splitext(input_file)[1]}")
        
        if end_time:
            command = f'-i "{input_file}" -ss {start_time} -to {end_time} -c copy "{output_file}"'
        elif duration:
            command = f'-i "{input_file}" -ss {start_time} -t {duration} -c copy "{output_file}"'
        else:
            return {"error": "Either end_time or duration must be specified for trim operation"}
    
    elif operation.lower() == "convert":
        output_format = kwargs.get("output_format", "mp4")
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}.{output_format}")
        
        command = f'-i "{input_file}" "{output_file}"'
    
    elif operation.lower() == "compress":
        crf = kwargs.get("crf", "23")
        preset = kwargs.get("preset", "medium")
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}_compressed{os.path.splitext(input_file)[1]}")
        
        command = f'-i "{input_file}" -c:v libx264 -crf {crf} -preset {preset} -c:a aac -b:a 128k "{output_file}"'
    
    elif operation.lower() == "extract_audio":
        output_format = kwargs.get("output_format", "mp3")
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}.{output_format}")
        
        command = f'-i "{input_file}" -q:a 0 -map a "{output_file}"'
    
    elif operation.lower() == "scale":
        width = kwargs.get("width")
        height = kwargs.get("height")
        scale = kwargs.get("scale")
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}_scaled{os.path.splitext(input_file)[1]}")
        
        if width and height:
            command = f'-i "{input_file}" -vf "scale={width}:{height}" "{output_file}"'
        elif scale:
            command = f'-i "{input_file}" -vf "scale=iw*{scale}:ih*{scale}" "{output_file}"'
        else:
            return {"error": "Either width/height or scale factor must be specified for scale operation"}
    
    elif operation.lower() == "overlay":
        overlay_file = kwargs.get("overlay_file")
        position = kwargs.get("position", "10:10")  # Default position
        output_file = kwargs.get("output_file", f"{os.path.splitext(input_file)[0]}_overlay{os.path.splitext(input_file)[1]}")
        
        if not overlay_file:
            return {"error": "overlay_file must be specified for overlay operation"}
            
        command = f'-i "{input_file}" -i "{overlay_file}" -filter_complex "overlay={position}" "{output_file}"'
    
    elif operation.lower() == "concat":
        file_list = kwargs.get("file_list", [])
        output_file = kwargs.get("output_file", "output_concat.mp4")
        
        if not file_list or not isinstance(file_list, list) or len(file_list) < 2:
            return {"error": "file_list must contain at least 2 files for concat operation"}
            
        # Create temporary file list
        temp_list_file = "temp_file_list.txt"
        with open(temp_list_file, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")
                
        command = f'-f concat -safe 0 -i "{temp_list_file}" -c copy "{output_file}"'
    
    else:
        return {"error": f"Unsupported operation: {operation}"}
    
    # Check if execution is requested and execute the command if needed
    execute = kwargs.get("execute", False)
    result = {
        "operation": operation,
        "command": command,
        "full_command": f"ffmpeg {command}"
    }
    
    if execute:
        execution_result = run_ffmpeg_command(result["full_command"])
        result["execution_result"] = execution_result
    
    return result



if __name__ == "__main__":
    mcp.run(transport='stdio')