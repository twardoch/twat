# Chutes AI Media Generation Suite

Comprehensive Python clients for image and video generation using the Chutes AI platform.

## 1. Overview

This project provides four complete, production-ready Python modules for AI media generation:

- **`chutes_hidream.py`** - HiDream-specific API client for high-quality image generation and editing
- **`chutes_image.py`** - General image generation client supporting 20+ models with parallel processing
- **`chutes_skyreels_vid.py`** - SkyReels video generation client for text-to-video and image-to-video
- **`chutes_wan_vid.py`** - WAN FLF2V client for first-last-frame-to-video generation

## 2. Features

### 2.1. chutes_hidream.py
- ✨ **Text-to-image generation** with HiDream API
- 🎨 **Image editing capabilities** for existing images
- 📐 **7 preset resolutions** (1024x1024, 768x1360, 1360x768, 880x1168, 1168x880, 1248x832, 832x1248)
- 🎯 **Aspect ratio support** - automatically finds closest HiDream resolution
- 🛡️ **Robust error handling** with exponential backoff retries (3 attempts)
- 🔥 **CLI interface** with Fire for direct command-line usage
- 📝 **Comprehensive logging** with Loguru and structured metadata
- ⚡ **Both sync and async** operations supported

### 2.2. chutes_image.py
- 🤖 **20+ image generation models** across 8 categories (anime, artistic, realistic, etc.)
- 🚀 **Multi-model parallel processing** with intelligent worker allocation
- 🔄 **Sync, async, and streaming** API support
- 📊 **Smart model registry** with categorization and filtering
- 🎛️ **Advanced parameter support** (resolution, aspect ratio, guidance scale, etc.)
- 🔥 **Feature-rich CLI** with model discovery and batch processing
- 📈 **Production-grade error handling** with enhanced retry strategies
- 💾 **Automatic file naming** and safe filename generation

### 2.3. chutes_skyreels_vid.py
- 🎬 **Text-to-video generation** from text prompts
- 🖼️ **Image-to-video generation** with optional first/last frame images
- 📺 **2 resolution options** (720P HD, 540P SD) optimized for SkyReels
- ⚡ **Advanced video parameters** (97-10000 frames, 16-60 FPS, shift controls)
- 🛡️ **Robust retry logic** with exponential backoff for long video operations
- 🔥 **CLI interface** with comprehensive parameter support
- 📝 **Comprehensive logging** for video generation workflows
- ⚡ **Both sync and async** operations supported

### 2.4. chutes_wan_vid.py
- 🎯 **First-Last-Frame-to-Video** specialized generation (both images required)
- 📐 **5 resolution options** (landscape HD, portrait HD, wide, tall, square)
- 🎛️ **WAN-specific parameters** (81-241 frames with 4n+1 constraint, sample shift)
- 🖼️ **Single frame mode** for image interpolation between frames
- 🔧 **User-friendly resolution names** with automatic format mapping
- 🛡️ **Enhanced validation** for mandatory image inputs and constraints
- 🔥 **CLI interface** with required parameter enforcement
- 💪 **8-GPU distributed processing** support (H100/H800/H200)

## 3. Installation

The modules use uv script dependencies. Simply run them directly:

```bash
# Image generation modules
python chutes_hidream.py --help
python chutes_image.py --help

# Video generation modules
python chutes_skyreels_vid.py --help
python chutes_wan_vid.py --help
```

Required dependencies are automatically managed via uv.

## 4. Configuration

Set your Chutes API key as an environment variable:

```bash
export CHUTES_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
CHUTES_API_KEY=your-api-key-here
```

## 5. Usage

### 5.1. Command Line Interface

#### 5.1.1. HiDream Commands

```bash
# Generate image with HiDream
python chutes_hidream.py image "a beautiful sunset" --output sunset.jpg

# Edit existing image (image path first, then prompt)
python chutes_hidream.py edit input.jpg "make it brighter" --output bright_image.jpg

# Use aspect ratio (finds closest HiDream resolution)
python chutes_hidream.py image "landscape photo" --ar "16:9" --output wide.jpg

# List available resolutions
python chutes_hidream.py resolutions

# List available models
python chutes_hidream.py list

# Get model information
python chutes_hidream.py info "hidream-v1"
```

#### 5.1.2. General Image Generation

```bash
# Generate with default model (FLUX.1-dev)
python chutes_image.py image "a beautiful landscape"

# Use specific model
python chutes_image.py image "anime girl" --model "Animij"

# Multi-model generation (parallel processing)
python chutes_image.py image "cute cat" --model "Animij,HassakuXL,FLUX.1-dev"

# Use all available models (20+ models in parallel)
python chutes_image.py image "fantasy castle" --model "*"

# Use aspect ratio (calculates optimal resolution)
python chutes_image.py image "portrait" --ar "3:4" --model "JuggernautXL"

# Use specific resolution
python chutes_image.py image "wallpaper" --res "1920x1080"

# List all available models
python chutes_image.py list

# Filter models by category
python chutes_image.py list --category anime

# Get model information
python chutes_image.py info "FLUX.1-dev"

# List categories
python chutes_image.py categories
```

#### 5.1.3. SkyReels Video Generation

```bash
# Generate video from text prompt
python chutes_skyreels_vid.py video "a peaceful sunset over calm ocean waves"

# Generate video with custom parameters
python chutes_skyreels_vid.py video "dancing in the rain" --resolution "720P" --fps 24 --num_frames 120

# Image-to-video with first frame only
python chutes_skyreels_vid.py video "transition to night" --first_frame sunset.jpg --fps 24

# Image-to-video with both first and last frames
python chutes_skyreels_vid.py video "morphing landscape" --first_frame day.jpg --last_frame night.jpg

# Show SkyReels capabilities
python chutes_skyreels_vid.py info

# Test API connectivity
python chutes_skyreels_vid.py test
```

#### 5.1.4. WAN FLF2V Video Generation

```bash
# Generate video between two frames (both required)
python chutes_wan_vid.py video "smooth transition" frame1.jpg frame2.jpg

# Use custom resolution and parameters
python chutes_wan_vid.py video "flowing water" start.jpg end.jpg --resolution "landscape_hd" --frames 121 --fps 24

# Generate single interpolated frame instead of video
python chutes_wan_vid.py video "middle frame" image1.png image2.png --single_frame --output middle.png

# Use direct resolution format
python chutes_wan_vid.py video "portrait transition" selfie1.jpg selfie2.jpg --resolution "720*1280"

# Show WAN capabilities and requirements
python chutes_wan_vid.py info

# List available resolutions
python chutes_wan_vid.py resolutions

# Test with sample images
python chutes_wan_vid.py test
```

### 5.2. Library Usage

#### 5.2.1. HiDream API

```python
from chutes_hidream import HidreamClient

client = HidreamClient()

# Generate image synchronously
response = client.generate_sync(
    prompt="a beautiful sunset over mountains",
    res="1024x1024",
    guidance_scale=5.0,
    inference_steps=50
)

if response.success:
    print(f"Image URL: {response.image_url}")
    print(f"Generation time: {response.generation_time:.2f}s")

# Generate image asynchronously
import asyncio

async def generate_hidream():
    response = await client.generate_async(
        prompt="magical forest",
        res="1360x768",
        guidance_scale=6.0
    )
    return response

# Edit image synchronously
response = client.edit_sync(
    prompt="make it brighter and more colorful",
    image_path="input.jpg",
    guidance_scale=5.0,
    image_guidance_scale=4.0,
    inference_steps=28
)

# Edit image asynchronously  
async def edit_hidream():
    response = await client.edit_async(
        prompt="add flowers in the foreground",
        image_path="landscape.jpg",
        negative_prompt="blur, low quality"
    )
    return response
```

#### 5.2.2. General Image Generation

```python
from chutes_image import ChutesImageClient

client = ChutesImageClient()

# List available models and categories
models = client.available_models
print(f"Available models: {len(models)}")

anime_models = client.list_models(category="anime")
print(f"Anime models: {[m.name for m in anime_models]}")

# Generate image synchronously
response = client.generate_sync(
    model="FLUX.1-dev",
    prompt="a futuristic cityscape",
    width=1024,
    height=1024,
    guidance_scale=7.5,
    inference_steps=30
)

# Generate image asynchronously
import asyncio

async def generate_async():
    response = await client.generate_async(
        model="Animij",
        prompt="anime character with blue hair",
        guidance_scale=8.0,
        width=768,
        height=1024
    )
    return response

response = asyncio.run(generate_async())

# Stream generation updates
async def stream_generation():
    async for chunk in client.generate_stream(
        model="FLUX.1-dev",
        prompt="a magical forest",
        guidance_scale=7.0
    ):
        print(f"Stream update: {chunk}")

asyncio.run(stream_generation())
```

#### 5.2.3. SkyReels Video API

```python
from chutes_skyreels_vid import SkyreelsClient

client = SkyreelsClient()

# Text-to-video generation
response = client.text_to_video_sync(
    prompt="a beautiful sunset over mountains",
    resolution="720P",
    fps=24,
    num_frames=97,
    guidance_scale=6.0,
    inference_steps=30
)

if response.success:
    print(f"Video generated in {response.generation_time:.2f}s")
    with open("sunset_video.mp4", "wb") as f:
        f.write(response.video_data)

# Image-to-video generation
from io import BytesIO

response = client.image_to_video_sync(
    prompt="transition from day to night",
    first_frame="day_scene.jpg",
    last_frame="night_scene.jpg",
    resolution="540P",
    fps=24,
    num_frames=120
)

# Async video generation
import asyncio

async def generate_video_async():
    response = await client.text_to_video_async(
        prompt="flowing river in forest",
        resolution="720P",
        num_frames=97,
        fps=24
    )
    return response

response = asyncio.run(generate_video_async())
```

#### 5.2.4. WAN FLF2V API

```python
from chutes_wan_vid import WanClient

client = WanClient()

# Image-to-video generation (both frames required)
response = client.image_to_video_sync(
    prompt="smooth morphing between expressions",
    first_frame="smile.jpg",
    last_frame="serious.jpg",
    resolution="portrait_hd",
    fps=16,
    frames=81,
    guidance_scale=5.0,
    steps=25
)

if response.success:
    print(f"Video generated in {response.generation_time:.2f}s")
    with open("morphing_video.mp4", "wb") as f:
        f.write(response.video_data)

# Single frame interpolation
response = client.image_to_video_sync(
    prompt="interpolated middle frame",
    first_frame="start.png",
    last_frame="end.png",
    single_frame=True,
    resolution="square"
)

if response.success and response.image_data:
    with open("interpolated_frame.png", "wb") as f:
        f.write(response.image_data)

# Async video generation
import asyncio

async def generate_wan_video_async():
    response = await client.image_to_video_async(
        prompt="landscape transformation",
        first_frame="summer.jpg",
        last_frame="winter.jpg",
        resolution="landscape_hd",
        frames=121,
        fps=24
    )
    return response

response = asyncio.run(generate_wan_video_async())
```

## 6. Project Overview

This project creates efficient Python-compatible modules for AI media generation using the Chutes AI platform. The suite includes four specialized modules:

1. **`chutes_hidream.py`** - HiDream-specific APIs for specialized image generation and editing
2. **`chutes_image.py`** - General image generation with support for 20+ models
3. **`chutes_skyreels_vid.py`** - SkyReels video generation for text-to-video and image-to-video
4. **`chutes_wan_vid.py`** - WAN FLF2V for first-last-frame-to-video generation

## 7. Technical Requirements

### 7.1. Core Dependencies

- `python-dotenv` - Environment variable management for CHUTES_API_KEY
- `fire` - CLI interface generation
- `tenacity` - Robust retry logic with exponential backoff
- `loguru` - Enhanced logging with structured output
- `requests` - HTTP client for API calls
- `aiohttp` - Async HTTP client for streaming responses
- `pydantic` - Data validation and serialization

### 7.2. API Integration

- Authentication via Bearer token from CHUTES_API_KEY environment variable
- Support for both synchronous and asynchronous API calls
- Robust error handling with retry mechanisms
- Streaming response support for real-time generation feedback

## 8. Module 1: `chutes_hidream.py` - Hidream API Handler

### 8.1. Features

- **Text-to-image generation** via Hidream API endpoint
- **Image editing capabilities** via Hidream Edit API endpoint
- **Resolution presets**: 1024x1024, 768x1360, 1360x768, 880x1168, 1168x880, 1248x832, 832x1248
- **Configurable parameters**: seed, guidance_scale (0-10), num_inference_steps (5-75)
- **CLI interface** for direct command-line usage
- **Validation** using Pydantic models based on JSON schemas

### 8.2. API Endpoints

- Primary: `https://chutes-hidream.chutes.ai/generate`
- Edit: `https://chutes-hidream-edit.chutes.ai/generate`

### 8.3. Schema Support

- `hidream-schema.json` - Basic text-to-image generation
- `hidreamedit-schema.json` - Image editing with text prompts
- Full schema validation with proper error messages

## 9. Module 2: `chutes_image.py` - General Image Generation

### 9.1. Features

- **Multi-model support** for various image generation models
- **Unified interface** for all supported models
- **Model auto-discovery** from existing model files
- **Configurable parameters**: seed, width, height, guidance_scale, negative_prompt, inference_steps
- **Streaming support** for real-time generation updates
- **CLI interface** with model selection and parameter tuning

### 9.2. Supported Models

The chutes_image.py module supports 20+ models across 8 categories:

**General Models (6)**
- FLUX.1-dev - High-quality text-to-image generation
- Qwen/Qwen-Image - Advanced Qwen image generation 
- qwen-image - Simplified Qwen image generation
- playground-v2.5 - Versatile playground model
- Shitao/OmniGen-v1 - Omnipotent generation model

**Anime Models (4)**
- Animij - Anime-style image generation
- HassakuXL - High-quality anime generation
- Illustrious-XL - High-resolution anime illustration
- Ilustrij - Illustration-focused anime model

**Realistic Models (1)**
- JuggernautXL - High-resolution realistic image generation

**Artistic Models (4)**
- chroma - Chromatic artistic generation
- diagonalge/ConstShaper - Constraint-based artistic shaping
- iLustMix - Mixed artistic style generation
- Lykon/dreamshaper-xl-1-0 - Versatile XL model for various styles

**Character Models (1)**
- diagonalge/Booba - Specialized character generation model

**Cartoon Models (1)**
- nova-cartoon-xl - Cartoon-style generation

**Furry Models (1)**
- NovaFurryXL - Furry character generation

**Specialized Models (3)**
- orphic-lora - LoRA-based specialized model
- ostris/Flex.1-alpha - Flexible experimental model
- neta-lumina - Luminous specialized generation

### 9.3. API Endpoints

- Primary: `https://image.chutes.ai/generate`
- Model-specific endpoints where applicable

## 10. Implementation Details

### 10.1. Error Handling Strategy

- **Connection errors**: Retry with exponential backoff (3 attempts max)
- **Rate limiting**: Respect 429 status codes with proper delays
- **Validation errors**: Clear error messages with schema violations
- **Timeout handling**: Configurable timeouts for different operations
- **Graceful degradation**: Fallback options when primary endpoints fail

### 10.2. Logging Strategy

- **Structured logging** with request/response details
- **Performance metrics** (request duration, retry counts)
- **Debug mode** for detailed API interaction logging
- **Error tracking** with full stack traces
- **CLI output** with progress indicators and status updates

### 10.3. CLI Interface Design

- **Subcommands** for different operations (generate, edit, list-models)
- **Parameter validation** with helpful error messages
- **Output options** (JSON, image file, stdout)
- **Configuration file support** for default parameters
- **Help documentation** with examples

### 10.4. Code Architecture

- **Pydantic models** for request/response validation
- **Base classes** for common functionality
- **Async/sync wrappers** for different use cases
- **Plugin system** for easy model additions
- **Configuration management** with environment variables

## 11. Quality Assurance

### 11.1. Testing Strategy

- **Unit tests** for all API methods
- **Integration tests** with mock API responses
- **CLI tests** for command-line interface
- **Error scenario testing** for robust error handling
- **Performance benchmarks** for optimization

### 11.2. Code Quality

- **Type hints** throughout the codebase
- **Docstring documentation** with usage examples
- **Code formatting** with black/ruff
- **Linting** with comprehensive rules
- **Security scanning** for API key handling

## 12. Deployment Considerations

### 12.1. Environment Setup

- **Virtual environment** management
- **Dependency pinning** for reproducible builds
- **Environment variable validation** on startup
- **Configuration documentation** for deployment

### 12.2. Usage Patterns

- **Library usage** - Import and use in Python scripts
- **CLI usage** - Command-line tool for direct usage
- **Async usage** - Integration with async frameworks
- **Batch processing** - Multiple image generation workflows


*(See `python chutes_image.py list` for complete list)*

## 13. API Endpoints

### 13.1. Image Generation APIs
- **HiDream Generate**: `https://chutes-hidream.chutes.ai/generate`
- **HiDream Edit**: `https://chutes-hidream-edit.chutes.ai/generate`
- **General Image**: `https://image.chutes.ai/generate` (streaming)

### 13.2. Video Generation APIs
- **SkyReels Text-to-Video**: `https://kikakkz-skyreels-v2-14b-540p.chutes.ai/text2video`
- **SkyReels Image-to-Video**: `https://kikakkz-skyreels-v2-14b-540p.chutes.ai/image2video`
- **WAN FLF2V**: `https://kikakkz-wan2-1-14b-flf2v.chutes.ai/flf2video`

## 14. Error Handling

All modules include production-grade error handling:

### 14.1. chutes_hidream.py
- **Exponential backoff retries**: 3 attempts with 2-8 second delays
- **Request/Response validation**: Pydantic model validation with clear error messages
- **API error handling**: Handles both JSON and binary image responses
- **Timeout management**: Configurable timeouts (default: 120s)
- **Detailed error context**: Full parameter logging and error classification

### 14.2. chutes_image.py
- **Enhanced retry strategy**: 3 attempts with 5-30 second delays for server errors
- **Intelligent error classification**: Different handling for 503/500/429/404 errors
- **Multi-model error handling**: Continues processing other models if some fail
- **Resource management**: Smart worker allocation to prevent API overload
- **Detailed error reporting**: Complete context including model, parameters, and retry attempts

### 14.3. chutes_skyreels_vid.py
- **Extended timeout handling**: 1200-second timeout for video generation processes
- **Video-specific retries**: 3 attempts with 5-30 second delays optimized for video APIs
- **Binary response handling**: Robust processing of MP4 video data streams
- **Parameter validation**: Comprehensive validation of video parameters and constraints
- **Image processing errors**: Detailed error handling for base64 image encoding/decoding

### 14.4. chutes_wan_vid.py
- **Extended timeout handling**: 1200-second timeout for complex 8-GPU distributed processing
- **Mandatory input validation**: Strict enforcement of required first and last frame images
- **Frame constraint validation**: Auto-correction of frame counts to meet 4n+1 requirement
- **Resolution mapping errors**: Clear error messages for invalid resolution specifications
- **Distributed processing errors**: Enhanced error handling for multi-GPU video generation

## 15. Logging

Structured logging is provided via Loguru:

- **Request/response details**: Full API interaction logging with metadata
- **Performance metrics**: Generation times, retry counts, and parallel execution timing
- **Debug mode**: Verbose logging for troubleshooting with parameter context
- **CLI output**: Progress indicators, status updates, and error summaries
- **Error classification**: Specific error types with helpful user suggestions

## 16. Testing

Run the included test suite:

```bash
python test_modules.py
```

This validates:
- ✅ Module imports and initialization (chutes_hidream, chutes_image)
- ✅ Pydantic model validation (HidreamGenerateRequest, ImageGenerationRequest)
- ✅ CLI interface functionality (HidreamCLI, ChutesImageCLI)
- ✅ Model registry completeness (20+ models across 8 categories)
- ✅ Safe filename and utility functions

## 17. Key Features Summary

### 17.1. chutes_hidream.py
- **7 preset resolutions** with aspect ratio support
- **Image editing capabilities** with base64 handling
- **Sync/async operations** with comprehensive error handling
- **CLI with Fire** for direct command-line usage
- **Pydantic validation** with field aliases for API compatibility
- **Exponential backoff retries** (3 attempts, 2-8s delays)

### 17.2. chutes_image.py  
- **20+ models** across 8 categories with intelligent registry
- **Multi-model parallel processing** with worker allocation
- **Advanced parameter support** (resolution, aspect ratio, guidance)
- **Production-grade error handling** with enhanced retry strategies  
- **Smart filename generation** and safe file handling
- **CLI with batch processing** and model discovery

### 17.3. chutes_skyreels_vid.py
- **Dual video generation modes** (text-to-video and image-to-video)
- **2 resolution options** (720P, 540P) optimized for SkyReels
- **Advanced video parameters** (97-10000 frames, 16-60 FPS, shift controls)
- **Extended timeout handling** (1200s) for video generation processes
- **Comprehensive image processing** with base64 encoding/decoding
- **CLI with video-specific** parameter validation and output handling

### 17.4. chutes_wan_vid.py
- **Specialized FLF2V generation** with mandatory first/last frame inputs
- **5 resolution options** with user-friendly naming and format mapping
- **Frame constraint enforcement** (4n+1 requirement with auto-correction)
- **Single frame interpolation** mode for image generation between frames
- **Extended timeout handling** (1200s) for 8-GPU distributed processing
- **CLI with mandatory parameter** enforcement and enhanced validation

## 18. Requirements

- **Python 3.11+** (uses modern type hints and syntax)
- **uv** (for automatic dependency management via script headers)
- **Chutes API key** (set as CHUTES_API_KEY environment variable)

## 19. Dependencies

All modules automatically manage dependencies via uv script headers:

```python
# dependencies = [
#   "aiohttp", "requests", "pydantic", "fire", "tenacity", 
#   "loguru", "python-dotenv", "asyncio", "python-slugify", 
#   "pathvalidate", "pillow"
# ]
```

## 20. License

See project license for details.