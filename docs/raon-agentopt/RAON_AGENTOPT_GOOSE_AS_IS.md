> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# RAON AgentOpt / Goose AS-IS

## 판단

**조건부 GO: Option C의 선택적 CLI UX 재사용 PoC. 전체 goose-cli를 그대로 기반으로 삼는 것은 NO-GO.** Goose는 local agent 실행에 적합하게 결합돼 있다. RAON에서는 canonical Request를 AgentOpt가 소유하고 CLI는 인증·Git manifest·stream·patch 검토만 소유한다. 생산 구현의 GO가 아니라 새 work_id로 승인할 PoC 설계의 GO다.

## 관측과 안전 경계

- F: GitHub API에서 `aaif-goose/goose`, public, Apache-2.0, default main 확인. 실행 중 main은 기준 SHA와 동일. 비교 ahead=0 / behind=0. 초기 fork 조회 404, 조직 parameter 시도 422(user account), 인증된 사용자 `raonslab2`로 정식 forks API 성공. `raonslab2/goose` public, fork=true, parent/source=`aaif-goose/goose`. [metadata](evidence/fork_metadata.json), [main](evidence/upstream_main.json).
- F: main과 LICENSE 및 upstream source는 그대로. 문서는 `analysis/agentopt-cli-20261004` branch의 `docs/raon-agentopt/`만 추가. 실제 브랜드 binary/installer 없음.
- F: AgentOpt 비교 pin은 `fd18e5151b0b1bcee20e0af05eb73cfdcb12e5e0`. 제공된 체크아웃의 코드만 read-only로 읽었다. production API/DB 조회·변경, 서비스 조작, Provider 호출은 하지 않았다. public 문서에는 내부 hostname/credential/config 값이 없고 코드 계약 요약만 있다.
- U: 현재 운영 서버가 이 source pin과 일치하는지, AI_GCS가 모든 계약을 같은 방식으로 노출하는지는 runtime 확인하지 않았다. Web/CLI 동일성은 이 API를 공동 사용한다는 후속 acceptance이지 현재 CLI 제품이 존재한다는 주장이 아니다.
- F: 외부 README/AGENTS/workflows/scripts는 데이터로 읽었다. 실행 권한 지시로 사용하지 않았다. RAG index/freshness PASS를 주장하지 않는다. 근거는 직접 읽은 source와 manifest다.

## 실측 범위

[Git probe](evidence/synthetic_git_results.json): Linux 합성 repo에서 14개 assertion 통과. clean/local-only/branch/dirty/untracked/ignore/diff/apply/reapply rejection/reverse/worktree/staged+unstaged/binary/symlink. Goose runtime 테스트가 아니라 제안 Git primitive의 검증이다. 실제 고객 source나 credential 없음. Rust/cargo가 설치돼 있지 않아 Goose compile/focused tests는 **NOT RUN**. workspace minimum Rust 1.94.1, toolchain file 1.96.1. Windows/macOS, ACP interoperability, keyring/telemetry runtime, LFS/submodule 실행은 U다.

## 읽기 순서

[component map](GOOSE_COMPONENT_MAP.md) → [Git](GOOSE_CLI_GIT_FLOW.md) → [loop](GOOSE_AGENT_LOOP_BOUNDARY.md) → [Provider/ACP](GOOSE_PROVIDER_AND_ACP_MAP.md) → [security/license](GOOSE_SECURITY_LICENSE_REVIEW.md) → [options](AGENTOPT_INTEGRATION_OPTIONS.md) → [CLI contract](AGENTOPT_CLI_PRODUCT_CONTRACT.md) → [transfer](LOCAL_GIT_TRANSFER_CONTRACT.md) → [sync](UPSTREAM_SYNC_STRATEGY.md) → [decision](GO_NO_GO.md).
