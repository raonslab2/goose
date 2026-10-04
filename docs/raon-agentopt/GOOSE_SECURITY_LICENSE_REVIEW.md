> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# 보안·라이선스·공급망 검토

| source 근거(F) | 위험 | RAON 정책(P) / 남은 검증(U) |
|---|---|---|
| config/base.rs, paths.rs | env/config/keyring/secrets.yaml; file 저장은 평문 surface | Provider secret 저장 금지, user token만 OS keyring, fallback 기본 금지 |
| paths.rs | OS별 config/data/state, legacy Block/goose, absolute GOOSE_PATH_ROOT | 독립 namespace, 기존 Goose secret/history 자동 import 금지 |
| base.rs Unix secure write tests | Unix mode는 Windows ACL proof 아님 | Windows DACL 및 Linux mode 실측 |
| posthog.rs | 문서 GOOSE_DISABLE_TELEMETRY와 실제 GOOSE_TELEMETRY_OFF 불일치 | telemetry compile feature 제외 |
| posthog.rs::emit_event | onboarding_*와 telemetry_preference_set는 일반 consent 검사 우회 | 해당 경로 미포함, 네트워크 canary test |
| otel/otlp.rs, tracing/, logging.rs, provider request_log | OTEL/Langfuse/JSON/model payload·source 기록 | export 제외, source/prompt/token 없는 최소 로그 |
| commands/update.rs | upstream URL/identity 다운로드·provenance, update/disable-update feature | RAON updater 제외, 별도 signing/provenance 설계 |
| extension_manager/{stdio,streamable_http,builtin}.rs | subprocess/env/package runner/OAuth/remote MCP trust | 첫 PoC off, future pinned local capability |
| developer/{shell,edit}.rs, tool_execution | 사용자 권한 shell/fs, absolute path/symlink | 모델 tool 실행 없음, bounded Git/apply만 |
| security/, permission/confirmation | scanner false negative, AlwaysAllow, tool annotations trust | input/project digest에 upload/apply 승인 binding |
| hints/plugins/hooks/recipes | context injection과 script 실행 | 데이터≠권한, auto discovery/실행 제외 |
| acp/transport/{auth,mod,tls}.rs | URL token/log/origin/listener | outbound HTTPS/SSE, listener/query credential 없음 |
| config/tls.rs | client cert/key/CA 경로가 trust 변경 | validated roots, 인증 실패 fail-closed |

F: Linux config는 일반적으로 ~/.config/goose 계열, macOS는 legacy Block/goose OS strategy, Windows는 app strategy 경로다. 정확한 Windows/macOS runtime 경로는 U이므로 하드코딩하지 않는다. root override는 config/data/state 및 .agents 경로를 사용한다. sessions.db/log/export에도 source가 남을 수 있다. base.rs에서 keyring 미포함 build나 disable 설정은 file 저장으로 이어진다. Provider key와 user login token은 별개다.

F: PostHog 실제 opt-out은 GOOSE_TELEMETRY_OFF=1/true 또는 GOOSE_TELEMETRY_ENABLED=false이며 미선택은 일반 telemetry opt-in 전송을 막는다. 그러나 emit_event의 onboarding 경로는 일반 검사를 우회한다. CUSTOM_DISTROS.md의 GOOSE_DISABLE_TELEMETRY=1을 실제 비활성화 증거로 쓰면 안 된다. OTEL_SDK_DISABLED 등 별도 OTEL 경로도 있다. source sanitizer는 완전 secret detector가 아니다.

## egress 중앙화 조건

P: 선택 구조에서 모델 endpoint/Provider credential/Provider process는 서버 AgentOpt 소유다. Provider egress는 서버 경계를 따른다. 모든 네트워크의 중앙화를 뜻하지 않는다. PC→AgentOpt auth/API, 사용자 Git fetch/push, installer/update, future local build dependency fetch는 PC egress다. 각각 별도 정책이 필요하다. remote MCP/telemetry/model metadata/voice/local ACP process를 유지하면 추가 PC egress가 발생한다. Local Runner도 임의 shell network를 기본 허용하지 않는다. 이번 작업에서는 네트워크 정책을 바꾸지 않았다.

## Apache-2.0

F: LICENSE 원문을 byte-for-byte 보존했다. tracked tree에 NOTICE 이름 파일은 관측되지 않았다(source manifest inventory). 배포 dependency/artifact의 notice는 별도 확인해야 한다.

[Apache §4/§6](https://www.apache.org/licenses/LICENSE-2.0): license와 관련 attribution 보존, 수정 파일 자체에 prominent modification notice, 상표 오인 방지. 향후 수정 파일은 RAON modification: date/purpose comment/header와 patch register를 함께 둔다. 이번에는 새 분석 문서만 추가했다. RAON 제품은 출처를 설명하되 공식 Goose/AAIF endorsement처럼 보이지 않아야 한다.

## 공급망

F: Cargo.lock/Rust workspace/vendor/v8, Desktop package.json/pnpm lock/Electron 및 build scripts는 서로 다른 dependency closure다. upstream Apache만으로 모든 dependency 의무가 해결되지 않는다. workspace minimum Rust 1.94.1, toolchain 1.96.1을 구분한다. Desktop postinstall은 ACP TS client build를 포함하며 CLI-only 선택으로 이 surface를 줄일 수 있다.

F: deny.toml은 advisory/yanked 검사와 rsa RUSTSEC-2023-0071 예외를 포함한다. 전체 license audit PASS가 아니다. release.yml에 attest-build-provenance, Windows bundle에 conditional Azure signing, macOS bundle에 conditional signing/notarization이 있다. source workflow 존재≠fork artifact signing 완료. updater는 digest/Sigstore provenance 검증 및 Windows 교체 경로를 갖는다.

P: 후속 PoC에서 실제 선택 closure의 cargo metadata/deny/audit/SBOM/license inventory, native vendor notices와 npm 제외를 검증한다. 고객 배포 전 target별 license bundle, RAON provenance subject, Authenticode/rollback, install scripts/pinned Actions를 검토한다. U: 전체 dependency license 분류, 취약점 해결, signing/runtime은 미수행. fork release workflow 실행/secret 주입은 없었다.

## 직접 확인한 bundled notice 예시(F)

goose/src/session/export_html/vendor/marked.min.js header는 Marked v18.0.5/MIT copyright를, highlight.min.js header는 Highlight.js v11.9.0/BSD-3-Clause notice를 포함한다. 따라서 root NOTICE 파일이 없어도 embedded notice를 삭제하면 안 된다. 두 파일은 crates/ 하위이며 source manifest에 포함했다. vendor/v8의 native dependency까지 포함한 전체 배포 closure는 별도 조사해야 한다.

## MCP 역할 분리(P)

config/extensions.rs의 enabled entry와 timeout, agents/extension.rs의 타입, extension_manager의 tool owner/lifecycle, config/permission.rs의 AlwaysAllow/AskBefore/NeverAllow와 tool annotations가 Goose 로컬 실행 정책을 구성한다. stdio.rs는 command/args/env를 process에 전달하고 optional Docker 실행도 한다. streamable_http.rs는 OAuth를 다룬다. container 옵션이나 malware check 자체가 완전 sandbox/신뢰 보장이 아니다. RAON 첫 PoC는 MCP를 쓰지 않으며, 향후 local capability는 승인된 path/tool digest/bounds로 제한한다. AgentOpt server MCP/tools와 local MCP를 서로 다른 principal로 구분하고 server 요청이 임의 extension 설치·env 전달을 허용하지 않게 한다. Agent.Tools의 Score/context/rules 역할을 로컬 Goose extension manager로 대체하지 않는다.
