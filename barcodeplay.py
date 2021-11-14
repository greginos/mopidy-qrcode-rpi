import time
import logging
import argparse
import subprocess

#from espeakng import ESpeakNG
from imutils.video import VideoStream
from pyzbar import pyzbar

log = logging

def init():
    log.debug('init')
    t0 = time.time()

    # Initialize video stream.
    vs = VideoStream(usePiCamera=True).start()

    # Ensure camera sensor has had time to warm up.
    while verify_mopidy_status():
        time.sleep(0.1)

    play_buzz()
#    write_tts_file('Bonjour Gauthier')
    
    while time.time() - t0 < 2.0:
        time.sleep(0.1)

    return vs

def write_tts_file(message_text, voice=None):
    if not voice:
        voice = 'mb-fr1'
    proc = subprocess.Popen(['espeak-ng', '-m', '-v', voice, '-s', '150', '-a', '200', '--stdout' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    aplay = subprocess.Popen(['aplay', '-D', 'sysdefault:CARD=Headphones'], stdin=proc.stdout)
    proc.stdin.write(message_text.encode('utf-8') + b" <break time=\"2s\" /> " + message_text.encode('utf-8') + b" <break time=\"3s\" /> \n")
    proc.stdin.close()
    proc.wait()

def cleanup(vs):
    log.debug('cleanup')
    vs.stop()

def verify_mopidy_status():
    status = subprocess.call(['systemctl', 'is-active', 'mopidy', '--quiet'])
    log.debug({status == 0})
    status != 0

def play_buzz():
    """Play a sound to indicate success"""
    subprocess.call(['aplay', '-D', 'sysdefault:CARD=Headphones','/home/pi/ruby-mopidy/beep.wav'])

def scan_barcodes_loop(vs, tmax=1200):
    log.debug('scan_barcodes_loop')
    log.info('Ready for barcodes...')
    t0 = time.time()

    while True:
        tf = time.time()
        if tf - t0 > tmax:
            return None

        # Get a frame of video.
        frame = vs.read()

        # Detect barcodes in the frame.
        barcodes = pyzbar.decode(frame)

        log.debug("Scanned new frame in %0.2fs" % (time.time() - tf))

        if barcodes:
            return barcodes


def parse_qqqr_barcode(barcode):
    log.info('parse_qqqr_barcode')
    play_buzz()
    if barcode.type != 'QRCODE':
        return

    data = barcode.data.decode('utf-8')
    log.info('Found barcode: %s: %s' % (barcode.type, data))

    if data == 'next':
        play_next_song()
    elif data == 'volume up':
        volume_up()
    elif data == 'volume down':
        volume_down()
    elif data.startswith('volume'):
        volume_set(data.split(' ')[1])
    elif data == 'play':
        resume()
    elif data == 'pause':
        pause()
    elif data.startswith('https://open.spotify.com/track/'):
        play_song(data)
    elif data.startswith('https://open.spotify.com/episode/'):
        play_episode(data)
    elif data.startswith('https://open.spotify.com/album/'):
        play_album(data)
    elif data.startswith('https://open.spotify.com/playlist/'):
        play_playlist(data)

    
def call_ruby_mopidy(command, options):
    subprocess.call(['ruby', '/home/pi/ruby-mopidy/ruby_mopidy.rb', '--command={command}'.format(command=command), '--options={options}'.format(options=options)])

def play_next_song():
    call_ruby_mopidy('navigation', 'next')
    log.info('Play next song')
    
def resume():
    call_ruby_mopidy('navigation', 'play')
    log.info('Playing')

def pause():
    call_ruby_mopidy('navigation', 'pause')
    log.info('Pausing')
    
def volume_up():
    call_ruby_mopidy('volume', 'up')
    log.info('Volume going up')

def volume_set(value):
    call_ruby_mopidy('volume', '{value}')
    log.info('Volume set to {value}')

def volume_down():
    call_ruby_mopidy('volume', 'down')
    log.info('Volume going down')

def play_song(data):
    log.info('Playing song')
    call_ruby_mopidy('track', data.split('track/')[1].split('?')[0])

def play_episode(data):
    log.info('Playing episode')
    call_ruby_mopidy('episode', data.split('episode/')[1].split('?')[0])

def play_album(data):
    log.info('Playing album')
    call_ruby_mopidy('album', data.split('album/')[1].split('?')[0])

def play_playlist(data):
    log.info('Playing playlist')
    call_ruby_mopidy('playlist', data.split('playlist/')[1].split('?')[0])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    vs = init()

    while True:
        barcodes = scan_barcodes_loop(vs, tmax=1200)
        if not barcodes:
            # Timed out without detecting a barcode.
            break

        if len(barcodes) > 1:
            log.warning('detected multiple barcodes in frame')

        track_id = parse_qqqr_barcode(barcodes[0])
        time.sleep(1)

    cleanup(vs)

if __name__ == '__main__':
    main()

