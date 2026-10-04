> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Goose CLI와 Local Git 흐름

## 실제 구현(F)

cli.rs가 cwd/session, text/file/stdin 실행 입력, resume/no-session, provider/extension 옵션을 파싱한다. session/builder.rs는 로컬 SQLite session과 Agent를 만들고 Provider/extension을 연결한다. session/mod.rs는 Agent reply stream과 tool confirmation을 처리하며 output/streaming_buffer/input/elicitation이 terminal UX를 제공한다. history 소유자는 서버 Request가 아니라 SessionManager다.

조사한 developer 도구는 shell과 file read/write/edit/tree다(developer/mod.rs). branch/HEAD/status/diff/commit/patch/worktree/rollback은 임의 shell Git 또는 extension으로 가능하다. 그러나 이를 안전한 typed Git lifecycle 제품 계약으로 제공하는 것은 아니다. subprocess.rs::git_command는 implicit bare repository와 fsmonitor를 방어하지만, 임의 shell에서 실행한 git에 자동 적용되는 정책은 아니다.

hints/load_hints.rs는 상위 .git 존재로 root와 import boundary를 찾는다. .git 파일도 존재 검사에 해당하므로 worktree root 탐지에 사용할 수 있다. import_files.rs는 gitdir/commondir와 metadata import 추가 방어를 한다. developer/tree.rs는 git_ignore/exclude/global 및 require_git(false) walker를 사용한다. 이는 context 선택 지원이지 snapshot manifest나 secret 검증이 아니다.

developer/edit.rs는 fs::read_to_string, fs::write와 before/after 문자열 교체다. Git patch transaction/base hash/conflict rollback 계약은 없다. file helper 자체는 repo root containment를 보장하지 않으며 일반 filesystem의 symlink 동작을 고려해야 한다. 승인 UI가 filesystem isolation을 제공하지 않는다.

| 기능 | 확인한 수준(F) | 필요한 계약(P) |
|---|---|---|
| branch/HEAD/status/diff/commit | shell Git 사용 가능 | typed argv, NUL-safe parse, immutable base binding |
| dirty/index/untracked | Git/file로 관찰 가능 | staged/unstaged 분리, untracked opt-in, overwrite 금지 |
| worktree | cwd/.git pointer hints 처리 | lease/lock/conflict/cleanup/rollback receipt |
| ignore/large repo | ignore-aware tree/context | allowlist manifest, payload bounds, 누락 표시 |
| local-only/no remote | 로컬 도구에 remote 불필요 | AgentOpt snapshot 실행 API gap |
| symlink/submodule/LFS | Git 표현 가능 | escape 차단, gitlink SHA, pointer/object 분리 |
| binary | text editor 부적합 | 첫 PoC 거부, 향후 digest object 정책 |
| patch/apply | shell git apply 가능 | complete evidence/base hash/dry-run/receipt |

## 동작 검증

[합성 probe](evidence/synthetic_git_probe.py)를 Linux 임시 repo에서 실행하여 [14개 assertion](evidence/synthetic_git_results.json)이 통과했다. diff는 untracked를 포함하지 않고, 같은 patch 재적용은 실패하며, staged/unstaged가 구분되고 worktree .git은 파일이다. **Git primitive 검증이며 Goose CLI runtime PASS가 아니다.** 고객 source/credential은 사용하지 않았다.

## 플랫폼

developer/shell.rs는 Windows 기본 cmd, GOOSE_SHELL override와 executable별 flag, Unix -c 경로를 갖는다. subprocess.rs는 Windows no-window, Unix process group, Linux parent-death signal을 구분한다. goose-cli/src/signal.rs와 Cargo의 Windows console/winapi dependency도 플랫폼 차이를 나타낸다. Windows/macOS runtime은 미검증이다.

P: RAON Git 호출은 shell 문자열 대신 executable+argv로 고정한다. Windows path/UTF-8/CRLF/case/drive/UNC/reparse point/console cancellation을 별도 acceptance로 검증한다. 기존 portability 코드를 재사용해도 이 검증을 생략하지 않는다.
