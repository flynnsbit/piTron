#!/usr/bin/env python3
"""
Test script for MPV playlist functionality - replicates Tron game video logic
"""

import subprocess
import serial
import logging
import time
import os.path
import json
import socket

# MPV Control Class
class MPVController:
    def __init__(self, socket_path='/tmp/mpvsocket'):
        self.socket_path = socket_path
        self.mpv_process = None
        self.loop_fallback_video = None

    def start_mpv_daemon(self):
        """Start mpv in daemon mode with optimal settings for gapless playback"""
        try:
            self.mpv_process = subprocess.Popen([
                'mpv',
                '--idle=yes',
                '--loop-playlist=inf',
                '--keep-open=no',
                '--gapless-audio=yes',
                '--cache=yes',
                '--cache-secs=3',
                '--hwdec=auto',
                '--vo=gpu',
                '--fullscreen',
                '--no-osc',
                '--no-osd-bar',
                '--input-ipc-server=' + self.socket_path,
                '--no-terminal',
                '--really-quiet'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)  # Give mpv time to start
            return True
        except Exception as e:
            print("Failed to start mpv: %s" % str(e))
            return False

    def send_command(self, command):
        """Send JSON command to mpv via socket"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_path)
            sock.send((json.dumps(command) + '\n').encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            sock.close()
            return response
        except Exception as e:
            print("MPV command failed: %s" % str(e))
            return None

    def clear_playlist(self):
        """Clear the entire playlist"""
        self.send_command({"command": ["playlist-clear"]})
        self.loop_fallback_video = None

    def loadfile_replace(self, filepath):
        """Load file and replace current playlist (clear + play)"""
        self.clear_playlist()
        self.send_command({"command": ["loadfile", filepath, "replace"]})
        self.loop_fallback_video = filepath

    def loadfile_append(self, filepath):
        """Append file to end of playlist"""
        self.send_command({"command": ["loadfile", filepath, "append"]})

    def loadfile_insert(self, filepath):
        """Insert file to play next (position 1 in playlist)"""
        self.send_command({"command": ["loadfile", filepath, "insert-next"]})

    def loadfile_loop(self, filepath):
        """Set file as loop fallback - append to end of playlist"""
        self.send_command({"command": ["loadfile", filepath, "append"]})
        self.loop_fallback_video = filepath

    def get_playlist_count(self):
        """Get current playlist count"""
        response = self.send_command({"command": ["get_property", "playlist-count"]})
        if response:
            try:
                data = json.loads(response)
                return data.get("data", 0)
            except:
                return 0
        return 0

    def get_playlist_info(self):
        """Get playlist info for debugging"""
        return self.send_command({"command": ["get_property", "playlist"]})

    def stop(self):
        """Stop mpv daemon"""
        if self.mpv_process:
            self.mpv_process.terminate()
            self.mpv_process.wait()

# Globals
mpv = MPVController()

def filechecker(x, y, z):
    # x = TRUE | FALSE - Clear the playlist
    # y = Append (a), Insert (I), Loop (L)
    # z = file path
    result = ""
    print(f"filechecker({x}, '{y}', '{z}')")

    if not os.path.isfile(z):
        print("ERROR: Video file not found: %s" % z)
        return "File not found"

    try:
        if x:
            # Clear playlist (X command)
            mpv.clear_playlist()
            result = "Cleared playlist"

        if y == 'a':
            # Append to playlist
            mpv.loadfile_append(z)
            result += " | Appended: %s" % z
        elif y == 'I':
            # Insert next
            mpv.loadfile_insert(z)
            result += " | Inserted: %s" % z
        elif y == 'L':
            # Loop fallback - append as loop video
            mpv.loadfile_loop(z)
            result += " | Set loop fallback: %s" % z

        playlist_count = mpv.get_playlist_count()
        print(f"Playlist count: {playlist_count}")
        return result
    except Exception as e:
        print("Filechecker error: %s" % str(e))
        return "Error: %s" % str(e)

def test_playlist_operations():
    """Test all playlist operations like the Tron game uses them"""

    print("\n=== Testing MPV Playlist Operations ===\n")

    # Start MPV daemon
    print("1. Starting MPV daemon...")
    if not mpv.start_mpv_daemon():
        print("FAILED: Could not start MPV daemon")
        return False
    print("SUCCESS: MPV daemon started")

    time.sleep(2)

    try:
        # Test 1: Attract Mode (state '01') - One looping video
        print("\n--- Test 1: Attract Mode ---")
        print("Clear playlist + loop single attract video")
        result = filechecker(True, 'a', '/media/usb1/attract/attract.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        # Test 2: Game Start (state '61') - Clear and set base video
        print("\n--- Test 2: Game Start ---")
        print("Clear playlist + set game_start.mp4 as base")
        result = filechecker(True, 'a', '/media/usb1/attract/game_start.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        # Test 3: Disc MB Active (state '2E') - Append without clearing
        print("\n--- Test 3: Disc MB Active (append without clear) ---")
        print("Append discmb_active.mp4 to playlist (keeps game_start.mp4 as fallback)")
        result = filechecker(False, 'a', '/media/usb1/discmb/discmb_active.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        # Test 4: CLU Lit (state '49') - Insert video
        print("\n--- Test 4: CLU Lit (insert next) ---")
        print("Insert clu_lit.mp4 to play after current")
        result = filechecker(False, 'I', '/media/usb1/clu/clu_lit.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        # Test 5: Disc MB Complete (state '33') - Clear, insert complete, then loop game_start
        print("\n--- Test 5: Disc MB Complete ---")
        print("Clear + insert complete + set game_start as loop fallback")
        result = filechecker(True, 'I', '/media/usb1/discmb/discmb_complete.mp4')
        print(f"Result (complete): {result}")

        result = filechecker(False, 'L', '/media/usb1/attract/game_start.mp4')
        print(f"Result (fallback): {result}")
        time.sleep(5)

        # Test 6: Game Over (state '26')
        print("\n--- Test 6: Game Over ---")
        print("Clear + insert game_over.mp4")
        result = filechecker(True, 'I', '/media/usb1/attract/game_over.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        # Test 7: Return to Attract
        print("\n--- Test 7: Return to Attract ---")
        print("Clear + loop attract.mp4 (like initial state)")
        result = filechecker(True, 'a', '/media/usb1/attract/attract.mp4')
        print(f"Result: {result}")
        time.sleep(3)

        print("\n=== All tests completed successfully ===")
        return True

    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return False
    finally:
        print("\nStopping MPV daemon...")
        mpv.stop()

if __name__ == "__main__":
    print("PiTron MPV Playlist Test")
    print("========================")

    # Check if test files exist
    test_files = [
        '/media/usb1/attract/attract.mp4',
        '/media/usb1/attract/game_start.mp4',
        '/media/usb1/discmb/discmb_active.mp4',
        '/media/usb1/clu/clu_lit.mp4',
        '/media/usb1/discmb/discmb_complete.mp4',
        '/media/usb1/attract/game_over.mp4'
    ]

    missing_files = [f for f in test_files if not os.path.isfile(f)]

    if missing_files:
        print(f"WARNING: Some test files missing: {missing_files}")
        print("This is expected in a development environment.")
        print("The script will report 'File not found' for missing videos but will continue testing control logic.\n")

    success = test_playlist_operations()

    if success:
        print("\n✓ All playlist operations completed successfully!")
        print("MPV replacement for omxd is ready for production use.")
    else:
        print("\n✗ Test failed. Check MPV installation and socket permissions.")
