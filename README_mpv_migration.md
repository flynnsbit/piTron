# PiTron MPV Migration Guide

## Overview
This guide explains how to migrate from omxd/omxplayer to mpv for video playback in your Tron pinball system.

## What Changed
- **Replaced omxd** with a custom `MPVController` class using JSON IPC
- **MPV optimizations** for gapless playback and hardware acceleration
- **Preserved all playlist logic** - the `filechecker()` function API remains identical
- **Maintained zero-delay transitions** between videos

## Installation Steps

### 1. Install MPV
```bash
sudo apt update
sudo apt install mpv
```

### 2. Verify Hardware Acceleration
On Raspberry Pi, ensure MPV can use hardware decoding:
```bash
mpv --hwdec=help
```
If you see `v4l2m2m` or similar, MPV should work well with video acceleration.

### 3. Test MPV Installation
```bash
mpv --version
```
Should show version information.

### 4. Optional: Install socat (usually already available)
```bash
sudo apt install socat
```

## Key Features Preserved

### Playlist Management
- **Clear (X)**: Clears playlist, starts fresh
- **Append (a)**: Adds video to end of playlist
- **Insert (I)**: Inserts video to play after current
- **Loop (L)**: Sets fallback video that plays after all queued videos finish

### Gapless Playback
- `--gapless-audio=yes` prevents audio gaps
- `--cache=yes` and `--cache-secs=3` pre-buffers videos
- `--idle=yes` keeps mpv running between videos

### Hardware Acceleration
- `--hwdec=auto` enables Raspberry Pi GPU acceleration
- `--vo=gpu` uses GPU video output

## File Changes

### New MPV Controller Class
The `MPVController` handles all communication with mpv daemon via socket commands.

### Updated filechecker() Function
```python
def filechecker(x, y, z):
    # x = TRUE | FALSE - Clear the playlist
    # y = Append (a), Insert (I), Loop (L)
    # z = file path
```

Same API as before, but internally uses mpv commands.

### Daemon Startup
```python
# Start MPV daemon
logger.info("Starting MPV daemon...")
if mpv.start_mpv_daemon():
    logger.info("MPV daemon started successfully")
else:
    logger.error("Failed to start MPV daemon")
    exit(1)
```

## Testing

### Basic Test
After installation, test basic functionality:
```bash
python3 ogtron_v20_mpv.py
```

### Verify Playlist Operations
1. **Attract Mode**: Should loop single video
2. **Game Start**: Should clear and start game_start.mp4
3. **State Changes**: Video transitions should be instant
4. **Multi-Player**: Should maintain separate player states

## Performance Benefits

### Better Hardware Acceleration
MPV has more up-to-date Raspberry Pi GPU support than omxplayer.

### Improved Reliability
mpv is actively maintained, unlike the aging omx suite.

### Better Memory Management
mpv has better memory usage for long-running processes.

## Troubleshooting

### MPV Won't Start
- Check `/tmp/mpvsocket` permissions
- Verify ffmpeg installation: `ffmpeg -version`

### Videos Not Playing
- Check file paths in video directories
- Verify GPU memory allocation in `/boot/config.txt`
- Test with: `mpv --no-video <video.mp4>` (check audio only)

### GAP Errors
- Add `--demuxer-lavf-allow-mimetype=yes` if needed
- Check video codec compatibility

## Rollback
If you need to rollback:
1. Stop the script
2. `sudo pkill mpv`
3. Delete the socket: `rm -f /tmp/mpvsocket`
4. Use original ogtron_v19.py

## Technical Notes

### Why MPV Instead of VLC?
- VLC is heavier on resources
- MPV playlist control is more precise
- MPV has better embedded device performance

### Socket Communication
MPV uses JSON over Unix socket for commands:
```python
{"command": ["loadfile", "/path/to/file.mp4", "append"]}
```

### Playlist Logic
The system maintains a "loop fallback" video concept where certain videos (like game_start.mp4) become the default playback after temporary overlays finish.
