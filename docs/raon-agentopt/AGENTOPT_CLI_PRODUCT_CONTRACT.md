> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# 최소 CLI 제품 계약 초안

P: 별도 agentopt binary이며 명령 이름은 확정되지 않았다. Goose run/session/configure의 local-agent 의미를 유지하지 않는다. 첫 slice에서 interactive chat은 제외한다. network command는 향후 auth edge의 짧은 user token으로 실행하며 서버가 project membership을 검증한다. trusted-proxy secret/header 권한은 PC에 배포하지 않는다.

| 명령 후보 | local side effect | server API(F existing/P gap) | auth/Request | source | output/evidence | 실패·재시도 |
|---|---|---|---|---|---|---|
| login | OS keyring token/expiry | P device/PKCE exchange, F session 조회 | user-scoped token | 없음 | identity/scopes | refresh, token log 금지 |
| projects | catalog cache | F GET projects | membership | 없음 | 허용 project | GET retry/stale 표시 |
| use project | local 선택 저장 | F projects 확인 | 선택≠권한 | 없음 | project/provider/Score | forbidden 거부 |
| init | 명시적 .agentopt 설정, cache ignore, HEAD/status | F projects/scores, P repo binding | project/repo fingerprint | 자동 upload 없음 | base/dirty/exclusions | repo 없음 거부, remote 없음 허용 |
| run instruction | 전송 전 durable key/journal, manifest preview | F POST requests, P immutable input/snapshot | owner/project/key, optional work_order/Score | Mode1 SHA, Mode2 opt-in content | canonical request_id | timeout 동일 key/payload, mismatch 409 |
| ps | cache/cursor | F GET requests | project/owner | 없음 | canonical state | GET retry |
| watch request | cursor 저장, rendering | F detail/events after/Last-Event-ID | 동일 Request, reconnect auth | 없음 | stream/질문/terminal | cursor dedup, local tool 실행 없음 |
| diff request | hash-verified cache | F terminal detail/patch snapshot, P manifest | Request/evidence snapshot | patch 수신 | base/truncation/exclusions | nonterminal 409, incomplete apply 거부 |
| apply request | 승인된 file mutation/rollback receipt | F patch/artifacts, P optional receipt | request/base/input/evidence binding | upload 없음 | changed paths/hashes/local receipt | dry-run/stale 거부, double apply no-op |
| result request | read/cache | F detail | canonical Request | 없음 | outcome와 validation 구분 | evidence 임시실패 GET retry |
| evidence request | 지정 폴더 download, overwrite 금지 | F detail/artifacts/patch | owner/snapshot | 승인 artifact만 | Score/context/validation/Git 한계 | digest/path/expiry 확인 |

API source는 Provider/ACP 문서에 기록한 pin의 app.py다. public CLI login API가 이미 존재한다는 뜻이 아니다. HTTPS SSE로 시작하며 WSS 필수 요건은 없다. watch 질문 응답은 messages의 answers+idempotency를 활용할 수 있지만 formal approval event ID/schema/허용 상태를 확정해야 한다. event 조회≠shell 승인이다.

cache는 user/server/project/request별 분리, token은 keyring, 일반 log에 source/prompt/token 기록 금지. use로 기존 Request project를 변경할 수 없다. Web-created Request를 ID로 조회하며 Goose session을 만들지 않는다. offline이면 cached local status/diff에 stale 표시, autonomous 실행/자동 queue 전송 없음.

idempotency journal은 POST 전 원래 payload/digest/key를 원자적으로 저장한다. retry에서 prompt/Score/attachment를 바꾸지 않는다. 다른 지시는 새 operation/key다. work_order의 work_id/version/content_hash와 request_id를 구분한다. SSE 종료 후 detail을 다시 읽어 Provider completion/Validation/Evidence/Git delivery를 구분한다.

## 최소 API gap(P)

1. public user CLI auth edge: rotation/revoke/scopes/project isolation. trusted header는 내부 경계에서만 생성.
2. Mode1 immutable repo identity/SHA acceptance. CreateRequest는 extra forbid이고 configured checkout은 사용자 지정 immutable-SHA 계약이 아니다.
3. complete portable delivery manifest: base/input/evidence digest, pre/post file hashes/modes, patch/artifacts, untracked/binary/truncation.
4. Mode2 CAS upload/manifest/retention/temp-workspace 실행. attachments/references≠실행 snapshot.
5. typed approval/question/answer idempotency; local receipt와 서버 Validation 분리.
6. future Local Runner signed lease/capability/attestation. 첫 PoC 제외.

API/CLI 구현은 새로운 work_id로 지시받아야 한다. 이번 작업에서는 endpoint나 client를 만들지 않는다.
