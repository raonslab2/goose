"""RAON analysis addition, 2026-10-04. Records pinned public sources and sanitized contract locations."""
from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[3]; out=root/'docs/raon-agentopt/evidence'
sha='591edd47cf2cfea4957d720c607cf2a4def8673d'
paths=['Cargo.toml','Cargo.lock','rust-toolchain.toml','CUSTOM_DISTROS.md','LICENSE','deny.toml','BUILDING_LINUX.md','ui/desktop/package.json','ui/desktop/src/updates.ts','ui/desktop/src/app-update.yml','.github/workflows/release.yml','.github/workflows/bundle-windows.yml','.github/workflows/bundle-macos.yml','.github/workflows/ci.yml','.github/workflows/cargo-deny.yml','crates/goose-cli/Cargo.toml','crates/goose-cli/src/main.rs','crates/goose-cli/src/lib.rs','crates/goose-cli/src/cli.rs','crates/goose-cli/src/logging.rs','crates/goose-cli/src/signal.rs','crates/goose-cli/src/commands/session.rs','crates/goose-cli/src/commands/update.rs','crates/goose-cli/src/commands/roam_client.rs','crates/goose-cli/src/commands/schedule.rs','crates/goose/src/agents/agent.rs','crates/goose/src/agents/state_machine/mod.rs','crates/goose/src/agents/state_machine/ops_llm.rs','crates/goose/src/agents/tool_execution.rs','crates/goose/src/agents/reply_parts.rs','crates/goose/src/agents/subagent_handler.rs','crates/goose/src/agents/subagent_execution_tool/mod.rs','crates/goose/src/agents/mcp_client.rs','crates/goose/src/agents/extension_manager/mod.rs','crates/goose/src/session/session_manager.rs','crates/goose/src/hints/load_hints.rs','crates/goose/src/hints/import_files.rs','crates/goose/src/subprocess.rs','crates/goose/src/posthog.rs','crates/goose/src/otel/mod.rs','crates/goose/src/otel/otlp.rs','crates/goose/src/logging.rs','crates/goose/src/acp/provider.rs','crates/goose/src/acp/server.rs','crates/goose/src/acp/server_factory.rs','crates/goose/src/acp/fs.rs','crates/goose/src/acp/transport/mod.rs','crates/goose/src/acp/transport/auth.rs','crates/goose/src/acp/transport/tls.rs','crates/goose/src/providers/mod.rs','crates/goose/src/providers/provider_registry.rs','crates/goose/src/providers/codex_acp.rs','crates/goose/src/providers/claude_acp.rs','crates/goose-providers/src/lib.rs','crates/goose-providers/src/openai.rs','crates/goose-providers/src/anthropic.rs','crates/goose-providers/src/api_client.rs','crates/goose-provider-types/src/base.rs','crates/goose-provider-types/src/request_log.rs','crates/goose-agent/Cargo.toml','crates/goose-agent/src/machine.rs','crates/goose-agent/src/inference.rs']
for prefix,names in [('crates/goose-cli/src/session/', ['mod','builder','input','editor','completion','paste','output','streaming_buffer','thinking','elicitation']),('crates/goose/src/config/', ['base','paths','extensions','permission','tls','declarative_providers']),('crates/goose/src/agents/platform_extensions/developer/', ['mod','shell','edit','tree']),('crates/goose/src/agents/platform_extensions/', ['scheduler','orchestrator']),('crates/goose/src/agents/extension_manager/', ['stdio','builtin','streamable_http'])]:
    paths += [prefix+n+'.rs' for n in names]
tracked=subprocess.check_output(['git','-C',str(root),'ls-files'],text=True).splitlines()
paths += ['crates/goose/src/session/export_html/vendor/marked.min.js', 'crates/goose/src/session/export_html/vendor/highlight.min.js', 'crates/goose/src/agents/extension.rs']
paths += [p for p in tracked if p.startswith('crates/goose-providers/src/declarative/') and p.endswith('.rs')]
paths += [p for p in tracked if p.startswith('crates/goose/src/acp/server/') and p.endswith('.rs')]
paths += [p for p in tracked if p.startswith('vendor/') and re.search(r'(LICENSE|NOTICE|COPYING)',Path(p).name,re.I)]
keywords=re.compile(r'Agent::new|update_provider|async fn (reply|create|stream)|GOOSE_STATE_MACHINE|GOOSE_TELEMETRY_OFF|TELEMETRY_ENABLED_KEY|is_onboarding_event|pub async fn emit_event|DB_NAME|GOOSE_PATH_ROOT|GOOSE_DISABLE_KEYRING|enum SecretStorage|git_command|core.fsmonitor|safe.bareRepository|fn find_git_root|fn resolve_path|fn file_(read|write|edit)|fn windows_shell|GOOSE_SHELL|verify_provenance|sigstore|check_acp_token|X-Secret-Key|fn acp_http_options|OTEL_SDK_DISABLED|\[features\]|^default =|^rust-version|^channel =|^pub trait Provider')
entries=[];missing=[]
for p in sorted(set(paths)):
    file=root/p
    if not file.is_file(): missing.append(p);continue
    data=file.read_bytes();lines=data.decode(errors='replace').splitlines()
    hits=[{'line':i,'anchor':m.group(0)} for i,line in enumerate(lines,1) if (m:=keywords.search(line))][:40]
    entries.append({'path':p,'sha256':hashlib.sha256(data).hexdigest(),'line_count':len(lines),'url':f'https://github.com/aaif-goose/goose/blob/{sha}/{p}', 'anchors':hits})
notice=[p for p in tracked if re.match(r'^NOTICE(?:[._-].*)?$',Path(p).name,re.I)]
result={'upstream_sha':sha,'observed_at_utc':'2026-10-04','baseline_sha':sha,'ahead':0,'behind':0,'notice_inventory':notice,'license_sha256':hashlib.sha256((root/'LICENSE').read_bytes()).hexdigest(),'files':entries,'requested_paths_not_present':missing,'method':'direct source reads; anchors are symbols, not credential-bearing excerpts'}
(out/'source_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Workspace source pin, hashes and route/contract symbols only. Never embed runtime config, hostnames or credentials.
ao=root.parent; ao_sha=subprocess.check_output(['git','-C',str(ao),'rev-parse','HEAD'],text=True).strip()
ao_entries=[]
for n in ['app','auth','store','acceptance','scores','evidence','workspaces','adapters','dispatcher','agent_tools_release']:
    p=f'agentopt_v2/{n}.py';data=(ao/p).read_bytes();lines=data.decode().splitlines()
    anchors=[]
    for i,line in enumerate(lines,1):
        if re.match(r'\s*@app\.(get|post|patch|delete|put)\(',line): anchors.append({'line':i,'symbol':line.strip()})
        else:
            m=re.match(r'(?:async )?def ([A-Za-z_][A-Za-z0-9_]*)\(|class ([A-Za-z_][A-Za-z0-9_]*)',line)
            if m: anchors.append({'line':i,'symbol':m.group(1) or m.group(2)})
    ao_entries.append({'path':p,'sha256':hashlib.sha256(data).hexdigest(),'anchors':anchors})
(out/'agentopt_contract_manifest.json').write_text(json.dumps({'source_commit':ao_sha,'access':'assigned source worktree read-only; no production API/DB','files':ao_entries},indent=2)+'\n')
print(json.dumps({'public_source_files':len(entries),'missing_paths':missing,'NOTICE':notice}))
