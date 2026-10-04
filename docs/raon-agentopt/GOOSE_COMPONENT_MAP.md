> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Goose 구성요소 지도

| 영역 | upstream source 경로 | 확인한 구조(F) | RAON 설계 판단(P) |
|---|---|---|---|
| workspace | Cargo.toml, rust-toolchain.toml | crates/* + vendor/v8, version 1.53.0; 별도 alpha GDK crates | 고정 release에서 선택적 재사용 |
| CLI | crates/goose-cli/src/main.rs, cli.rs, lib.rs | clap Command dispatch; goose binary; CliSession library export | 독립 parser와 작은 UX 모듈 |
| interactive | session/builder.rs, mod.rs, input.rs, editor.rs, completion.rs, paste.rs | rustyline 입력; builder에서 Agent와 Provider 생성 | UI와 실행 분리 필요 |
| stream | session/output.rs, streaming_buffer.rs, thinking.rs, task_execution_display/ | terminal/tool/thinking 렌더링, Goose event 타입 결합 | canonical event용 중립 renderer |
| run/session | cli.rs, commands/session.rs, goose/src/session/session_manager.rs | 비대화 Run, 대화 Session, SQLite sessions.db/cwd/history/export/import | Request cache로 대체 |
| agent | goose/src/agents/agent.rs, state_machine/, goose-agent/src/ | legacy reply와 opt-in state machine, inference/tool/retry/approval/compaction | 제외 |
| providers | goose/src/providers/provider_registry.rs, goose-providers/src/lib.rs, goose-provider-types/src/base.rs | factory, HTTP adapters, provider 타입 | 직접 모델 실행 제외 |
| declarative | goose-providers/src/declarative/, goose/src/config/declarative_providers.rs | JSON definitions + custom config | canonical Request adapter로는 부적합 |
| ACP | goose/src/acp/provider.rs, server.rs, server_factory.rs, transport/ | 외부 agent client 및 Goose server 양방향 | 향후 protocol facade 후보 |
| MCP | goose/src/agents/extension_manager/, mcp_client.rs, config/extensions.rs, goose-mcp/ | builtin/stdio/HTTP/OAuth/tool ownership | 첫 PoC 비활성화 |
| file/shell | agents/platform_extensions/developer/{mod,edit,shell,tree}.rs | 직접 fs 읽기/쓰기/문자열 편집, shell, ignore tree | Git apply 정책은 신규 필요 |
| hints | hints/load_hints.rs, import_files.rs | .git root/ignore/import metadata 경계 | 권한 없는 context 데이터 |
| scheduler | platform_extensions/{scheduler,orchestrator}.rs, subagent_handler.rs, CLI commands/schedule.rs | scheduler/subagent/recipe | AgentOpt 중복, 제외 |
| security | config/{base,paths,permission,tls}.rs, security/, subprocess.rs | keyring/file, scanner, approval, TLS/process | approval는 sandbox가 아님 |
| release | goose-cli/Cargo.toml, .github/workflows/{release,bundle-windows,bundle-macos}.yml, commands/update.rs | Rust CLI, platform bundle/provenance, 별도 Electron | CLI-only로 축소 |
| telemetry | goose/src/posthog.rs, otel/, goose-cli/src/logging.rs | consent + 별도 onboarding 경로, OTEL/log | compile 제외 우선 |

표의 session/agents/config 경로는 각각 앞서 표시한 crate의 src 하위다. 상세 파일별 pin/hash/검색 위치와 영구 링크는 [source manifest](evidence/source_manifest.json)에 있다.

CUSTOM_DISTROS.md 그림만 보고 모든 CLI가 ACP를 경유한다고 해석하면 안 된다. 실제 session/builder.rs는 Agent::new, provider create, update_provider를 호출한다. 문서의 goose/src/providers/declarative/ 경로도 현재 존재하지 않으며 실제 구현은 goose-providers/src/declarative/다.

CLI Command에는 configure/info/session/run/acp(stdio)/serve(HTTP·WS), recipe 관련 명령, skills/plugin/doctor/update/term/review와 feature에 따른 schedule/roam 등이 있다(cli.rs). RAON에서는 별도 agentopt binary를 사용한다. 기존 run/session/configure의 로컬 실행 의미를 그대로 유지하지 않는다.
