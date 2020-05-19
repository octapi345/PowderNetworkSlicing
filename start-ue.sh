#!/bin/bash
set -ux
tmux new-session -d -s ue
tmux send-keys 'sudo srsue /etc/srslte/ue.conf' C-m
tmux split-window -v
tmux select-layout even-vertical
tmux attach-session -d -t ue
