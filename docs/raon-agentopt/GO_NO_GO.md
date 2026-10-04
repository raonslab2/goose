> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# GO / NO-GO

**새 work_id로 승인할 Windows 우선 Option C PoC는 조건부 GO. 현재 production 및 Goose CLI/core 전체 재사용은 NO-GO.** Goose terminal UX 일부를 참고·추출하되 AgentOpt V2만 canonical 실행엔진으로 유지한다. API/auth/Provider/Runner/installer/UI/egress/배포 구현은 이번 GO가 승인하지 않는다.

근거: CLI builder는 local Agent/Provider를 생성하고 기본 feature에 scheduler/telemetry/OTEL/local inference/update가 포함된다. config/branding만으로 실행 소유권을 바꿀 수 없다. AgentOpt는 이미 Request/idempotency/SSE/Score/evidence primitive를 제공하며 ACP translation 없이 사용 가능하다. Git은 shell/file capability이지 transactional snapshot/apply 제품 계약이 아니다. [component](GOOSE_COMPONENT_MAP.md), [loop](GOOSE_AGENT_LOOP_BOUNDARY.md), [Provider/ACP](GOOSE_PROVIDER_AND_ACP_MAP.md), [14 Git checks](evidence/synthetic_git_results.json)를 근거로 한다.

| 재사용 후보 | 수정할 부분 | 쓰지 않을 부분 |
|---|---|---|
| output/stream buffer/input/completion | neutral event interface, Agent/provider coupling 제거 | CliSession builder/session truth/Agent::reply/GDK |
| terminal cancellation/approval UI 패턴 | typed server question/idempotent answers | autonomous local tool approvals |
| ignore/import/Git process 안전 패턴 | 신규 bounded typed manifest/apply | arbitrary shell/SSH/hooks |
| build/platform 지식 | own CLI auth/keyring/release namespace | Electron/voice/roaming/gateway/local inference |
| upstream attribution | per-file 수정 표시/patch register | Provider/local ACP agent/scheduler/subagent/recipe/MCP auto-load |

최소 API gap: public CLI user auth edge, immutable Mode1 repo/SHA acceptance, complete portable base/file-hash delivery manifest, typed approval/answers. Mode2 CAS 실행/retention은 후속 별도 gate, Mode3 signed runner는 미래다. [CLI 계약](AGENTOPT_CLI_PRODUCT_CONTRACT.md) 참조. Score는 pinned advisory context이며 권한/Validation proof가 아니다.

예상 divergence(P): upstream core patch 0, 별도 CLI crate/repo와 borrowed UI 2–6 file 후보. extraction 비용이나 transitive core dependency가 크면 generic terminal crates로 Goose 재사용량을 줄인다. 현재 docs branch는 production source 변경 0이다.

주요 위험: CLI auth gap, snapshot/model/log secret 노출, stale-base/race overwrite, local autonomy/MCP, telemetry 문서 불일치/onboarding bypass, upstream updater identity, project cache 격리, Windows path/ACL/reparse/CRLF, 미검증 signing/license closure. [보안](GOOSE_SECURITY_LICENSE_REVIEW.md)과 [전송](LOCAL_GIT_TRANSFER_CONTRACT.md)에 대응책과 미검증 영역을 명시했다.

## 후속 변경 repo와 범위

새 RAON CLI repo/package(명칭 추후 지정): client/Git/renderer/tests. AgentOpt V2 repo: 최소 auth/immutable binding/manifest만 별도 승인 후 변경. AI_GCS repo는 public auth gateway exchange가 필요할 때만 검토하며 UI 변경은 기본 제외. Agent.Tools Score schema/content는 변경하지 않고 server catalog binding을 사용한다. goose fork는 upstream reference/분석 위치로 유지한다.

첫 slice는 sample remote-Git Mode1, ps/watch/result/evidence 후 bounded text diff/apply다. Mode2 local-only는 다음 gate, Local Runner는 구현 범위 밖이다. 새 Provider 엔진을 만들지 않는다.

## 객관적 acceptance

1. Windows 11 x64/Linux 합성 repo에서 UTF-8/공백/CRLF/clean/dirty/index/untracked/ignore/worktree 검증. traversal/symlink/junction/ADS/case collision 거부. apply 성공, stale refusal, double apply no-op, crash/concurrent-edit recovery.
2. revocable 짧은 user auth, forbidden project/Request 차단. PC에 trusted proxy secret/Provider credential 없음. keyring/ACL 실측.
3. CLI-origin Request가 Web의 같은 ID로 조회, Web-origin ID가 CLI watch/result/evidence로 조회. 동일 key/payload 한 Request, mismatch 409. 동시 retry/disconnect/restart/SSE dedup 보존.
4. immutable accepted SHA와 manifest 보존, local HEAD 변경이 입력을 바꾸지 못함. complete patch/base/file hash 검증, truncation/missing artifact 거부. Provider/Validation/Evidence/local receipt 구분.
5. Score identity/hash/release/manifest acceptance snapshot, project isolation/work_order version·hash replay 보존.
6. dependency graph에 Goose agent/providers 없음. forged tool/repository hint/hooks/config/env가 local model/shell/MCP를 활성화하지 못함.
7. canary packet test에서 모델/PostHog/OTEL/metadata egress 없음. 승인 auth/API만 사용, Git/update/build local egress 예외는 별도 설명. 서버 Provider credential/egress 유지.
8. Rust pin/Windows/Linux build/focused tests, borrowed file/dependency/build size/time/conflict 실측. release 전 SBOM/third-party license/수정 표시 검증. 고객 installer 배포는 PoC 범위 밖.
9. Mode2는 deterministic remote-less manifest/idempotency/secret bounds/expiry/cleanup/isolated workspace를 별도 검증. Mode3는 새 signed-lease 승인 필요.

## 검증 한계와 안전 종료

fork lineage/license/pin과 합성 Git은 확인했다. Rust/cargo 부재로 Goose build/focused tests NOT RUN. Windows/macOS/ACP/auth/signing/telemetry network runtime과 전체 dependency license audit는 미검증이다. production readiness PASS를 주장하지 않는다.

이 작업의 명령은 production 서비스/DB/Request를 조작하지 않았고 AgentOpt source만 읽었다. production DB snapshot 비교는 하지 않았으므로 이 진술은 작업 수행 범위에 대한 확인이다. 결과는 fork와 문서만 Git에 전달한다. 후속 구현은 반드시 새로운 work_id와 지시가 필요하다.
