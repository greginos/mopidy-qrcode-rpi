import time
import logging
import argparse
import subprocess

from imutils.video import VideoStream
from pyzbar import pyzbar

log = logging
QQQR_ROOT_URI = 'qqqr:gmusic:track:'

def init():
    log.debug('init')
    t0 = time.time()

    # Initialize video stream.
    vs = VideoStream(usePiCamera=True).start()

    # Initialize Google Play Music api.
    #gmusicplay.init_gmusic_api()
    #gmusicplay.init_gmusic_track_id_info()
    #spotifyplay.init_spotipy()

    play_buzz()
    # Ensure camera sensor has had time to warm up.
    while time.time() - t0 < 2.0:
        time.sleep(0.1)

    return vs


def cleanup(vs):
    log.debug('cleanup')
    vs.stop()


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
        raise Exception('Unexpected barcode type: %s' % barcode.type)

    data = barcode.data.decode('utf-8')
    log.info('Found barcode: %s: %s' % (barcode.type, data))

    if data == 'next':
        play_next_song()
    elif data == 'volume up':
        volume_up()
    elif data == 'volume down':
        volume_down()
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
    elif not data.startswith(QQQR_ROOT_URI):
        raise Exception('Unexpected QR data: %s' % data)

    track_id = data[len(QQQR_ROOT_URI):]
    return track_id
    
def call_ruby_mopidy(command, options):
    subprocess.call(['ruby', '/home/pi/ruby-mopidy/ruby-mopidy.rb', '--command={command}'.format(command=command), '--options={options}'.format(options=options)])

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
    subprocess.call(['ruby', 'ruby-mopidy.rb', '--command=volume', '--options=up'])
    log.info('Volume going up')

def volume_down():
    subprocess.call(['ruby', 'ruby-mopidy.rb', '--command=volume', '--options=down'])
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
        #play_buzz()
        barcodes = scan_barcodes_loop(vs, tmax=1200)
        if not barcodes:
            # Timed out without detecting a barcode.
            break

        #play_buzz()

        if len(barcodes) > 1:
            log.warning('detected multiple barcodes in frame')

        track_id = parse_qqqr_barcode(barcodes[0])
        #gmusicplay.play_gmusic_track_blocking(track_id)
        #artist, title = gmusicplay.get_gmusic_track_info(track_id)
        #print((artist, title))
        #(sartist, stitle, uri) = spotifyplay.find_spotify_track(artist, title)
        #if uri is None:
            #print('No spotify track found')
            #continue
        print('Matched spotify track: %s - %s') #% (sartist, title))
        #spotifyplay.play_spotify_track(uri)

        time.sleep(3)

    cleanup(vs)

if __name__ == '__main__':
    main()

