> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Upstream sync 전략

F: fork main은 분석 upstream pin을 유지하고 분석 문서만 별도 branch에 추가했다. core patch/installer/release/tag/workflow 실행은 없고 LICENSE는 동일하다. 정식 ancestry를 유지했으며 다른 repo로 history 없이 복사하지 않았다. clone은 partial-blob filtered이지만 shallow가 아니다.

P: fork main은 검토한 upstream commit으로 fast-forward만 한다. sync마다 parent/source/public/license/NOTICE/ancestry/기준 대비 차이를 검증한다. 분석/product commit을 tracking main에 합치지 않는다. 분석 branch는 pin에서 재현 가능하게 보존한다.

후속 CLI는 별도 repo/package와 작은 provenance-labelled extraction이 유리하다. 새 work_id에서 정확한 repo를 정한다. borrowed file마다 attribution/modification notice/source SHA/dependency/license evidence를 기록한다. generic terminal crate 직접 사용이 싸면 Goose 재사용을 줄인다.

| option | 예상 변경 영역(P) | core divergence | sync 비용 |
|---|---|---|---|
| A | parser/session/agent/state machine/provider/config/MCP/API/security/update/release 8–12영역 | 큰 central patch | 빠른 release마다 광범위 회귀 |
| B | config/branding/extension/provider 2–4영역 | 작지만 canonical 요구 불충족 | core rewrite하면 B 범위 이탈 |
| C | own input/render/client/Git/cache 3–5영역, borrowed 2–6 file 후보 | upstream core 0 목표 | 선택 파일/dependency만 추종 |
| D | client/facade/auth/mapping/stream/evidence 4–7영역 | custom client면 core 0 가능 | ACP schema/SDK matrix 필요 |

이는 실제 구현 LOC/파일 수 측정이 아닌 source 기반 계획 범위다. goose-cli 전체 복제/링크는 C 추정을 무효화한다. PoC에서 dependency/build time/file count/upstream replay conflict를 실측한다.

매주 upstream security/release를 검토하고 고정 release에서 target build/focused tests 후 업데이트한다. declarative 경로 이동, alpha GDK/agent 변화, ACP/telemetry/updater를 특별 점검한다. source patch는 UI adapter에 한정하며 inference/scheduler/provider core 수정은 별도 설계 검토와 지시가 필요하다.

patch register: path/upstream SHA/license/수정 목적·일자/owner/test/conflict count. release마다 SBOM/artifact attestation/RAON signing identity를 준비한다. fork workflow 활성화 전 검토하며 이번에는 secrets를 추가하거나 실행하지 않았다. upstream PR도 제출하지 않는다.
