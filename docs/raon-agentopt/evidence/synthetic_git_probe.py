"""RAON analysis addition, 2026-10-04. Synthetic Git contract probes, not Goose runtime tests."""
import json, pathlib, subprocess, tempfile

def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='raon-synthetic-') as tmp:
        repo = pathlib.Path(tmp) / 'repo'; repo.mkdir()
        def git(*args, ok=True):
            p = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-c', 'safe.bareRepository=explicit', '-C', str(repo), *args], capture_output=True, text=True)
            if ok and p.returncode: raise RuntimeError(p.stderr)
            return p
        def check(name, value):
            assert value, name
            results.append({'scenario': name, 'passed': True})
        git('init', '-b', 'main'); git('config', 'user.name', 'Synthetic'); git('config', 'user.email', 'synthetic@example.invalid')
        (repo/'a.txt').write_text('base\n'); (repo/'.gitignore').write_text('ignored.secret\n')
        git('add', '.'); git('commit', '-m', 'synthetic base')
        base = git('rev-parse', 'HEAD').stdout.strip()
        check('clean', git('status', '--porcelain').stdout == '')
        check('local-only-no-remote', git('remote').stdout == '')
        git('switch', '-c', 'topic'); check('branch', git('branch', '--show-current').stdout.strip() == 'topic')
        (repo/'a.txt').write_text('changed\n'); (repo/'untracked.txt').write_text('sample\n'); (repo/'ignored.secret').write_text('FAKE_SECRET\n')
        status = git('status', '--porcelain').stdout
        check('dirty-and-untracked', ' M a.txt' in status and '?? untracked.txt' in status)
        check('ignore-not-in-status', 'ignored.secret' not in status)
        patch = git('diff', '--no-ext-diff', '--no-textconv', '--binary', base).stdout
        check('diff-excludes-untracked', 'untracked.txt' not in patch)
        git('restore', 'a.txt')
        patchfile = pathlib.Path(tmp)/'result.patch'; patchfile.write_text(patch)
        git('apply', '--check', str(patchfile)); git('apply', str(patchfile))
        check('apply', (repo/'a.txt').read_text() == 'changed\n')
        check('reapply-conflict-refused', git('apply', '--check', str(patchfile), ok=False).returncode != 0)
        git('apply', '-R', str(patchfile)); check('reverse-rollback', (repo/'a.txt').read_text() == 'base\n')
        wt = pathlib.Path(tmp)/'worktree'; git('worktree', 'add', '-b', 'isolated', str(wt), base)
        check('worktree-git-pointer', (wt/'.git').is_file())
        git('worktree', 'add', str(pathlib.Path(tmp)/'conflict'), 'isolated', ok=False)
        check('worktree-branch-conflict', git('worktree', 'add', str(pathlib.Path(tmp)/'conflict2'), 'isolated', ok=False).returncode != 0)
        (repo/'a.txt').write_text('staged\n'); git('add', 'a.txt'); (repo/'a.txt').write_text('unstaged\n')
        check('staged-and-unstaged-distinct', 'staged' in git('diff', '--cached').stdout and 'unstaged' in git('diff').stdout)
        (repo/'binary.dat').write_bytes(bytes(range(256))); git('add', 'binary.dat'); git('commit', '-m', 'binary fixture')
        (repo/'binary.dat').write_bytes(bytes(range(255,-1,-1)))
        check('binary-patch', 'GIT binary patch' in git('diff', '--binary').stdout)
        (repo/'link').symlink_to('a.txt'); git('add', 'link')
        check('symlink-mode-120000', '120000' in git('ls-files', '--stage', 'link').stdout)
    return {'kind':'synthetic-git-only', 'platform':'Linux', 'goose_runtime_executed':False, 'customer_source_used':False, 'results':results}

if __name__ == '__main__': print(json.dumps(main(), indent=2))
