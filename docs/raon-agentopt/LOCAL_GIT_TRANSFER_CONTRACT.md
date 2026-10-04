> RAON 분석 추가: 2026-10-04 UTC. 분석 전용, 배포물이 아님. Goose source pin `591edd47cf2cfea4957d720c607cf2a4def8673d`. 사실(F), 설계 제안(P), 미검증(U)을 구분한다. 아래 upstream 경로는 모두 이 SHA 기준이며 [source evidence](evidence/source_manifest.json)에 파일 해시와 검색 위치가 있다.

# Source 전송·Local Git 계약

이 문서의 계약은 P다. 서버 project policy가 mode를 허용하며 client가 다른 project workspace를 선택할 수 없다. source upload/model processing 동의를 구분한다. source를 PC에 보관해도 model prompt/tool output에 내용이 들어가면 Provider로 전송될 수 있다.

| mode | source truth/전송 | 실행 | privacy/cost | 범위 |
|---|---|---|---|---|
| 1 remote Git canonical | 승인된 remote identity+immutable SHA, 전체 upload 없음 | 기존 server Worker/worktree/Provider | 서버·remote에 source 존재, dirty 제외 | Windows 첫 PoC |
| 2 local snapshot | remote 불필요, HEAD+selected tracked blobs+index/worktree diff+opt-in untracked CAS | temporary server workspace, 기존 Worker 통합 | 선택 source가 PC 밖으로 나감 | 별도 후속 gate |
| 3 Local Runner | PC source, outbound signed bounded lease/result | server scheduler 소유, runner capability 실행 | prompt/log leak 별도 통제 | future, 구현 없음 |

## immutable manifest

schema/version/project/repo identity(credential URL 제외)/hash algorithm/HEAD/path/mode/type/size/blob digest/base hash/index delta/worktree delta/excluded reasons/untracked inventory/limits를 canonical JSON+SHA-256으로 binding한다. Git SHA와 transport SHA-256을 혼동하지 않는다. 서버는 path/size/digest를 검증하고 필요한 context 누락을 거부한다. 누락 파일을 몰래 fetch하지 않는다. .git/config/hooks를 전송하거나 서버 repo에 설치하지 않는다.

F: Git probe는 staged/unstaged/diff/untracked/binary/symlink의 차이를 확인했다. 현 CreateRequest에는 snapshot/manifest/SHA 필드가 없으며 attachments/references로 execution root 변경을 승인하지 않는다(app.py/workspaces.py).

## 경계

- dirty: 자동 stash/reset/commit 없음. HEAD/index/worktree와 포함 선택을 표시한다. Mode1은 clean input 또는 dirty 무시를 명시적으로 고지하고 Mode2는 accepted effective bytes를 base로 한다.
- untracked: 기본 제외, path별 opt-in/preview. gitignore/info exclude/global ignore+RAON deny/secret detection. tracked secret도 차단한다. ignore≠secret proof. keyring/SSH/env/DB credential/.git 전송 금지.
- binary/LFS: 첫 PoC 수정 거부. 향후 digest/size object 정책; pointer≠object. 자동 smudge/download/URL credential 전달 없음. 필요한 object 누락 시 거부.
- submodule: gitlink SHA만 기록, 기본 recurse 없음. 별도 immutable manifest/동의 필요. nested .git/unsafe .gitmodules URL 차단. 첫 PoC submodule 수정 제외.
- symlink/reparse: root 밖을 따르지 않으며 첫 PoC 포함/수정 거부. 향후 link metadata 보존+traversal guard. Windows junction/drive/UNC/case collision/reserved names/NTFS ADS, absolute/../NUL/control path를 extraction/apply 전에 거부.
- large repo: deterministic allowlist/dependency closure preview/omission report. 제안 기본값: uncompressed 20 MiB, text file 1 MiB, 2,000 paths. 측정된 서버 한도가 아니며 project가 낮출 수 있다. overflow는 거부하고 silent truncate하지 않는다. zip bomb/중첩 expansion 별도 제한.
- encryption: TLS 검증, project별 encrypted at rest/user auth, cross-project CAS 존재 oracle 차단. token URL 금지. 제안 retention은 snapshot ≤7일, 실패 transient workspace ≤24시간, project별 축소 가능. 실제 source 사용 전 정책 승인 필요. source-bearing evidence에도 retention 적용, cleanup receipt 제공.

## patch/apply/rollback

terminal delivery manifest에 Request/input SHA 또는 snapshot/evidence digest/pre/post file hashes/modes/completeness/Validation을 binding한다. apply는 auth·base hash·path·lock·truncation을 검사하고 격리 worktree/index에서 git apply --check 후 진행한다. touched files/index 원본을 journal로 보관하고 deterministic 변경을 적용한다. 강제 reset/stash rollback은 금지한다. rollback은 journal이 쓴 값과 일치하는 파일/index에만 적용하며 concurrent user edit는 안전하게 중단한다. crash recovery는 fsync/atomic write/race protection이 필요하고 단순 dry-run만으로 입증되지 않는다.

untracked artifact는 create-only 승인, overwrite 금지. F: evidence.py의 untracked omission/truncation 때문에 기존 patch endpoint만으로 auto apply를 허용할 수 없다. double apply는 receipt/post hash로 no-op 또는 conflict. 자동 commit/push/remote 변경 없음. worktree branch를 빼앗지 않고 새 lease/branch를 사용한다. local apply receipt≠server Validation.

## future Local Runner

signed envelope는 Request/project/device/task/capability/version/typed argv/repo/input digest/root allowlist/deadline/resources/output bound/nonce/lease/attempt/signature rotation을 포함한다. PC가 HTTPS/WSS를 시작하고 inbound SSH/listener는 없다. 모델 key나 agent loop 없이 한 bounded step을 실행한다. expired/replay/wrong-project를 거부하며 cancel/reconnect는 server lease로 해결한다. non-idempotent tool을 자동 반복하지 않는다. result는 envelope/tool version/input-output digest에 binding하며 compromised PC 결과는 untrusted다. build dependency fetch는 별도 local-egress 예외다. 구현하지 않았다.
