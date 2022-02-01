require_relative './mopidy/lib/mopidy.rb'
require 'optparse'

class RubyMopidy
  MAXIMUM_VOLUME = 80
  VOLUME_INCREMENT = 10
  def initialize(options)
    @options = options
    Mopidy.configure do |config|
      config.mopidy_url = 'http://localhost:6680/mopidy/rpc'
    end
  end

  def call
    p @options
    case @options[:command]
    when 'volume'
      if @options[:options] == 'up'
        volume_up
      elsif @options[:options] == 'down'
        volume_down
      else
        change_volume(@options[:options].to_i)
      end
    when 'navigation'
      if @options[:options] == 'next'
        p 'play next song'
        next_song
      elsif @options[:options] == 'pause'
        p 'pausing broadcast'
        Mopidy::Playback.pause
      elsif @options[:options] == 'play'
        p 'playing songs'
        Mopidy::Playback.play
      elsif @options[:options] == 'stop'
        p 'stop'
        Mopidy::Playback.stop
      elsif @options[:options] == 'shuffle'
        p 'shuffle songs'
        Mopidy::Tracklist.shuffle #`shuffle': wrong number of arguments (given 0, expected 2) (ArgumentError)
      end
    when 'album'
      play_album(@options[:options])
    when 'playlist'
      play_playlist(@options[:options])
    when 'track'
      play_track(@options[:options])
    when 'episode'
      play_track(@options[:options])
    when 'webradio'
      play_webradio(@options[:options])
    end
  end

  def find_state
    Mopidy::Playback.state
  end

  def search_uri(uri)
    Mopidy::Library.lookup(uri)
  end

  def search_tracks(string)
    response = Mopidy::Library.search(string)
    response.body.first['tracks'].first
  end

  def play_album(album_uri)
    stop
    Mopidy::Tracklist.clear
    Mopidy::Tracklist.add_uri("spotify:album:#{album_uri}")
    play
  end

  def play_playlist(playlist_uri)
    stop
    Mopidy::Tracklist.clear
    Mopidy::Tracklist.add_uri("spotify:playlist:#{playlist_uri}")
    play
  end
  
  def play_webradio(uri)
    stop
    Mopidy::Tracklist.clear
    Mopidy::Tracklist.add_uri(uri)
    play
  end

  def add_track(track)
    Mopidy::Tracklist.clear
    Mopidy::Tracklist.add_uri(track)
  end

  def play_track(track)
    stop
    add_track("spotify:track:#{track}")
    play
  end

  def play_episode(track)
    stop
    add_track("spotify:episode:#{track}")
    play
  end

  def volume_up
    volume = Mopidy::Mixer.volume.body
    if volume < (MAXIMUM_VOLUME - VOLUME_INCREMENT)
      volume += VOLUME_INCREMENT
    elsif volume < MAXIMUM_VOLUME
      volume = MAXIME_VOLUME
    end
    Mopidy::Mixer.volume = volume
  end

  def volume_down
    volume = Mopidy::Mixer.volume.body
    if volume > VOLUME_INCREMENT
      volume -= VOLUME_INCREMENT
    elsif volume < VOLUME_INCREMENT
      volume = 0
    end
    Mopidy::Mixer.volume = volume
  end

  def change_volume(value)
    Mopidy::Mixer.volume = value
  end

  def stop
    Mopidy::Playback.stop
  end

  private

  def playing?
    find_state.body['result'] == 'playing'
  end

  def play
    Mopidy::Playback.play
  end

  def next_song
    Mopidy::Playback.next
  end
end

option_parser = OptionParser.new do |opts|
  opts.on '-i', '--include', 'Include protocol headers'
  opts.on '-v', '--[no-]verbose', 'Make the operation more talkative'
  opts.on '-m', '--message=MSG', 'Use the given message'
  opts.on '-c', '--command=COMMAND', 'Use the given command'
  opts.on '-o', '--options=OPTIONS', 'Option for the given command'
end
options = {}

option_parser.parse!(into: options)

RubyMopidy.new(options).call
# track = client.search_tracks('stan')
# client.play_track(track)
# client.volume_down
# client.search_tracks('princesse et le dictateur')
# album_uri = 'spotify:album:59HnOYmSTW2CgNihmws5H4'
# client.play_album(album_uri)
