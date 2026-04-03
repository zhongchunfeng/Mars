#!/bin/bash
set -euo pipefail

# 简单的安全审计：检查是否包含敏感配置
echo "Running security audit..."
if grep -r "PASSWORD\|SECRET\|KEY" . --exclude-dir=.git --exclude="sync.sh"; then
    echo "Error: Potential secrets detected! Push aborted."
    exit 1
fi

echo "No secrets detected. Proceeding with sync..."
git add .
git commit -m "feat(agent): update by Antigravity at $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main