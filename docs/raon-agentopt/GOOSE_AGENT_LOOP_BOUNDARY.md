> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Goose Agent loop 경계

## 소유권과 실행(F)

session/builder.rs → Agent::new → provider create/update_provider → Agent::reply → provider stream → tool execution → conversation persistence → 다음 inference로 이어진다. goose/src/agents/agent.rs에는 기존 reply loop와 reply_with_state_machine가 공존한다. state_machine/mod.rs의 GOOSE_STATE_MACHINE opt-in은 기본 false다. goose-agent는 재사용 가능한 machine/operation/inference alpha crate이며 기존 loop 전체가 대체됐다는 뜻은 아니다.

state_machine/ops_llm.rs는 GooseInferenceProvider로 inner Provider stream을 호출한다. 같은 디렉터리에 tool approval/calling/retry/max turns/compaction/recipe/skills/steering/hooks와 effects/session 처리가 있다. 모델 대화 retry는 canonical Request 생성 idempotency가 아니다. subagent_handler.rs, subagent_execution_tool/, scheduler/orchestrator, recipes는 추가 autonomous execution 경로다.

SessionManager의 sessions.db/conversation/cwd/provider/extension state가 로컬 truth다. tool_execution 및 extension_manager는 subprocess/filesystem 또는 remote MCP를 실행한다. Goose permission/mode/confirmation과 AgentOpt project/auth/Score/Validation은 동일 계약이 아니다.

## RAON 소유권(P)

| 기능 | CLI | AgentOpt V2 |
|---|---|---|
| 입력/terminal/diff 검토 | 소유 | event/result 제공 |
| repo selection/manifest/apply | bounded local Git UX | accepted base/delivery binding |
| identity/ordering/retry/resume | request_id/cursor cache | canonical Request/event log |
| project/auth/Score/context | catalog 선택 | acceptance snapshot/검증 |
| schedule/workspace/Provider | 없음 | 기존 Scheduler/Worker/Provider |
| validation/evidence | 조회, local receipt 구분 | 서버 truth |
| local build/tool | 첫 PoC 없음 | 향후 signed Local Runner contract |

제외: Agent::reply, goose-agent machine/inference, provider registry/model API, local ACP Provider process, subagents/recipes/scheduler, hooks, remote extension auto-load, roaming/gateway/local inference/voice. CLI session은 project/request/manifest digest/cursor/apply receipt cache만 보관한다. 모델 메시지 자체 truth나 autonomous queue를 만들지 않는다. resume/messages는 서버 계약을 사용하며 UI reconnect가 새 inference를 시작하지 않는다.

후속 검증: CLI dependency graph에서 goose-agent/goose-providers를 제외하고 위조 tool event로 shell이 실행되지 않는지 확인한다. Provider 환경변수/Goose config/recipe가 모델 endpoint나 local agent process를 활성화할 수 없어야 한다. goose-cli/Cargo.toml에는 goose/goose-providers가 unconditional dependency이므로 --no-default-features만으로 이 경계가 확보되지 않는다.
