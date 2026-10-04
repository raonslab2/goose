> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Provider·ACP·AgentOpt API 지도

## Provider(F)

goose-provider-types/src/base.rs는 model config/system/messages/tools/stream/usage 인터페이스를 정의한다. goose-providers/src/lib.rs는 모델 HTTP adapters와 declarative providers를 제공하고 goose/src/providers/provider_registry.rs가 factory를 제공한다. direct stream은 legacy agents/agent.rs/reply_parts.rs 및 state_machine/ops_llm.rs를 경유한다.

goose-providers/src/declarative/는 JSON 정의와 factory/macros, config/declarative_providers.rs는 custom config 경로다. AgentOpt adapter를 끼울 수는 있지만 Request execution을 model token stream처럼 표현하게 된다. providers/{codex_acp,claude_acp}.rs와 acp/provider.rs는 로컬 ACP agent process도 지원한다. codex_acp.rs는 executable 탐색과 mode mapping을 수행한다. API key만 제거해도 직접 Provider 실행 제거가 되지 않는다. 이 process는 실행하지 않았다.

P: AgentOpt를 OpenAI-compatible proxy로 사용하지 않는다. chat completion에는 project ownership/work_id version/hash/idempotency/immutable input/Score release·hash/Validation·Evidence/Git delivery가 필수 의미로 없다. metadata나 side channel을 붙이면 별도 Request protocol이 필요해지고 로컬 loop/tool state까지 정합성을 유지해야 한다. credential만 중앙화해도 shell/MCP/network/source egress는 PC에 남는다.

## ACP(F)

- goose acp는 stdio agent server, goose serve는 acp-http feature의 HTTP/WebSocket server다. acp/transport/mod.rs는 /acp, server_factory.rs는 server 생성, server/는 session create/load/fork/prompt/tool/custom dispatch를 구현한다. 서버는 Goose Agent를 실행한다.
- acp/provider.rs는 외부 ACP agent를 Provider처럼 쓰는 client다. generic UI transport 추상화만은 아니다. CLI commands/roam_client.rs도 roaming 구조에 속한다.
- acp/fs.rs 및 tool notification에는 client filesystem/tool capability surface가 있다. transport/auth.rs는 X-Secret-Key 또는 query token과 constant-time 비교, transport/mod.rs는 CORS/WS origin, tls.rs는 TLS를 다룬다. URL token은 로그 노출 위험이 있다.

| 통합(P) | 변경 | canonical 의미 |
|---|---|---|
| Goose serve + 새 UI | UI만 추가, Goose backend 유지 | 두 번째 실행엔진이므로 불충족 |
| Goose ACP Provider → AgentOpt ACP server | facade + client/factory 제한 | session≠Request, durable mapping/metadata 필요 |
| 중립 ACP client → AgentOpt facade | facade와 capability deny-by-default | editor 연동 가치, REST보다 비용 증가 |
| 선택적 CLI UX → AgentOpt REST/SSE | 작은 client crate/Git apply | 기존 identity/event/evidence 직접 활용 |

ACP prompt/session만으로 Score/evidence/status를 완전 표현한다고 단정하지 않는다. 향후 facade는 user/project/session/prompt key→Request durable mapping, 같은 payload replay, mismatch 409, cursor, digest, approval ID, concurrent ordering이 필요하다. reconnect에서 session/new로 작업을 재생성하지 않는다. 첫 PoC는 ACP 없는 REST/SSE다.

## AgentOpt 소스 계약(F)

비교 pin fd18e5151b0b1bcee20e0af05eb73cfdcb12e5e0. agentopt_v2/{app,store,auth,acceptance,scores,evidence,workspaces}.py를 read-only로 확인했다. 공개 문서에는 내부 주소/설정값을 기록하지 않는다.

- CreateRequest(extra forbid): project_id/provider/profile/prompt/attachment_ids/reference_ids, optional work_order(work_id/version/content_hash), score_binding/output_schema, required idempotency_key.
- POST /api/v1/requests: membership/project/provider/profile 검증, owner/project/key 및 normalized payload hash replay, 다른 payload conflict. work_order replay는 별도 binding 경로이며 CLI가 work_id를 임의 생성하지 않는다.
- GET requests/detail/events: sequence SSE, after/Last-Event-ID, terminal 종료. messages/resume/cancel은 별도 mutation이다.
- terminal detail evidence 및 patch?snapshot=.../artifacts. evidence.py에는 untracked가 patch에 포함되지 않을 수 있음과 truncation 한계가 명시된다. 실행 종료≠Validation PASS.
- GET projects/providers/project scores. Score identity는 contract/version/hash/content_ref/release_id/manifest_digest이며 acceptance snapshot을 보존한다. scores.py에서 advisory이며 권한 부여가 아니다.
- auth.py는 trusted loopback proxy identity/shared proxy secret이다. public device/PKCE/Bearer login은 이 소스로 입증되지 않는다. trusted secret/header 권한을 PC에 배포하면 안 된다.

P gap: CLI user auth edge, immutable input binding, snapshot execution/retention, portable complete patch manifest, typed approval 계약. HTTPS+SSE가 현 API와 가장 가깝다. production API나 AI_GCS runtime을 호출하지 않아 운영 버전/실제 Web 동일성은 미검증이다.
