# Development Plan

## Project Overview
This project creates Python clients for various Chutes AI services, providing both library interfaces and CLI tools for image generation, video generation, and background removal. The architecture follows consistent patterns established in `chutes_hidream.py` and `chutes_image.py`.

## Technical Architecture

### Core Design Patterns
1. **Pydantic Models**: Request/response validation with field constraints
2. **Dual Interface**: Sync/async methods for all operations
3. **Retry Logic**: Tenacity-based exponential backoff with structured error handling
4. **Client-CLI Pattern**: Separate client classes with Fire-based CLI wrappers
5. **Model Registry**: Centralized metadata about available models/endpoints

### Technology Stack
- **Language**: Python 3.12+ with modern type hints
- **HTTP**: `requests` (sync) + `aiohttp` (async)
- **CLI**: `fire` framework for command-line interfaces
- **Validation**: `pydantic` for data models
- **Retry**: `tenacity` for robust error handling
- **Logging**: `loguru` for structured logging
- **Utils**: `python-slugify`, `pathvalidate`, `PIL`

## Phase 1: SkyReels Video Generation Client (`chutes_skyreels_vid.py`)

### Objectives
Create a comprehensive client for SkyReels-V2-14B video generation API following established patterns.

### Implementation Steps

#### 1. Core Infrastructure Setup
- Add file header with UV script dependencies
- Import all necessary libraries matching existing patterns
- Set up environment variable loading and constants
- Define API endpoints and default configurations

#### 2. Pydantic Model Design
- `SkyreelsVideoRequest`: Complete parameter model with validation
  - All 15+ parameters from schema.json with proper types/constraints
  - Support for resolution enum (720P/540P)
  - Optional image inputs (first/last frame base64)
  - Video timing parameters (fps, num_frames, etc.)
- `SkyreelsVideoResponse`: Structured response model
  - Success/failure status
  - Video URL or binary data
  - Generation metadata (timing, parameters used)
  - Comprehensive error information

#### 3. Client Class Implementation (`SkyreelsClient`)
- **Initialization**: API key validation, timeout configuration, headers setup
- **Request Handling**: 
  - Sync/async HTTP methods with retry logic
  - Binary video response handling (MP4 content)
  - Streaming response support if available
  - Comprehensive error handling with context

#### 4. Core Generation Methods
- `text_to_video_sync/async`: Text-only video generation
- `image_to_video_sync/async`: Image-guided video generation  
- Helper methods for image processing (base64 encoding)
- Utility functions for video format detection and saving

#### 5. CLI Interface (`SkyreelsCLI`)
- **video** command: Main video generation interface
  - Support for both text-to-video and image-to-video modes
  - All parameter options with sensible defaults
  - Output file handling (auto-naming, format detection)
  - Progress indication and error reporting
- **info** command: Display model capabilities and parameter ranges
- **test** command: Quick functionality validation

#### 6. Advanced Features
- **Batch Processing**: Multiple prompt processing
- **Parameter Validation**: Real-time constraint checking
- **File Management**: Smart output naming, directory creation
- **Progress Tracking**: Generation status and timing information

### Success Criteria
- [ ] Complete parameter coverage from schema.json
- [ ] Sync and async operation support
- [ ] Robust error handling with retries
- [ ] CLI interface with all major options
- [ ] Binary video response handling
- [ ] Comprehensive logging and debugging
- [ ] Input validation and sanitization
- [ ] Output file management

## Phase 2: WAN Video Generation Client (`chutes_wan_vid.py`)

### Objectives
Create a comprehensive client for WAN 2.1 FLF2V (First Last Frame to Video) API with specialized image-to-video functionality.

### Key Differences from SkyReels
- **Required Images**: Both first AND last frame images are mandatory (not optional)
- **Single Endpoint**: Only `/flf2video` for image-to-video generation
- **Resolution Format**: Uses `WIDTH*HEIGHT` format (e.g., `1280*720`) with 5 fixed options
- **Parameter Names**: `steps` (not `inference_steps`), `sample_shift` (not `shift`)
- **Frame Range**: 81-241 frames (vs 97-10000 for SkyReels)

### Implementation Steps

#### 1. Core Infrastructure Setup
- File header with UV script dependencies matching established patterns
- Import libraries and set up environment variables
- Define WAN-specific API endpoint: `https://kikakkz-wan2-1-14b-flf2v.chutes.ai/flf2video`
- Set higher timeout (600s) due to complex multi-GPU processing

#### 2. Pydantic Model Design
- `WanVideoRequest`: Parameter model with WAN-specific constraints
  - **Required fields**: `prompt`, `first_image_b64`, `last_image_b64`
  - Resolution enum with 5 options: `1280*720`, `720*1280`, `832*480`, `480*832`, `1024*1024`
  - `frames`: 81-241 range with constraint that `frames % 4 == 1`
  - `steps`: 20-50 (renamed from `inference_steps`)
  - `sample_shift`: 1-7 (different from SkyReels `shift`)
  - `single_frame`: Boolean for image vs video output
- `WanVideoResponse`: Structured response model
  - Binary video/image data handling
  - Enhanced metadata for specialized processing

#### 3. Client Class Implementation (`WanClient`)
- **Image Processing**: Specialized methods for required first/last frame handling
- **Validation**: Ensure both images are provided before API calls
- **Resolution Handling**: Support for WAN's `WIDTH*HEIGHT` format
- **Error Handling**: Account for 8-GPU distributed processing requirements

#### 4. Core Generation Methods
- `image_to_video_sync/async`: Primary generation method (images always required)
- **No text-to-video**: WAN only supports image-guided video generation
- Enhanced image preprocessing matching WAN's requirements (1280x720 target)
- Frame count validation and auto-correction (`frames % 4 == 1`)

#### 5. CLI Interface (`WanCLI`)
- **video** command: Image-to-video generation with required image inputs
  - Mandatory `--first_frame` and `--last_frame` parameters
  - All WAN-specific parameters with proper validation
  - Resolution selection with friendly names mapped to WAN format
  - Auto-filename generation reflecting WAN parameters
- **info** command: Display WAN capabilities and constraints
- **resolutions** command: List available resolution options

#### 6. Advanced Features
- **Image Validation**: Ensure both input images are provided and valid
- **Resolution Mapping**: User-friendly resolution names mapped to WAN format
- **Frame Constraint Handling**: Auto-adjust frame count to meet `% 4 == 1` requirement
- **Output Mode Selection**: Support both video and single-frame output

### Success Criteria
- [ ] Mandatory image input validation and processing
- [ ] All 5 WAN resolution options supported
- [ ] Frame count constraint validation (`frames % 4 == 1`)
- [ ] Proper handling of WAN-specific parameter names and ranges
- [ ] CLI interface clearly indicates required image inputs
- [ ] Error handling for missing or invalid images
- [ ] Binary video and image response handling
- [ ] Comprehensive parameter validation

## Phase 3: REMBG Background Removal Integration

### Objective
Implement chutes_rembg.py module for background removal functionality that integrates with the existing Chutes AI framework.

## Technical Requirements

### Phase 1: Analysis and Understanding

**Objective**: Analyze existing codebase structure and REMBG functionality

**Technical Specifications**:
1. **Existing Chutes Module Analysis**:
   - Study chutes_hidream.py structure: Pydantic models, API client patterns, CLI interface design
   - Study chutes_image.py structure: Model registry, streaming responses, error handling patterns
   - Identify common patterns: authentication, retry logic, logging, configuration management
   - Extract reusable components and design patterns

2. **REMBG Functionality Analysis**:
   - Analyze files in @rembg directory to understand background removal algorithms
   - Identify API endpoints and request/response formats for REMBG services
   - Understand input/output requirements: image formats, processing parameters
   - Document REMBG-specific configuration and model options

### Phase 2: Module Design and Architecture

**Objective**: Design chutes_rembg.py following established framework patterns

**Technical Specifications**:
1. **Pydantic Model Design**:
   - Create RembgRequest model for background removal parameters
   - Define input validation for image data (base64, file paths, stdin)
   - Implement output format specifications (PNG requirements)
   - Add model selection and processing options

2. **Client Architecture**:
   - Implement RembgClient class following existing client patterns
   - Add both synchronous and asynchronous processing methods
   - Integrate tenacity retry logic for robust error handling
   - Implement proper authentication and API key management

3. **I/O Interface Design**:
   - Support stdin/stdout for pipeline integration
   - Support --input and --output file arguments
   - Implement automatic format detection and conversion
   - Ensure PNG output format compliance

### Phase 3: Implementation

**Objective**: Implement chutes_rembg.py with complete functionality

**Technical Specifications**:
1. **Core Functionality**:
   - Background removal processing with REMBG API integration
   - Image format handling (input: various formats, output: PNG)
   - Error handling with meaningful user feedback
   - Progress tracking and logging for long operations

2. **CLI Interface**:
   - Fire-based CLI following established patterns
   - Support for both file-based and stream-based operations
   - Command: `remove_background` with flexible I/O options
   - Help documentation and usage examples

3. **Configuration Management**:
   - Environment variable support (CHUTES_API_KEY, REMBG_API_KEY if needed)
   - .env file integration following existing patterns
   - Default parameter configuration
   - Model selection and quality settings

4. **Integration Features**:
   - Logging with loguru following established patterns
   - Structured error handling with specific exception types
   - Request/response metadata tracking
   - Performance metrics (processing time, file sizes)

### Phase 4: Testing and Validation

**Objective**: Ensure robust functionality and integration

**Technical Specifications**:
1. **Functionality Testing**:
   - Test stdin/stdout pipeline operations
   - Test file-based input/output operations
   - Validate PNG output format compliance
   - Test error scenarios and edge cases

2. **Integration Testing**:
   - Verify compatibility with existing framework patterns
   - Test CLI interface functionality
   - Validate configuration and authentication flows
   - Confirm proper logging and error reporting

3. **Performance Validation**:
   - Test with various image sizes and formats
   - Validate processing time expectations
   - Confirm memory usage efficiency
   - Test concurrent processing capabilities

## Implementation Details

### File Structure
```
chutes_rembg.py
├── Pydantic Models (RembgRequest, RembgResponse)
├── RembgClient Class
├── I/O Utilities (stdin/stdout, file handling)
├── CLI Interface (Fire-based)
├── Error Handling and Logging
└── Configuration Management
```

### API Integration
- REMBG service endpoint integration
- Request formatting and authentication
- Response processing and image extraction
- Error handling for API failures

### I/O Modes
1. **Pipeline Mode**: `cat image.jpg | python chutes_rembg.py remove_background > output.png`
2. **File Mode**: `python chutes_rembg.py remove_background --input image.jpg --output output.png`
3. **Interactive Mode**: CLI prompts for missing parameters

## Success Criteria
- chutes_rembg.py successfully removes backgrounds from input images
- PNG output format is consistently produced
- Both stdin/stdout and file-based I/O modes work correctly
- CLI interface follows established framework patterns
- Error handling and logging are comprehensive and user-friendly
- Module integrates seamlessly with existing Chutes AI framework
- Code follows established quality standards and patterns