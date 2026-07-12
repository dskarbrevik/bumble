# secrets/

Personal captures and credentials (signal captures, badge IDs, API keys). Everything
in this directory except this README is gitignored — verify with `git check-ignore`
before adding a new file type anywhere else that might carry secrets.

Agent conventions: treat files here as read-only personal data. Never copy their
contents into committed files, logs, or source code — reference them by path, and
generate any derived artifacts (e.g. compiled key headers) into gitignored locations.
When in doubt, gitignore first, ask second.
