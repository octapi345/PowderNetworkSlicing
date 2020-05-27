#!/bin/bash
set -ux
tmux new-session -d -s enb
tmux send-keys 'sudo srsepc /etc/srslte/epc.conf' C-m
sleep 1.0
tmux split-window -v
tmux send-keys 'sudo srsenb /etc/srslte/enb.conf' C-m
tmux split-window -v
tmux select-layout even-vertical
tmux attach-session -d -t enb
