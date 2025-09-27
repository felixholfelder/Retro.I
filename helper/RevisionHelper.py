import subprocess


class RevisionHelper:

    # TODO - get only remote branches
    # TODO - hide HEAD "branch/tag"
    def get_branches(self) -> list[str]:
        local = subprocess.check_output(["git", "branch", "--format=%(refname:short)"], text=True).splitlines()

        remote = subprocess.check_output(["git", "branch", "-r", "--format=%(refname:short)"], text=True).splitlines()

        remote_clean = [r.split("/", 1)[1] for r in remote if r.startswith("origin/")]

        all_branches = sorted(set(local) | (set(remote_clean) - set(local)))

        def branch_sort_key(branch: str):
            if branch in ("main", "master"):
                return (0, branch)
            elif branch.startswith("renovate/"):
                return (2, branch)
            else:
                return (1, branch)

        return sorted(all_branches, key=branch_sort_key)

    def get_tags(self) -> list[str]:
        tags = subprocess.check_output(
            ["git", "for-each-ref", "--sort=-creatordate", "--format=%(refname:short)", "refs/tags"], text=True
        ).splitlines()
        return tags

    def get_current_revision(self) -> str:
        try:
            # try with tag
            tag = subprocess.check_output(
                ["git", "describe", "--tags", "--exact-match"], text=True, stderr=subprocess.DEVNULL
            ).strip()
            if tag:
                return tag
        except subprocess.CalledProcessError:
            pass

        # try with branch
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        if branch != "HEAD":
            return branch

        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        return commit
