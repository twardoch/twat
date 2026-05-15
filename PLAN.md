# twat Ecosystem Modernization Plan

This plan indexes the issue set created for `issues/101.md` and defines the execution order.

## Current State

- [102: Current State Inventory](issues/102-current.md)

## Host Plan

- [103-host: Host Package Implementation Plan](issues/103-host.md)

## Plugin Plans

- [103-twat_audio: Audio domain package](issues/103-twat_audio.md)
- [103-twat_coding: Coding/stub package](issues/103-twat_coding.md)
- [103-twat_ez: Dependency helper package](issues/103-twat_ez.md)
- [103-twat_font: Font organizer package](issues/103-twat_font.md)
- [103-twat_fs: File upload/storage package](issues/103-twat_fs.md)
- [103-twat_genai: Generative media API package](issues/103-twat_genai.md)
- [103-twat_hatch: Package scaffolding package](issues/103-twat_hatch.md)
- [103-twat_image: Image domain package](issues/103-twat_image.md)
- [103-twat_labs: Experimental package](issues/103-twat_labs.md)
- [103-twat_llm: Text-heavy LLM package](issues/103-twat_llm.md)
- [103-twat_mp: Parallel processing package](issues/103-twat_mp.md)
- [103-twat_os: Path/OS utility package](issues/103-twat_os.md)
- [103-twat_search: Search package](issues/103-twat_search.md)
- [103-twat_speech: Speech domain package](issues/103-twat_speech.md)
- [103-twat_task: Task orchestration package](issues/103-twat_task.md)
- [103-twat_text: Text domain package](issues/103-twat_text.md)
- [103-twat_video: Video domain package](issues/103-twat_video.md)

## Parallel Execution Groups

1. Provider and text foundations: `twat_genai`, `twat_llm`, `twat_text`.
2. Media domain packages: `twat_image`, `twat_video`, `twat_audio`, `twat_speech`.
3. Ecosystem support packages: `twat_font`, `twat_fs`, `twat_search`, `twat_coding`.
4. Lightweight support and host packages: host `twat`, `twat_os`, `twat_mp`, `twat_ez`, `twat_hatch`, `twat_task`, `twat_labs`.
5. Consolidation: cross-package install, host discovery, docs consistency, tests, and manual QA.

## Execution Rule

Each group owns disjoint package paths during implementation. Shared boundary decisions are documented in `issues/102-current.md` and repeated in package plans.
